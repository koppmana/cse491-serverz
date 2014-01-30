import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is koppmana\'s Web server.<br>' \
                      '<a href="/content">Content</a><br>' + \
                      '<a href="/file">File</a><br>' + \
                      '<a href="/image">Image</a><br>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Fulfilling content request</h1>'

    server.handle_connection_content(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Fulfilling file request</h1>'

    server.handle_connection_file(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Fulfilling image request</h1>'

    server.handle_connection_image(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_failed():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 400 BAD\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Bad request</h1>'

    server.handle_connection_failed(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_post():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'Hello, World.'

    server.handle_connection_post(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_form():
    form_conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")

    form_return = 'HTTP/1.0 200 OK\r\n' + \
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

    server.handle_connection(form_conn)

    assert form_conn.sent == form_return, 'Got: %s' % (repr(form_conn.sent),)

def test_handle_get_submit():
    submit_conn = FakeConnection("GET /submit?firstName=Allen&lastName=Koppman HTTP/1.0\r\n\r\n")

    submit_return = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<p>' + \
             'Hello Mr. Allen Kopppman.' + \
             '</p>'

    server.handle_connection(submit_conn)

    assert submit_conn.sent == submit_return, 'Got: %s' % (repr(submit_conn.sent),)

def test_handle_post_submit():
    submit_conn = FakeConnection("POST /submit HTTP/1.0\r\n\r\nfirstName=Allen&lastName=Koppman")

    submit_return = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<p>' + \
             'Hello Mr. Allen Koppman.' + \
             '</p>'

    server.handle_connection(submit_conn)

    assert submit_conn.sent == submit_return, 'Got: %s' % (repr(submit_conn.sent),)
