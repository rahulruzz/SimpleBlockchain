import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Genesis
        # Initial block of our block chain
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new block in the blockchain
        :param proof: <int> The proof (using Proof of Work algorithm)
        :param previous_hash: (Optional) <str> Hash of previous block
        :return: <dict> New block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transaction': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset current transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction. Adds to next new block to be minded
        :param sender: <string> Address of sender
        :param recipient: <string> Address of recipient
        :param amount: <int> Amount
        :return: <int> Index of block that holds this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # Hashes a block
        pass

    @property
    def last_block(self):
        # Returns the last block in the chain
        pass
