import logging

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.ledger import get_latest_validated_ledger_sequence
from xrpl.asyncio.transaction import submit_and_wait, autofill, sign
from xrpl.models.transactions.transaction import Transaction as XrplTransaction
from xrpl.wallet import Wallet

from postfiat.models.transaction import Transaction
from postfiat.nodes.task.constants import TXN_FEE
from postfiat.rpc.errors import RpcSendError

log = logging.getLogger(__name__)

_FOK_LEDGER_OFFSET = 1


class RpcSender():

    def __init__(self, endpoint: str):
        self.xrpl_client = AsyncJsonRpcClient(endpoint)

    async def submit_and_wait(self, txn: Transaction, wallet: Wallet, fill_or_kill: bool = False, fok_tolerance: int = 0) -> list[str]:
        try:
            txn = XrplTransaction.from_dict(txn.to_dict())
            if fill_or_kill:
                txn_dict = txn.to_dict()
                seq = await get_latest_validated_ledger_sequence(self.xrpl_client)
                txn_dict['last_ledger_sequence'] = seq + _FOK_LEDGER_OFFSET + fok_tolerance
                txn = XrplTransaction.from_dict(txn_dict)
                txn = await autofill(txn, self.xrpl_client)
                txn = sign(txn, wallet)
                return await submit_and_wait(txn, self.xrpl_client, check_fee=False, autofill=False, fail_hard=True)
            else:
                return await submit_and_wait(txn, self.xrpl_client, wallet)
        except Exception as e:
            log.error(f"Failed to send transaction: {txn} from wallet: {wallet}")
            raise RpcSendError(f"Failed to send transaction: {e}") from e
