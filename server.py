from flask import Flask, request, jsonify
from blockchain import BlockChain

web_app = Flask(__name__)

blockchain = BlockChain()

node_address = None

@web_app.route('/post-transaction', methods=['POST'])
def post_transaction():
    """
    Input:
    {
        "sender": "address_1"
        "receiver": "address_2",
        "amount": 3
    }
    """
    transaction_data = request.get_json()

    blockchain.create_new_transaction(**transaction_data)

    response = {
        'message': 'Transaction has been submitted successfully'
    }

    return jsonify(response), 201


@web_app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine_block(node_address)
    response = {
        'message': 'Successfully Mined the new Block',
        'block_data': block
    }
    return jsonify(response)


@web_app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.serialize_chain()
    }
    return jsonify(response)


@web_app.route('/register-node', methods=['POST'])
def register_node():

    node_data = request.get_json()

    blockchain.add_node(node_data.get('address'))

    response = {
        'message': 'New node has been added',
        'node_count': len(blockchain.nodes),
        'nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@web_app.route('/sync-chain', methods=['GET'])
def consensus():

    def get_neighbour_chains():
        neighbour_chains = []
        for node_address in blockchain.nodes:
            response = requests.get(node_address + url_for('get_chain')).json()
            chain = response['chain']
            neighbour_chains.web_append(chain)
        return neighbour_chains

    neighbour_chains = get_neighbour_chains()
    if not neighbour_chains:
        return jsonify({'message': 'No neighbour chain is available'})

    longest_chain = max(neighbour_chains, key=len)

    if len(blockchain.chain) >= len(longest_chain):  
        response = {
            'message': 'Chain is already up to date',
            'chain': blockchain.serialize_chain
        }
    else:  
	response = {
            'message': 'Chain was replaced',
            'chain': blockchain.get_serialized_chain
        }
	new_chain = [blockchain.get_block_object_from_block_data(block) for block in longest_chain]
        if blockchain.is_valid_chain(new_chain):
		blockchain.chain = new_chain 	
	else: 
        	response = {
            		'message': 'Chain is already up to date',
            		'chain': blockchain.serialize_chain
        	}

    return jsonify(response)

if __name__ == "__main__":
	from argparse import ArgumentParser
	parser = ArgumentParser()
	parser.add_argument('-H', '--host', default="127.0.0.1")
	parser.add_argument('-p', '--port', default=5000, type=int)
	args = parser.parse_args()
	node_address = "http://"+args.host+":"+str(args.port)
	web_app.run(host = args.host, port = args.port, debug = True)

