# image handling API
import sqlite3


import os

DB_FILE = "images.sqlite"

images = {}

class Image(object):
    def __init__(self, data="", filetype=""):
        self.filetype = filetype
        self.data = data

def add_image(data, filetype):
    db = sqlite3.connect(DB_FILE)

    db.text_factory = bytes

    # insert image into db
    db.execute('INSERT INTO image_store (image, filetype) VALUES (?, ?)',
               (data, filetype))
    db.commit()

def get_image(num):
    db = sqlite3.connect(DB_FILE)

    db.text_factory = bytes

    c = db.cursor()

    # Get image by key value
    if num >= 0:
        c.execute('SELECT i, filetype, image FROM image_store WHERE i=(?)', \
                  (num,))
    else:
        c.execute('SELECT i, filetype, image FROM image_store ORDER BY i \
            DESC LIMIT 1')

    try:
        i, filetype, image = c.fetchone()
        print "got image: " + str(i)

        return Image(image, filetype)
    except:
        pass

def get_latest_image():
    return get_image(-1)

def image_count():
    db = sqlite3.connect(DB_FILE)

    c = db.cursor()

    # insert!
    c.execute('SELECT COUNT(*) FROM image_store')

    try:
        return int(c.fetchone()[0])
    except:
        return 0
