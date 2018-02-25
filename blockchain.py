import hashlib
import time
from block import Block

class BlockChain:

	def __init__(self):
		self.chain=[]
		self.uncommited_transactions = []
		self.nodes = set()	
		self.create_genesis_block()
	
	def create_genesis_block(self):
		return self.create_new_block("0",0)
	
	def create_new_block(self,prev_hash,proof):
		new_block = Block(prev_hash,self.uncommited_transactions,proof,len(self.chain))
		self.reset_transactions()
		self.chain.append(new_block)
		return new_block

	def create_new_transaction(self,sender,receiver,amount):
		self.uncommited_transactions.append({ "sender": sender, "receiver": receiver, "amount": amount})
		#return True

	def last_block(self):
		return self.chain[-1]

	def do_proof_of_work(self,prev_proof):
		# >>>>> Algorithm
		proof = prev_proof + 1 
		while (hashlib.sha256(str(proof).encode()).hexdigest()[0] == "0"):
			proof += 1
		# >>>>> Algorithm
		return proof

	def reset_transactions(self):
		self.uncommited_transactions = []

	def add_node(self,address):
		self.nodes.add(address)

	def is_valid_chain(self,chain): 
		last = len(chain)-1
		while last>0:
			if not BlockChain.is_valid_block(chain[last-1],chain[last]):
				return False
		return True

    	def mine_block(self, miner_address):
        	self.create_new_transaction(sender=None, receiver=miner_address, amount=1)
        	prev_block = self.last_block()
        	prev_proof = prev_block.proof
        	proof = self.do_proof_of_work(prev_proof)
        	prev_hash = prev_block.block_hash()
        	block = self.create_new_block(prev_hash, proof)
        	return vars(block)

	def serialize_chain(self):
        	return [vars(block) for block in self.chain]

	@staticmethod
	def is_valid_block(prev_block,block):	
		if prev_block.index+1 == block.index and prev_block.block_hash() == block.prev_hash and BlockChain.is_proof_correct(prev_block, block.proof) and prev_block.timestamp >= block.timestamp:
			return False
		return True

	@staticmethod
	def convert_from_json_to_block(json_data):
		return Block(json_data["prev_hash"],json_data["transactions"],json_data["proof"],json_data["index"])
		#return True

