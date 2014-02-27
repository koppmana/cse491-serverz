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

# Test GET Connections

# Test / path
def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 80)

    assert 'HTTP/1.0 200' in conn.sent and 'form' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test /content path
def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 80)

    assert 'HTTP/1.0 200' in conn.sent and 'content' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test /file path
def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 80)

    assert 'HTTP/1.0 200' in conn.sent and 'file' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test /image path
def test_handle_connection_image():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Fulfilling image request</h1>'

    server.handle_connection(conn, 80)

    assert 'HTTP/1.0 200' in conn.sent and 'image' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)
    
# Test get sumbit 
def test_handle_get_submit():
    conn = FakeConnection("GET /submit?firstname=Mike&lastname=Jones" + \
                          " HTTP/1.1\r\n\r\n")

    server.handle_connection(conn, 80)

    assert 'html' in conn.sent and "Mike" in conn.sent \
      and 'Jones' in conn.sent, 'Got: %s' % (repr(conn.sent),)

# Test invalid path
def test_handle_invalid_path():
    conn = FakeConnection("GET /bad HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, 80)
    assert 'HTTP/1.0 404' in conn.sent and 'town' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test no first name in request
def test_handle_submit_no_first_name():
    conn = FakeConnection("GET /submit?firstname=&lastname=Jones" + \
                          " HTTP/1.1\r\n\r\n")

    server.handle_connection(conn, 80)

    assert 'html' in conn.sent and "Jones" in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test no last name in request
def test_handle_submit_no_last_name():
    conn = FakeConnection("GET /submit?firstname=Mike&lastname=" + \
                          " HTTP/1.1\r\n\r\n")

    server.handle_connection(conn, 80)

    assert 'html' in conn.sent and "Mike" in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test POST stuff

def test_handle_connection_post():
    conn = FakeConnection("POST / HTTP/1.0\r\n" + \
      "Content-length: 0\r\n\r\n")

    server.handle_connection(conn, 80)
    assert 'HTTP/1.0 200' in conn.sent and 'form' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test submitting form via POST
def test_handle_post_submit():
    conn = FakeConnection("POST /submit HTTP/1.1\r\n" + \
                          "Content-Length: 31\r\n\r\n" + \
                          "firstname=Mike&lastname=Jones")

    server.handle_connection(conn, 80)
    
    assert 'HTTP/1.0 200' in conn.sent and "WHO?" in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test multipart form encoding
def test_handle_submit_post_multipart_and_form_data():
    conn = FakeConnection("POST /submit " + \
          "HTTP/1.1\r\nContent-length: 246\r\n\r\n------" + \
          "WebKitFormBoundaryAaal27xQakxMcNYm\r\n" + \
          'Content-Disposition: form-data; name="firstname"\r\n\r\nMike' + \
          '\r\n------WebKitFormBoundaryAaal27xQakxMcNYm\r\n' + \
          'Content-Disposition: form-data; name="lastname"\r\n\r\nJones' + \
          '\r\n------WebKitFormBoundaryAaal27xQakxMcNYm--")')

    server.handle_connection(conn, 80)
    
    assert 'HTTP/1.0 200' in conn.sent and "WHO?" in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test long requests
def test_handle_long_request():
    firstname = lastname = "werrrwerwerwerqeew" * 100
    conn = FakeConnection("POST /submit HTTP/1.1\r\n" + \
                          "Content-Length: 4020\r\n\r\n" + \
                          "firstname=%s&lastname=%s" % (firstname, lastname))

    server.handle_connection(conn, 80)
    
    assert 'HTTP/1.0 200' in conn.sent and "WHO?" in conn.sent, \
    'Got: %s' % (repr(conn.sent),)
    
# Test empty request
def test_handle_empty_request():
  conn = FakeConnection("\r\n\r\n")

  server.handle_connection(conn, 80)

  assert 'HTTP/1.0 404' in conn.sent and 'town' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)

# Test invalid post path request
def test_handle_invalid_path_post():
    conn = FakeConnection("POST /bad HTTP/1.1\r\n" + \
                          "Content-Length: 31\r\n\r\n" + \
                          "firstname=Mike&lastname=Jones")

    server.handle_connection(conn, 80)
    assert 'HTTP/1.0 404' in conn.sent and 'town' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)





