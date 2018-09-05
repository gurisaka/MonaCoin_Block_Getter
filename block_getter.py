import requests
import re
import json
import os
import glob
from pprint import pprint
import time

def fetch_block_file(block_number):
	pattern = "\[{'txid.*}\]\;"
	try:
		response = requests.get('https://bchain.info/MONA/block/' + str(block_number))
		print(response.status_code)
		matched_data = re.search(pattern, response.text)
		transactions_json = json.loads(matched_data.group().replace('\'','"')[:-1])

		if len(transactions_json) >= 20:
			fetch_large_block_file(block_number)

		else:
			with open(os.path.dirname(os.path.abspath(__file__)) + '/MONA_Blocks/' + str(block_number) + '_block.json','w') as file:
				json.dump(transactions_json,file,indent=4)

	except Exception as e :
		pprint(e)

def fetch_large_block_file(block_number):
	try:
		response = requests.get('https://mona.chainsight.info/api/block-index/' + str(block_number))
		block_hash = json.loads(response.text)['blockHash']

		response = requests.get('https://mona.chainsight.info/api/block/' + block_hash)
		json_data = json.loads(response.text)

		txids = json_data['tx']

		file_data = []

		for txid in txids:
			response = requests.get('https://mona.chainsight.info/api/tx/' + txid)
			time.sleep(0.3)
			transaction = json.loads(response.text)
			ts = int(transaction['time'])
			block = block_number
			sent = int(transaction['valueOut'] * 100000000)
			try:
				fees = -int(transaction['fees'] * 100000000)
			except:
				fees = -sent

			inputs = []
			outputs = []

			for vin in transaction['vin']:
				try:
					tx = vin['txid']
					addr = vin['addr']
					value = int(vin['value'] * 100000000)
					
					inputs.append({'tx':tx,'addr':addr,'value':value})

				except:
					coinbase = vin['coinbase']
					inputs.append({'coinbase':coinbase})

			for vout in transaction['vout']:
				if 'spentTxId' in vout.keys():
					addr = vout['scriptPubKey']['addresses'][0]
					spent = vout['spentTxId']
					value = int(float(vout['value']) * 100000000)

					outputs.append({'addr':addr,'spent':spent,'value':value})
				else:
					outputs.append({'value':0})
			file_data.append({'ts':ts,'in':inputs,'block':block,'sent':sent,'txid':txid,'fees':fees,'out':outputs})

		file = open(os.path.dirname(os.path.abspath(__file__)) + '/MONA_Blocks/' + str(block_number) + '_block.json','w')
		json.dump(file_data,file,indent=4)
		file.close()
		print('Completed ' + str(block_number) + ' !')

	except Exception as e:
		pprint(e)

def check_lack_blocks():
	file_paths = glob.glob(os.path.dirname(os.path.abspath(__file__)) + '/MONA_Blocks/*.json')
	block_numbers = [int(os.path.basename(os.path.abspath(file_path)).split('_')[0]) for file_path in file_paths]
	min_block_number = min(block_numbers)
	max_block_number = max(block_numbers)

	lack_block_numbers = []

	for n in range(min_block_number,max_block_number):
		if n not in block_numbers:
			lack_block_numbers.append(n)

	return lack_block_numbers

def merge_blocks_file(output_file_path):
	file_paths = glob.glob(os.path.dirname(os.path.abspath(__file__)) + '/MONA_Blocks/*.json')

	merged_json = {}
	for file_path in file_paths:
		with open(file_path,'r') as file:
			json_data =  json.load(file)

		for tx in json_data:
			block_number = tx['block']
			txid = tx['txid']

			if block_number not in merged_json.keys():
				merged_json[block_number] = {}

			merged_json[block_number][txid] = tx

	file = open(output_file_path,'w')
	json.dump(merged_json,file,indent=4)
	file.close()

def make_transactions_file(input_file_path,output_file_path):
	with open(input_file_path,'r') as file:
		blocks_json = json.load(file)

	transactions = {}

	for block_number in blocks_json.keys():
		for txid in blocks_json[block_number].keys():
			transactions[txid] = blocks_json[block_number][txid]

	file = open(output_file_path,'w')
	json.dump(transactions,file,indent=4)
	file.close()

