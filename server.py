#!/usr/bin/env python
import random
import socket
import time


##class Cse491server(object):
##
##    # initiliaze server then listen for client
##    def __init__(self):
##        self.sock = socket.socket()         # Create a socket object
##        self.host = socket.getfqdn() # Get local machine name
##        self.port = random.randint(8000, 9999)
##        self.sock.bind((self.host, self.port))        # Bind to the port
##
##        print 'Starting server on', self.host, self.port
##        print 'The Web server URL for this would be http://%s:%d/' % (self.host, self.port)
##
##        self.sock.listen(5)     # Now wait for client connection.
##
##
##    def wait_for_connect(self):
##        # Establish connection with client.    
##        self.conn, (self.client_host, self.client_port) = self.sock.accept()
##        
##        print 'Got connection from', self.client_host, self.client_port
##
##
##    # send response to client
##    def send_response(self, msg):
##        self.conn.send(msg)
##
##                
##    # close socket connection
##    def close_conn(self):
##        self.conn.close()
##        print "Disconnected from " + self.client_host

        
def main():
    #server = Cse491server()
    sock = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    sock.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    sock.listen(5)     # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        conn, (client_host, client_port) = sock.accept()
        
        print 'Got connection from', client_host, client_port

        handle_connection(conn)

def handle_connection(conn):
    req = conn.recv(1000)
    req_type = req.split()[0]

    if req_type == "GET":
        url = req.split()[1]

        if url == "/":
            handle_connection_default(conn)
        elif url == "/content":
            handle_connection_content(conn)
        elif url == "/image":
            handle_connection_image(conn)
        elif url == "/file":
            handle_connection_file(conn)
        else:
            handle_connection_failed(conn)
    elif req_type == "POST":
        handle_connection_post(conn)
    else:
        print "Invalid request, yo."

def handle_connection_default(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Hello, world.</h1>')
    conn.send('<a href="/content">Content</a><br>')
    conn.send('<a href="/file">File</a><br>')
    conn.send('<a href="/image">Image</a><br>')
    conn.send('This is koppmana\'s Web server.')
    conn.close()

def handle_connection_content(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Fulfilling content request</h1>')
    conn.send('This is koppmana\'s Web server.')
    conn.close()

def handle_connection_file(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Fullfilling file request</h1>')
    conn.send('This is koppmana\'s Web server.')
    conn.close()

def handle_connection_image(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Fullfilling image request</h1>')
    conn.send('This is koppmana\'s Web server.')
    conn.close()

def handle_connection_fail(conn):
    conn.send('HTTP/1.0 400 BAD\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Bad request</h1>')
    conn.send('This is koppmana\'s Web server.')
    conn.close()

def handle_post_connection(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('Hello, World.')
    conn.close()

if __name__ == '__main__':
    main()
