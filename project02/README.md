Project 02: Distributed Computing
=================================
Group Members
-------------

- Mimi Chen (mchen6)
- Andrew Paek (apaek1)

1. Describe the implementation of hulk.py. How does it crack passwords?
- `hulk.py` uses **itertools.product** to create every permutation of the given alphabet of a given length. Then it uses the crypographic hash function **MD5** to change it to a hash value consisting of lower case alphabets and numbers. These hash values are then compared to the hashes found in the hashes file. If there is a match, then that means the alpha-numeric combination from the permutation created is a password.
- To test `hulk.py`, we ran it on the hashes.txt file on passwords of lengths 1 to 4, and also testing for combinations with a specified prefix. Only passwords of lengths from 1 to 4 were tested since the larger the length, the number of permutations is greater, so the longer it took for the program to run.

2. Describe the implementation of fury.py:
- To utilize `hulk.py` to crack passwords, it creates a master with a name `fury-mchen6apaek1` with the command:
		queue = work_queue.WorkQueue(PORT, name = 'fury-mchen6apaek1', catalog=True)

A task list is also created by using `work_queue.Task(command)` on hulk.py. Source files are added and transferred to the workers by doing `task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT))`. The tasks then are submitted with `queue.submit(task)`. The only difference for checking passwords of lengths less than 6, length of 6, length of 7, and length of 8 are the prefixes used in `command`. Passwords for lengths less than 6 did not have prefixes. Passwords of length of 6 had one prefix, which we called by just doing a for loop over the ALPHABET (`string.ascii_lowercase + string.digits`). Passwords for length of 7 had 2 prefixes, which used the function `itertools.product(ALPHABET,repeat=2)` to create the 2 prefixes in an organized, systematic way. Passwords for length of 8 had 3 prefixes, which used the function `itertools.product(ALPHABET, repeat=3)` to create the 3 prefixes in an organized, systematic way.
- To divide up the work among the different workers, multiple tasks were created in the task list. 
- To keep track of what has been attempted, it the task is not empty and the task returns an exit status of 0, then the task output is printed. We also used a journal to keep track of our results and skip already completed tasks. before running fury.py, it loads the journal so that the program can be stopped and started any time. 
- To recover from failures, we used a journal to keep track of what tasks have been ran by saving the command for the task and its output to the journal. When there is a failure, the fury program can be restarted from where it left off because of the journal.
- To test `fury.py`, we began by calling 100 workers with ` condor _submit_workers -N fury-mchen6apaek1 100`. Upon completion of tasks, passwords that were found were outputted. Since this worked, we increased the total number of workers to 1000.

3. From your experience in this project and recalling your Discrete Math knowledge, what would make a password more difficult to brute-force: more complex alphabet or longer password? Explain.
- A longer password would be more difficult to brute-force than having a more complex alphabet because to calculate the number of password combinations, you would exponentiate the number of alphabet combos by the length of the password. A larger exponent will greatly increase the number of passwords than having a larger base number.
