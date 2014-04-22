# __init__.py is the top level file in a Python package.

import os
import sqlite3

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

DB_FILE = "images.sqlite"

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
     html.init_templates()

     if not os.path.exists(DB_FILE):
          create_db()
          

def create_db():
     print 'creating database'
     db = sqlite3.connect('images.sqlite')
     db.execute('CREATE TABLE image_store (i INTEGER PRIMARY KEY, filetype \
          VARCHAR(255), image BLOB)');
##    db.execute('CREATE TABLE image_comments (i INTEGER PRIMARY KEY, imageId INTEGER, \
##     comment TEXT, FOREIGN KEY (imageId) REFERENCES image_store(i))');
     db.commit()
     db.close()
     
def teardown():                         # stuff that should be run once.
     pass
