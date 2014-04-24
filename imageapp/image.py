# image handling API
import sqlite3


import os

DB_FILE = "images.sqlite"

images = {}

class Image(object):
    def __init__(self, data="", filetype=""):
        self.filetype = filetype
        self.data = data

# add image to db
def add_image(data, filetype, name, desc):
    db = sqlite3.connect(DB_FILE)

    db.text_factory = bytes

    # insert image into db
    db.execute('INSERT INTO image_store (image, filetype, name, desc) \
                VALUES (?, ?, ?, ?)', (data, filetype, name, desc))
    db.commit()

# return Image object built from image info from db
def get_image(num):
    db = sqlite3.connect(DB_FILE)

    db.text_factory = bytes

    c = db.cursor()

    # Get image by key value
    if num > 0:
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
    return get_image(0)

# return count of images
def image_count():
    db = sqlite3.connect(DB_FILE)

    c = db.cursor()

    c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')

    try:
        return int(c.fetchone()[0])
    except:
        return 0
    
# add a comment to the db
def add_comment(i, comment):
    db = sqlite3.connect(DB_FILE)

    db.text_factory = bytes

    c = db.cursor()

    if i < 1:
        c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
        try:
            i = c.fetchone()[0]
        except:
            return

    # insert comment into db
    db.execute('INSERT INTO comments (imgKey, comment) VALUES (?, ?)',
               (i, comment))
    db.commit()

# get comments from db
def get_comments(i):
    db = sqlite3.connect(DB_FILE)

    c = db.cursor()

    # get last image key
    if i < 1:
        c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
        try:
            i = c.fetchone()[0]
        except:
            return
        
    # get the comments for an image
    c.execute('SELECT i, comment, timestamp FROM comments WHERE imgKey=(?) ORDER BY timestamp \
        ASC', (i,))
    
    comments = []
    
    # get each comment into a list
    for row in c:
        comments.append((row[1], row[2]))

    return comments

# get metadata from db
def get_meta_data(i):
    db = sqlite3.connect(DB_FILE)

    c = db.cursor()

    # get last image key if index invalid
    if i < 1:
        c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
        try:
            i = c.fetchone()[0]
        except:
            return
        
    # get the comments for an image
    c.execute('SELECT name, desc, avg_rating, rating_count, timestamp FROM \
            image_store WHERE i=(?)', (i,))
    
    for row in c:
        return [row[0], row[1], float(row[2]), row[3], row[4]]

# return list of img indexes based off search criteria
def image_search(qs):
    db = sqlite3.connect(DB_FILE)

    c = db.cursor()

    # search db for images with name or desc containing the user search text
    c.execute('SELECT i, name FROM image_store WHERE name LIKE ? OR \
                desc LIKE ?', ("%"+qs+"%", "%"+qs+"%"))

    imgKeys = {}
    
    for row in c:
        imgKeys[row[0]] = row[1]

    return imgKeys

# get 10 highest rated images from db
def get_top_rated():
    db = sqlite3.connect(DB_FILE)

    c = db.cursor()

    # search db for images with name or desc containing the user search text
    c.execute('SELECT i, avg_rating FROM image_store ORDER BY avg_rating DESC LIMIT 10')

    imgKeys = []
    
    for row in c:
        imgKeys.append((row[0],row[1]))

    return imgKeys

# get 10 images with most ratings from db
def get_most_rated():
    db = sqlite3.connect(DB_FILE)

    c = db.cursor()

    # search db for images with name or desc containing the user search text
    c.execute('SELECT i, rating_count FROM image_store ORDER BY rating_count DESC LIMIT 10')

    imgKeys = []
    
    for row in c:
        imgKeys.append((row[0],row[1]))

    return imgKeys


# update rating in db 
def update_rating(index, rating):
    db = sqlite3.connect(DB_FILE)
    
    db.text_factory = bytes

    c = db.cursor()

    # get last image key if index invalid
    if index < 1:
        c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
        try:
            index = c.fetchone()[0]
        except:
            return
    
    c.execute('SELECT avg_rating, rating_count FROM image_store WHERE i=?', (index,))

    rs = c.fetchone()
    avg_rating = float(rs[0])
    rating_count = int(rs[1])

    # add one to count because user just rated
    rating_count += 1

    new_avg = calc_new_rating(avg_rating, rating, rating_count)
    
    c.execute('UPDATE image_store SET avg_rating=?, rating_count=? WHERE i=?', \
               (new_avg, rating_count, index))

    db.commit()

# calculate new average based on user rating and numbers of ratings
def calc_new_rating(avg, rating, count):
    diff = abs((rating - avg) / float(count))

    if rating > avg:
        avg += diff
    else:
        avg -= diff
        
    return avg
        

##def create_account(username, password):
##    db = sqlite3.connect(DB_FILE)
##
##    c = db.cursor()
##
##    c.execute("SELECT i FROM accounts WHERE username=(?)", (str(username),))
##
##    # check if username already exsists
##    try:
##        if c.fetchone()[0] < 1:
##            db.execute('INSERT INTO accounts (username, password) VALUES (?, ?)', \
##               (username, password))
##            return True
##    except:
##        return False
##
##def login(username, password):
##    db = sqlite3.connect(DB_FILE)
##
##    c = db.cursor()
##
##    c.execute("SELECT i FROM accounts WHERE username=(?) AND password=(?)", \
##              (str(username), str(password)))
##
##    try:
##        if c.fetchone()[0] > 0:
##            return True
##    except:
##        return False





    
