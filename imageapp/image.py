# image handling API
import sqlite3
DB_FILE = "images.db"

import os

images = {}

class Image(object):
    def __init__(self, data="", filetype=""):
        self.filetype = filetype
        self.data = data

def initialize():
    load()

def load():
    global images
##    if not os.path.exists(DB_FILE):
##        print 'CREATING', DB_FILE
##        db = sqlite3.connect(DB_FILE)
##        qs = "CREATE TABLE image_store" + \
##             "(i INTEGER PRIMARY KEY, image BLOB)"
##        db.execute(qs)
##        db.commit()
##        db.close()
##        
##    # connect to database
##    db = sqlite3.connect(DB_FILE)
##
##    db.text_factory = bytes
##
##    c = db.cursor()
##
##    # select all of the images
##    c.execute('SELECT i, image FROM image_store')
##    for i, image in c.fetchall():
##        images[i] = image

def add_image(data, filetype):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0

    image = Image(data, filetype)
##    # connect to the already existing database
##    db = sqlite3.connect(DB_FILE)
##
##    # configure to allow binary insertions
##    db.text_factory = bytes
##
##    # insert!
##    db.execute('INSERT INTO image_store (i, image) VALUES (?, ?)',
##               (image_num, data))
##    db.commit()

    images[image_num] = image
    
    return image_num

def get_image(num):
    return images[num]

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]

def get_images():
    return images

def image_count():
    try:
        return max(images.keys()) + 1
    except ValueError:
        return 0
