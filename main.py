from block_getter import *
from pprint import pprint
import sys
import time
import os

if __name__ == '__main__':
	try:
		start_block_height = int(sys.argv[1])
		dig_block_height = int(sys.argv[2])


		for n in range(dig_block_height):
			fetch_block_file(start_block_height - n)

			time.sleep(0.3)

		pprint(check_lack_blocks())
	except:
		pass

	merge_blocks_file(os.path.dirname(os.path.abspath(__file__)) + '/Outputs/MONA_Blocks.json')
	make_transactions_file(os.path.dirname(os.path.abspath(__file__)) + '/Outputs/MONA_Blocks.json',os.path.dirname(os.path.abspath(__file__)) + '/Outputs/MONA_Transactions.json')