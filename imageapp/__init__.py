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
          VARCHAR(255), name VARCHAR(50), desc VARCHAR(255), avg_rating FLOAT DEFAULT 5, \
                rating_count INTEGER DEFAULT 0, image BLOB, timestamp \
          DATETIME DEFAULT CURRENT_TIMESTAMP)');
     
     db.execute('CREATE TABLE comments (i INTEGER PRIMARY KEY, imgKey INTEGER, \
          comment VARCHAR(255), timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, \
          FOREIGN KEY (imgKey) REFERENCES image_store(i))');

##     db.execute('CREATE TABLE accounts (i INTEGER PRIMARY KEY, username \
##          VARCHAR(255), password VARCHAR(255))');
     
     db.commit()
     db.close()
     
def teardown():                         # stuff that should be run once.
     pass
