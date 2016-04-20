#!/usr/bin/env python2.7

import getopt
import logging
import os
import socket
import sys
import time

# Constants

ADDRESS  =  '127.0.0.1'
DOMAIN = 'localhost'
PATH = ''
PORT     = 80
PROGRAM  = os.path.basename(sys.argv[0])
LOGLEVEL = logging.INFO
REQUESTS = 1
PROCESSES = 1
URL = 'localhost'

# Utility Functions

def usage(exit_code=0):
    print >>sys.stderr, '''Usage: {program} [-v] ADDRESS PORT

Options:

    -h       Show this help message
    -v       Set logging to DEBUG level
    -r REQUESTS     Number of requests per process (default is 1)
    -p PROCESSES    Number of processes (default is 1)
'''.format(port=PORT, program=PROGRAM)
    sys.exit(exit_code)

# TCPClient Class

class TCPClient(object):

    def __init__(self, address=ADDRESS, port=PORT):
        ''' Construct TCPClient object with the specified address and port '''
        self.logger  = logging.getLogger()                              # Grab logging instance
        self.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Allocate TCP socket
        self.address = address                                          # Store address to listen on
        self.port    = port                                             # Store port to lisen on

    def handle(self):
        ''' Handle connection '''
        self.logger.debug('Handle')
        raise NotImplementedError

    def run(self):
        ''' Run client by connecting to specified address and port and then
        executing the handle method '''
        try:
            # Connect to server with specified address and port, create file object
            self.socket.connect((self.address, self.port))
            self.stream = self.socket.makefile('w+')
        except socket.error as e:
            self.logger.error('Could not connect to {}:{}: {}'.format(self.address, self.port, e))
            sys.exit(1)

        self.logger.debug('Connected to {}:{}...'.format(self.address, self.port))

        # Run handle method and then the finish method
        try:
            self.handle()
        except Exception as e:
            self.logger.exception('Exception: {}', e)
        finally:
            self.finish()

    def finish(self):
        ''' Finish connection '''
        self.logger.debug('Finish')
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass    # Ignore socket errors
        finally:
            self.socket.close()

class HTTPClient(TCPClient): #inherit from TCPClient
    def __init__(self, address, port, path):
        TCPClient.__init__(self, address, port)
        self.path = path
        self.host = address

    def handle(self): #don't need to redefine run or finish
        self.logger.debug('Handle')

        #Send request
        self.logger.debug('Sending request...')
        self.stream.write('GET {} HTTP/1.0\r\n'.format(self.path)) #must end HTTP with \r\n
        self.stream.write('Host: {}\r\n'.format(self.host))
        self.stream.write('\r\n') #to notify that the request is ending

        self.stream.flush()

        # Receive response
        self.logger.debug('Receiving response...')
        data = self.stream.readline()
        while data:
            sys.stdout.write(data)
            data = self.stream.readline()


# Main Execution

if __name__ == '__main__':
    # Parse command-line arguments
    try:
        options, arguments = getopt.getopt(sys.argv[1:], "hvr:p:")
    except getopt.GetoptError as e:
        usage(1)

    for option, value in options:
        if option == '-h':
            usage(0)
        if option == '-v':
            LOGLEVEL = logging.DEBUG
        elif option == '-r':
            REQUESTS = int(value)
        elif option == '-p':
            PROCESSES = int(value)
        else:
            usage(1)

    if len(arguments) >= 1:
        URL = arguments[0]
    if len(arguments) >= 2:
        PORT    = int(arguments[1])

    # Set logging level
    logging.basicConfig(
        level   = LOGLEVEL,
        format  = '[%(asctime)s] %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
    )

    # Parse URL 
    DOMAIN = URL.split('://')[-1] #gets rid of protocol part (http)
   
    if '/' not in DOMAIN:
        PATH  = '/'
 
    else:
        PATH = '/' + DOMAIN.split('/',1)[-1]
        if '?' in PATH:
            PATH = PATH.split('?')[0]
        DOMAIN = DOMAIN.split('/')[0]

    if ':' in DOMAIN: 
        PORT = int(DOMAIN.split(':')[-1])
        DOMAIN = DOMAIN.split(':')[0]
    
    logging.debug('URL: {}'.format(URL))
    logging.debug('HOST: {}'.format(DOMAIN))
    logging.debug('PORT: {}'.format(PORT))
    logging.debug('PATH: {}'.format(PATH))

    # Lookup host address
    try:
        ADDRESS = socket.gethostbyname(DOMAIN) # IP address number of DOMAIN
    except socket.gaierror as e:
        logging.error('Unable to lookup {}: {}'.format(ADDRESS, e))
        sys.exit(1)

    # Instantiate and run client
    for process in range(PROCESSES):
        try:
            pid = os.fork()
        except OSError as e:
            error('Forking failed: {}'.format(e))
        
        #Child process
        totaltime=0
        if pid == 0: 
            for request in range(REQUESTS):
                starttime=time.time()
                client = HTTPClient(DOMAIN,PORT,PATH)
                try:
                    client.run()
                except KeyboardInterrupt:
                    sys.exit(0)
                endtime=time.time()
                time = endtime - starttime
                totaltime = time + totaltime
                logging.debug('{} | Elapsed time: {} seconds'.format(os.getpid(), time))

            logging.debug('{} | Average Elapsed time: {} seconds'.format(os.getpid(), totaltime/REQUESTS))

        #Parent process
        else: 
            pid, status = os.wait()
# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
