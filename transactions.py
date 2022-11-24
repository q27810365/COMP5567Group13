import time
from hashlib import sha256

class Transaction:
    def __init__(self, fromAddr: str, toAddr: str, amount: int):
        self.timestamp = int(time.time())
        self.fromAddr = fromAddr
        self.toAddr = toAddr
        self.amount = amount
        # TODO sign sig
        self.signature = ''
        self.txId = self.selfHash

    def toDict(self):
        return {
            'txID': self.txId,
            'timestamp': self.timestamp,
            'fromAddr': self.fromAddr,
            'toAddr': self.toAddr,
            'amount': self.amount,
            'signature': self.signature
        }


    @staticmethod
    def transfer(fromAddr: str, toAddr: str, amount: int, prkey: str = None):
        # TODO sign sig
        sig = None
        return Transaction(fromAddr, toAddr, amount)

    @property
    def selfHash(self):
        payload = str(self.timestamp) + self.fromAddr + self.toAddr + str(self.amount)
        return sha256(payload.encode('utf-8')).hexdigest()
