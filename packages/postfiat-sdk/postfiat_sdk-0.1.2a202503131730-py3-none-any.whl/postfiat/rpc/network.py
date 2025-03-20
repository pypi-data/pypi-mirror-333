from typing import Any, AsyncIterator

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.models.requests import AccountTx
from xrpl.models.response import Response as XrplResponse
from tenacity import retry, stop_after_attempt, wait_random_exponential

from postfiat.nodes.task.constants import EARLIEST_LEDGER_SEQ
from postfiat.models.transaction import Transaction
from postfiat.rpc.errors import RpcFetchError


@retry(stop=stop_after_attempt(3), wait=wait_random_exponential(multiplier=1, min=4, max=15))
async def _fetch_account_txns(client: AsyncJsonRpcClient, params: dict[str, Any]) -> XrplResponse:
    request = AccountTx(**params)
    response = await client.request(request)
    if response.status != 'success':
        raise RpcFetchError.new(f'Failed to fetch account tx', response)
    return response


class RpcClient():
    """
    A client for the RPC API of the Post Fiat Network.
    """
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.xrpl_client = AsyncJsonRpcClient(endpoint)

    async def _get_account_txn_responses(self,
                         account: str,
                         start_ledger: int = EARLIEST_LEDGER_SEQ,
                         end_ledger: int = -1,
    ) -> AsyncIterator[XrplResponse]:
        params = {
            'account': account,
            'ledger_index_min': start_ledger,
            'ledger_index_max': end_ledger,
            'forward': True,
        }
        response = await _fetch_account_txns(self.xrpl_client, params)
        yield response
        marker = response.result.get('marker')
        while marker:
            params['marker'] = marker
            response = await _fetch_account_txns(self.xrpl_client, params)
            yield response
            marker = response.result.get('marker')

    async def get_account_txns(self,
                         account: str,
                         start_ledger: int = EARLIEST_LEDGER_SEQ,
                         end_ledger: int = -1,
    ) -> AsyncIterator[Transaction]:
        async for response in self._get_account_txn_responses(account, start_ledger, end_ledger):
            for txn in response.result['transactions']:
                yield Transaction.from_dict(txn)
