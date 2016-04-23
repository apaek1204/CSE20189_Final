#!/usr/bin/env python2.7

import sys
import work_queue

#Constants

LENGTH = int(sys.argv[1])
ATTEMPTS = int(sys.argv[2])
HASHES = sys.argv[3]
TASKS = int(sys.argv[4])
SOURCES = ('mini-hulk.py', HASHES)
PORT = 9123


# Main Execution

if __name__ == '__main__':
	# Create a master and the task list
	queue = work_queue.WorkQueue(PORT, name = 'fury-samuel', catalog=True)
	queue.specify_log('mini-fury.log')

	for _ in range(TASKS):
		command = './mini-hulk.py {} {} {}'.format(LENGTH, ATTEMPTS, HASHES)
		task = work_queue.Task(command)

		for source in SOURCES: 
			task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT)
		queue.submit(task) 

	while not queue.empty():
		task = queue.wait()
		if task and task.return_status == 0: #check if task is valid 
			sys.stdout.write(task.output) #output of workers should be passwords

# source env.sh
# run mini-fury.py
# work queue does not start the worker; you must do a manual worker
	# work_queue_worker -d all -N fury-samuel 
