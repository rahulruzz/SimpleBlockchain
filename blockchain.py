import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # Genesis
        # Initial block of our block chain
        self.new_block(previous_hash='1', proof=100)

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
            'transactions': self.current_transactions,
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

    def proof_of_work(self, last_proof):
        """
        Simple proof of work:
        Find a number p such that hash(pp*) contains 4 leading zeros, where p is the previous
        proof and p* is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        # Simple incrementing while, trying to find a successful proof
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    def register_node(self, address):
        """
        Add a new node to list of nodes
        :param address: <string> Address of the node i.e. 'http://192.168.1.2:5000'
        """
        self.nodes.add(urlparse(address).netloc)

    def valid_chain(self, chain):
        """
        Check if block chain is valid
        :param chain: <list> the block chain
        :return: <bool> True if valid, False if not
        """
        pass

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates proof
        :param last_proof: <int> Previous proof
        :param proof: <int> Current proof
        :return: <bool> True if correct, False if not
        """
        # Convert to unicode
        guess = f'{last_proof}{proof}'.encode()
        # Hash the guess
        guess_hash = hashlib.sha256(guess).hexdigest()
        # Is hash successful?
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block
        :param block: <dict> block
        :return: <string>
        """
        # Need to order dictionary to prevent inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last block in the chain
        return self.chain[-1]


# Create our node
app = Flask(__name__)

# Generate unique address for our node
node_id = str(uuid4()).replace('-', '')

# Instantiate blockchain
blockchain = Blockchain()


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    Example request for transaction
    {
     "sender": "my address",
     "recipient": "someone else's address",
     "amount": 5
    }
    """
    values = request.get_json()

    # Confirm all required fields are in posted data
    required = ['sender', 'recipient', 'amount']
    if not all(field in values for field in required):
        return 'Missing values', 400

    # Create new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine():
    prev_block =  blockchain.last_block
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)

    # Reward miner for finding proof
    # Sender is 0 to signify this node
    blockchain.new_transaction(
        sender="0",
        recipient=node_id,
        amount=1
    )

    # Create hash of previous block
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.new_block(proof, prev_hash)

    response = {
        'message': "New Block Created",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

