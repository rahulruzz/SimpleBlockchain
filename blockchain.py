class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transaction = []

    def new_block(self):
        # Creates new block and adds to chain
        pass

    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to a list of transactions
        pass

    @staticmethod
    def hash(block):
        # Hashes a block
        pass

    @property
    def last_block(self):
        # Returns the last block in the chain
        pass
