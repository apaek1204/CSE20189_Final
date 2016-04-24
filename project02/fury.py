#!/usr/bin/env python2.7

import sys
import work_queue
import string
import json
import os

#Constants

SOURCES = ('hulk.py', 'hashes.txt')
PORT = 9123
ALPHABET = string.ascii_lowercase + string.digits
# Main Execution

if __name__ == '__main__':
	# Create a master
	  # 1. Random port between 9000 - 9999
	  # 2. Project name of fury-samuel
	  # 3. Catalog mode enabled
	queue = work_queue.WorkQueue(PORT, name = 'fury-mchen6apaek1', catalog=True)
	queue.specify_log('fury.log') #Specify Work Queue log location

	# Create task list

	# Check passwords for length of <6 
	for num in range(5):
		command = './hulk.py -l {}'.format(num)
		task = work_queue.Task(command)

		# Add source files (transfer files to workers)
		for source in SOURCES: 
			task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT)
		# Submit tasks
		queue.submit(task) 

	# Checking passwords of length 6
	for prefix in (ALPHABET):
		command = './hulk.py -l 5 -p {}'.format(prefix) 
		task = work_queue.Task(command)

		# Add source files (transfer files to workers)
		for source in SOURCES: 
			task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT)
		# Submit tasks
		queue.submit(task) 

	#length 7
	for prefix in itertools.product(ALPHABET,repeat=2):
		command = './hulk.py -l 5 -p {}'.format(prefix) 
		task = work_queue.Task(command)

		# Add source files (transfer files to workers)
		for source in SOURCES: 
			task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT)
		# Submit tasks
		queue.submit(task) 

	# Checking passwords of length 8
	for prefix in itertools.product(ALPHABET,repeat=3):
		command = './hulk.py -l 5 -p {}'.format(prefix) 
		task = work_queue.Task(command)

		# Add source files (transfer files to workers)
		for source in SOURCES: 
			task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT)
		# Submit tasks
		queue.submit(task) 


	JOURNAL={}
	# Until the Master queue 
	while not queue.empty():
		task = queue.wait() # wait on task
		
		if task and task.return_status == 0: #check if task is valid 
			sys.stdout.write(task.output) #output of workers should be passwords
			JOURNAL[task.command] = task.output.split()
			if command in JOURNAL:
				print >>sys.stderr, 'Already did',command
			else:

				with open('journal.json.new','w') as stream:
					json.dump(JOURNAL, stream)
				os.rename('journal.json.new','journal.json')


#-----------------------------------------------------------------
# source env.sh
# ./mini-fury.py

# work queue does not start the worker; you must do a manual worker
	# work_queue_worker -d all -N fury-mchen6apaek1

# condor _submit_workers -N fury-mchen6apaek1 200 # 200 friends
