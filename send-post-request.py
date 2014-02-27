#! /usr/bin/env python
import sys
import requests

url = sys.argv[1]

payload = { 'key' : 'value', 'firstname' : 'Mike', 'lastname' : 'Jones' }
r = requests.post(url, files=payload)

print r.status_code
print r.text


