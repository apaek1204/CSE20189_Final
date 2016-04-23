#!/usr/bin/env python2.7

import getopt
import os
import sys
import string
import hashlib
import random
import itertools

# Constants

PROGRAM = os.path.basename(sys.argv[0])
ALPHABET = string.ascii_lowercase + string.digits #only lower case and digits
PREFIX = ''
LENGTH = 8
HASHES = './hashes.txt' # Path to hashes file

# Functions

def usage(exit_code=0):
	print >>sys.stderr, '''Usage: {program} [-a ALPHABET -l LENGTH -s HASHES -p PREFIX]

	Options:
		-a ALPHABET 	Alphabet used for passwords
		-l LENGTH 	Length for passwords
		-s HASHES 	Path to file containing hashes
		-p PREFIX 	Prefix to use for each candidate password'''.format(program=PROGRAM)
	sys.exit(exit_code)

def md5sum(s):
	return hashlib.md5(s).hexdigest()

# Main Execution

if __name__ == '__main__':

	# Parse command line arguments
	try:
		options, arguments = getopt.getopt(sys.argv[1:], "a:l:s:p:h")
	except getopt.GetoptError as e:
		usage(1)

	for option, value in options:
		if option == '-h':
			usage(0)
		if option == '-a':
			ALPHABET = value
		elif option == '-l':
			LENGTH = int(value)
		elif option == '-s':
			HASHES = value
		elif option == '-p':
			PREFIX = value
		else:
			usage(1)

	
	# Hashes that need to be checked
	hashes = set([l.strip() for l in open(HASHES)])

	for candidate in itertools.product(ALPHABET, repeat=LENGTH): 
		# itertools creates a tupple of each permutation of given ALPHABET
		candidate = ''.join(candidate)
		CANDIDATE=PREFIX+candidate
		checksum = md5sum(CANDIDATE)
		
		# Check if the candidate matches the hashes 
		if checksum in hashes:
			print CANDIDATE
