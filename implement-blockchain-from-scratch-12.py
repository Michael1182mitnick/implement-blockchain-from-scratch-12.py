# Implement a Blockchain from Scratch
# Build a simplified version of a blockchain to understand how blockchain works. Include features like adding blocks, validating the chain, and implementing proof of work.

import hashlib
import time


class Block:
    def __init__(self, index, previous_hash, timestamp, data, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.proof}".encode()
        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # Controls the difficulty of the proof of work

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", 0)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        self.proof_of_work(new_block)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def proof_of_work(self, block):
        block.proof = 0
        block.hash = block.calculate_hash()
        while not block.hash.startswith('0' * self.difficulty):
            block.proof += 1
            block.hash = block.calculate_hash()
        return block.proof

    def is_valid_proof(self, block):

        return block.hash.startswith('0' * self.difficulty)


if __name__ == "__main__":
    # Create a blockchain
    my_blockchain = Blockchain()

    # Adding blocks with data
    print("Mining block 1...")
    new_block = Block(index=1, previous_hash=my_blockchain.get_latest_block().hash,
                      timestamp=time.time(), data="First block after Genesis", proof=0)
    my_blockchain.add_block(new_block)

    print("Mining block 2...")
    new_block = Block(index=2, previous_hash=my_blockchain.get_latest_block().hash,
                      timestamp=time.time(), data="Second block", proof=0)
    my_blockchain.add_block(new_block)

    print("Mining block 3...")
    new_block = Block(index=3, previous_hash=my_blockchain.get_latest_block().hash,
                      timestamp=time.time(), data="Third block", proof=0)
    my_blockchain.add_block(new_block)

    # Check if the blockchain is valid
    print(f"Blockchain valid: {my_blockchain.is_chain_valid()}")

    # Display the blockchain
    for block in my_blockchain.chain:
        print(f"Block {block.index}: {block.hash}, Data: {block.data}")
