#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import jinja2
from StringIO import StringIO

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
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    request = conn.recv(1)

    # We get the headers here
    while request[-4:] != '\r\n\r\n':
        request += conn.recv(1)

    split_request = request.split('\r\n')[0].split(' ')
    print split_request

    req_type = request_line1[0]

    try:
        url_parse = urlparse.urlparse(split_request[1])
        path = url_parse[2]
    except:
        invalid_path(conn, env)
        return

    if req_type == "GET":
        if path == "/":
            handle_connection_default(conn, env)
        elif path == "/content":
            handle_connection_content(conn, env)
        elif path == "/image":
            handle_connection_image(conn, env)
        elif path == "/file":
            handle_connection_file(conn, env)
        elif path == "/form":
            handle_form(conn, url_parse)
        elif path == "/submit": 
            handle_submit_get(conn, url_parse[4], env)
        else:
            invalid_path(conn, env)
    elif req_type == "POST":
        headers_dict, content = parse_post_request(conn, request)
        environ = {}
        environ['REQUEST_METHOD'] = 'POST'

        form = cgi.FieldStorage(headers = headers_dict, fp = StringIO(content), \
                                environ = environ)
        if path == "/":
            handle_connection_default(conn, env)
        elif path == "/submit":
            handle_submit_post(conn, form, env)
        else:
            invalid_path(conn, env)

    conn.close()

def handle_connection_default(conn, env):
    response = 'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            env.get_template("index.html").render()

  conn.send(response)


def handle_submit_get(conn, params, env):
    params = urlparse.parse_qs(params)

    try:
      firstname = params['firstname'][0]
    except KeyError:
      firstname = ''
      
    try:
      lastname = params['lastname'][0]
    except KeyError:
      lastname = ''

    vars = dict(firstname = firstname, lastname = lastname)
    template = env.get_template("submit.html")

    response = 'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            env.get_template("submit.html").render(vars)

    conn.send(response)

def handle_submit_post(conn, form, env):
     try:
      firstname = form['firstname'].value
    except KeyError:
      firstname = ''
    try:
      lastname = form['lastname'].value
    except KeyError:
      lastname = ''

    vars = dict(firstname = firstname, lastname = lastname)
    template = env.get_template("submit_result.html")

    response = 'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            env.get_template("submit.html").render(vars)

    conn.send(response)

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
            "<form action='/submit' method='POST' enctype='multipart/form-data'>" + \
            "First Name:<input type='text' name='firstName'>" + \
            "Last Name:<input type='text' name='lastName'>" + \
            "<input type='submit' value='Submit Multipart Post'>" + \
            "</form>\r\n"
    conn.send(forms)

def handle_connection_content(conn, env):
    response = 'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            env.get_template("content.html").render()

    conn.send(response)

def handle_connection_file(conn, env):
    response = 'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            env.get_template("file.html").render()

    conn.send(response)

def handle_connection_image(conn, env):
    response = 'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            env.get_template("image.html").render()
    
    conn.send(response)

def invalid_path(conn, env):
    response = 'HTTP/1.0 404 Not Found\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            env.get_template("invalid_path.html").render()

    conn.send(response)

def parse_post_request(conn, request):
  ''' Takes in a request (as a string), parses it, and
      returns a dictionary of header name => header value
      returns a string built from the content of the request'''
  
  header_dict = dict()

  request_split = request.split('\r\n')

  # Headers are separated from the content by '\r\n'
  # which, after the split, is just ''.

  # First line isn't a header, but everything else
  # up to the empty line is. The names are separated
  # from the values by ': '
  for i in range(1,len(request_split) - 2):
    header = request_split[i].split(': ', 1)
    header_dict[header[0].lower()] = header[1]

  content_length = int(header_dict['content-length'])

  content = ''
  for i in range(0,content_length):
    content += conn.recv(1)

  return header_dict, content

if __name__ == '__main__':
    main()
