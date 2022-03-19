from datetime import datetime
import hashlib

class Block:
  def __init__(self, data, previous_hash):
    self.hash = hashlib.sha256()
    self.previous_hash = previous_hash
    self.nonce = 0
    self.timestamp = datetime.now()
    self.data = data

  def mine(self, difficulty):
    self.hash.update(str(self).encode('utf-8'))
    while self.is_valid_hash(self.hash.hexdigest(), difficulty) is False:
      self.nonce += 1
      self.hash = hashlib.sha256()
      self.hash.update(str(self).encode('utf-8'))

  def is_valid_hash(self, hash, difficulty):
    return hash.startswith('0' * difficulty)

  def __str__(self):
    return f"-{self.data}-{self.nonce}-{self.previous_hash.hexdigest()}-{self.timestamp}"

class BlockChain:
  def __init__(self, difficulty):
    self.difficulty = difficulty
    self.blocks = []
    self.pool = []
    self.create_genesis_block()

  def create_genesis_block(self):
    h = hashlib.sha256()
    h.update(''.encode('utf-8'))
    origin = Block('Genesis', h)
    origin.mine(self.difficulty)
    self.blocks.append(origin)

  def proof_of_work(self, block: Block):
    hash = hashlib.sha256()
    hash.update(str(block).encode('utf-8'))

    return block.hash.hexdigest() == hash.hexdigest() and block.is_valid_hash(hash.hexdigest(), self.difficulty) and block.previous_hash == self.blocks[-1].hash

  def add_to_chain(self, block: Block):
    if self.proof_of_work(block):
      self.blocks.append(block)

  def add_to_pool(self, data):
    self.pool.append(data)

  def mine(self):
    if len(self.pool) > 0:
      data = self.pool.pop()
      block = Block(data, self.blocks[-1].hash)
      block.mine(self.difficulty)
      self.add_to_chain(block)
      self.print_block(block)
      

  def print_block(self, block):
    print("\n\n===========================================================")
    print(f"Hash: {block.hash.hexdigest()}")
    print(f"Previous hash: {block.previous_hash.hexdigest()}")
    print(f"Nonce: {block.nonce}")
    print(f"Data: {block.data}")
    print(f"Timestamp: {block.timestamp}")
    print("\n\n===========================================================")

# Difficulty = 4 (4 zeros)
chain = BlockChain(4)

for i in range(5):
  chain.add_to_pool(str(i))
  chain.mine()
  
