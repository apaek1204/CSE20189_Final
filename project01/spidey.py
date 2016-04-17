#!/usr/bin/env python2.7

import getopt
import logging
import os
import socket
import sys

# Constants

ADDRESS  = '0.0.0.0'
PORT     = 9234
BACKLOG  = 0
LOGLEVEL = logging.INFO
PROGRAM  = os.path.basename(sys.argv[0])
DOCROOT = '.'
FORKING = False

# Utility Functions

def usage(exit_code=0):
    print >>sys.stderr, '''Usage: {program} [-d DOCROOT -p PORT -f -v] 

Options:

    -h       Show this help message
    -f       Enable forking mode
    -v       Set logging to DEBUG level

    -d DOCROOT Set root directory (default is current directorY)
    -p PORT  TCP Port to listen to (default is {port})
'''.format(port=PORT, program=PROGRAM)
    sys.exit(exit_code)

# BaseHandler Class

class BaseHandler(object):

    def __init__(self, fd, address):
        ''' Construct handler from file descriptor and remote client address '''
        self.logger  = logging.getLogger()        # Grab logging instance
        self.socket  = fd                         # Store socket file descriptor
        self.address = '{}:{}'.format(*address)   # Store address
        self.stream  = self.socket.makefile('w+') # Open file object from file descriptor

        self.debug('Connect')

    def debug(self, message, *args):
        ''' Convenience debugging function '''
        message = message.format(*args)
        self.logger.debug('{} | {}'.format(self.address, message))

    def info(self, message, *args):
        ''' Convenience information function '''
        message = message.format(*args)
        self.logger.info('{} | {}'.format(self.address, message))

    def warn(self, message, *args):
        ''' Convenience warning function '''
        message = message.format(*args)
        self.logger.warn('{} | {}'.format(self.address, message))

    def error(self, message, *args):
        ''' Convenience error function '''
        message = message.format(*args)
        self.logger.error('{} | {}'.format(self.address, message))

    def exception(self, message, *args):
        ''' Convenience exception function '''
        message = message.format(*args)
        self.logger.error('{} | {}'.format(self.address, message))

    def handle(self):
        ''' Handle connection '''
        self.debug('Handle')
        raise NotImplementedError

    def finish(self):
        ''' Finish connection by flushing stream, shutting down socket, and
        then closing it '''
        self.debug('Finish')
        try:
            self.stream.flush()
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error as e:
            pass    # Ignore socket errors
        finally:
            self.socket.close()



#HTTPHandler

class HTTPHandler(BaseHandler):
    def handle(self): #need to overwrite handle

        # read lines
        data = self.stream.readline().rstrip()

        #done when there is an empty line
        while data:
            sys.stdou.write(data)
            data = self.stream.readline().rstrip()

        self.stream.write('HTTP/1.0 200 OK\r\n')
        self.stream.write('Content-Type: text/html\r\n')
        self.stream.write('\r\n')

# EchoHandler Class

class EchoHandler(BaseHandler):
    def handle(self):
        ''' Handle connection by reading data and then writing it back until EOF '''
        self.debug('Handle')

        try:
            data = self.stream.readline()
            while data:
                self.debug('Read {}', data)
                self.stream.write(data)
                self.stream.flush()
                data = self.stream.readline()
        except socket.error:
            pass    # Ignore socket errors

# TCPServer Class

class TCPServer(object):

    def __init__(self, address=ADDRESS, port=PORT, handler=EchoHandler):
        ''' Construct TCPServer object with the specified address, port, and
        handler '''
        self.logger  = logging.getLogger()                              # Grab logging instance
        self.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Allocate TCP socket
        self.address = address                                          # Store address to listen on
        self.port    = port                                             # Store port to lisen on
        self.handler = handler                                          # Store handler for incoming connections

    def run(self):
        ''' Run TCP Server on specified address and port by calling the
        specified handler on each incoming connection '''
        try:
            # Bind socket to address and port and then listen
            self.socket.bind((self.address, self.port))
            self.socket.listen(BACKLOG)
        except socket.error as e:
            self.logger.error('Could not listen on {}:{}: {}'.format(self.address, self.port, e))
            sys.exit(1)

        self.logger.info('Listening on {}:{}...'.format(self.address, self.port))

        while True:
            # Accept incoming connection
            client, address = self.socket.accept()
            self.logger.debug('Accepted connection from {}:{}'.format(*address))

            # Instantiate handler, handle connection, finish connection
            try:
                handler = self.handler(client, address)
                handler.handle()
            except Exception as e:
                handler.exception('Exception: {}', e)
            finally:
                handler.finish()

# Main Execution

if __name__ == '__main__':
    # Parse command-line arguments
    try:
        options, arguments = getopt.getopt(sys.argv[1:], "hp:d:fv")
    except getopt.GetoptError as e:
        usage(1)

    for option, value in options:
        if option == '-h':
            usage(0)
        if option == '-p':
            PORT = int(value)
        elif option == '-d':
            DOCROOT = value
        elif option == 'f':
            FORKING = True
        elif option == '-v':
            LOGLEVEL = logging.DEBUG
        else:
            usage(1)

    # Set logging level
    logging.basicConfig(
        level   = LOGLEVEL,
        format  = '[%(asctime)s] %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
    )

    # Instantiate and run server
    server = TCPServer(port=PORT)

    try:
        server.run()
    except KeyboardInterrupt:
        sys.exit(0)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
