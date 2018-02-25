import hashlib
import time

class Block:
	
	def __init__(self,prev_hash,transactions,proof,index, timestamp = time.time()):
		self.prev_hash = prev_hash
		self.transactions = transactions
		self.timestamp = timestamp
		self.index = index
		self.proof = proof
	
	def block_hash(self):
		return hashlib.sha256((str(self.prev_hash)+str(self.transactions)+str(self.proof)+str(self.index)+str(self.timestamp)).encode()).hexdigest()




