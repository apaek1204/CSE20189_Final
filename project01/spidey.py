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
    def __init__(self, fd, address, docroot = None):
        BaseHandler.__init__(self, fd, address)
        self.docroot = DOCROOT

    def _parse_request(self):
        try:
            # read lines
            data = self.stream.readline().rstrip()
            request = data.split(' ')
            REQUEST_METHOD = request[0]
            REQUEST_URI = request[1]
            parse_request_uri = REQUEST_URI.split('/')
            QUERY_STRING = ''########INCOMPLETE 
            #done when there is an empty line
            while data:
                self.debug('Read {}', data)
                #sys.stdout.write(data)
                data = self.stream.readline().rstrip()
                temp = data.split(':')
                if temp[0] == 'Host':
                    os.environ['HTTP_HOST']=temp[1]
                    os.environ['HTTP_REFERER']='http://' + temp[1] + parse_request_uri[1]
                elif temp[0] == 'Connection':
                    os.environ['HTTP_CONNECTION']=temp[1]
                elif temp[0] == 'Accept':
                    os.environ['HTTP_ACCEPT']=temp[1]
                elif temp[0] == 'Upgrade-Insecure-Requests':
                    os.environ['HTTP_UPGRADE_INSECURE_REQUESTS']=temp[1]
                elif temp[0] == 'User-Agent':
                    os.environ['HTTP_USER_AGENT']=temp[1]
                elif temp[0] == 'Accept-Encoding':
                    os.environ['HTTP_ACCEPT_ENCODING']=temp[1]
                elif temp[0] == 'Accept-Language':
                    os.environ['HTTP_ACCEPT_LANGUAGE']=temp[1]
                
        except socket.error:
            pass #ignore socket errors


    def startDoc(self, uripath):
        #check if the uripath starts with docroot
        #split both uripath and docroot into lists
        docrootlist=self.docroot.split('/')
        uripathlist = uripath.split('/')
        #check each element to compare
        for i in range(len(docrootlist)):
            if docrootlist[i] != uripathlist[i]:
                #if fails, then return false
                return False
        #if reaches end, return true
        return True

    def _handle_error(self, number):
        if number == 404:
            pass 
            # Display 404 error page
        if number == 403: 
            pass 
            # Display 403 error page

    def _handle_script(self):
        #NEED to do
        pass
    def _handle_file(self):
        # Determine the file's mimetype 
        mimetype, _ = mimetypes.guess_type(self.uripath)
        if mimetype is None:
            mimetype = 'application/octet-stream'

        # Write the http response status to socket
        

            self.stream.write('{}\r\n'.format(response))
            self.stream.write('Content-Type: {}\r\n'.format(mimetype))
            self.stream.write('\r\n')
            urifilef = open(self.urifile,'rb')
            try:
                byte=urifilef.read(1)
                while byte!= "":
                    self.stream.write(byte)
                    byte=f.read(1)
            except:
                pass
            finally:
                urifilef.close()

    def _handle_directory(self):
        #write HTML code
        pass
    



    def handle(self): #need to overwrite handle from BasHandler
        self.debug('Handle')
        
        #Pars HTTP request and headers
        self._parse_request()

        #Build uripath by normalizing REQUEST_URI
        self.uripath = os.path.normpath(self.docroot + os.environ['REQUEST_URI'])

        if not self.uripath or not self.startDoc(self.uripath):
            self._handle_error(404) #404 error
            #Need to write func
        
        elif os.path.isfile(self.uripath) and os.access(self.uripath, os.X_OK):
            self._handle_script() #CGI script 
            ##need to write func

        elif os.path.isfile(self.uripath) and os.access(self.uripath, os.R_OK):
            self._handle_file() #Static file
            #need to write func

        elif os.path.isdir(self.uripath) and os.acess(self.uripath, os.R_OK):
            self._handle_directory() #Directory listing
            #need to write func

        else:
            self._handle_error(403) #403 error

# EchoHandler Class
'''
class EchoHandler(BaseHandler):
    def handle(self):
        # Handle connection by reading data and then writing it back until EOF 
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
'''
# TCPServer Class

class TCPServer(object):

    def __init__(self, address=ADDRESS, port=PORT, handler=HTTPHandler):
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
