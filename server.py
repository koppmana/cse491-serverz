#!/usr/bin/env python
import random
import socket
import time
import urlparse

def main():
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
    req_info = conn.recv(1000)
    req = req_info.split(" ")
    url_parse = urlparse.urlparse(req[1])
    req_type = req[0]
    path = url_parse.path

    if req_type == "GET":
        if path == "/":
            handle_connection_default(conn)
        elif path == "/content":
            handle_connection_content(conn)
        elif path == "/image":
            handle_connection_image(conn)
        elif path == "/file":
            handle_connection_file(conn)
        elif path == "/form":
            handle_form(conn, url_parse)
        elif path == "/submit": 
            handle_submit(conn, url_parse, req_info, req_type)
        else:
            handle_connection_failed(conn)
    elif req_type == "POST":
        if path == "/":
            handle_connection_post(conn)
        elif path == "/submit":
            handle_submit(conn, url_parse, req_info, req_type)

    conn.close()

def handle_connection_default(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Hello, world.</h1>')
    conn.send('This is koppmana\'s Web server.<br>')
    conn.send('<a href="/content">Content</a><br>')
    conn.send('<a href="/file">File</a><br>')
    conn.send('<a href="/image">Image</a><br>')

def handle_submit(conn, url_info, req_info, req_type):
    if req_type == "GET":
        query = url_info.query
    elif req_type == "POST":
        query = req_info.splitlines()[-1]

    data = urlparse.parse_qs(query)
    print data
    f_name = data['firstName'][0]
    l_name = data['lastName'][0]
    send_data = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<p>' + \
             'Hello Mr. %s %s.' % (f_name, l_name) + \
             '</p>'
    conn.send(send_data)

def handle_form(conn, urlInfo):
    forms = 'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            "<form action='/submit' method='GET'>" + \
            "First Name:<input type='text' name='firstName'>" + \
            "Last Name:<input type='text' name='lastName'>" + \
            "<input type='submit' value='Submit Get'>" + \
            "</form>\r\n" + \
            "<form action='/submit' method='POST'>" + \
            "First Name:<input type='text' name='firstName'>" + \
            "Last Name:<input type='text' name='lastName'>" + \
            "<input type='submit' value='Submit Post'>" + \
            "</form>\r\n"
    conn.send(forms)

def handle_connection_content(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Fulfilling content request</h1>')

def handle_connection_file(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Fulfilling file request</h1>')

def handle_connection_image(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Fulfilling image request</h1>')

def handle_connection_failed(conn):
    conn.send('HTTP/1.0 400 BAD\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Bad request</h1>')

def handle_connection_post(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('Hello, World.')

if __name__ == '__main__':
    main()
