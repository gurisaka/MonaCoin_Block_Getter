from block_getter import *
from pprint import pprint
import sys
import time
import os

def get_head_to_tail_blocks(tail_block_height, head_block_height, api_interval):
	wanted_block_numbers = [block_number for block_number in range(tail_block_height, head_block_height + 1)]

	lack_block_numbers = check_lack_blocks(wanted_block_numbers)
	task_size = len(lack_block_numbers)

	failed_times = 0

	while True:
		for lack_block_number in lack_block_numbers[:]:
			if fetch_block_file(lack_block_number) == True:
				lack_block_numbers.remove(lack_block_number)
				sys.stdout.write('\rTask ' + str(task_size - len(lack_block_numbers)) + '/' + str(task_size))
				sys.stdout.flush()
			time.sleep(api_interval)

		if len(lack_block_numbers) == 0:
			break
		else:
			failed_times += 1

			if failed_times > 10:
				return False

	merge_blocks_file(os.path.dirname(os.path.abspath(__file__)) + '/Outputs/MONA_Blocks.json')
	make_transactions_file(os.path.dirname(os.path.abspath(__file__)) + '/Outputs/MONA_Blocks.json', os.path.dirname(os.path.abspath(__file__)) + '/Outputs/MONA_Transactions.json')

	print('')

	return True


if __name__ == '__main__':
	tail_block_height = int(sys.argv[1])
	head_block_height = 0

	if len(sys.argv) == 1:
		merge_blocks_file(os.path.dirname(os.path.abspath(__file__)) + '/Outputs/MONA_Blocks.json')
		make_transactions_file(os.path.dirname(os.path.abspath(__file__)) + '/Outputs/MONA_Blocks.json', os.path.dirname(os.path.abspath(__file__)) + '/Outputs/MONA_Transactions.json')

		sys.exit(0)

	if len(sys.argv) == 3:
		# head to tail
		head_block_height = int(sys.argv[2])
		get_head_to_tail_blocks(tail_block_height, head_block_height, 0.3)
		sys.exit(0)

	else:
		# highest to tail
		while True:
			head_block_height = get_max_height()

			if head_block_height == -1:
				head_block_height = tail_block_height
			get_head_to_tail_blocks(tail_block_height, head_block_height, 0.3)
			time.sleep(10)

		sys.exit(-1)