import quixote
import json
from quixote.directory import Directory, export, subdir

from . import html, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        return html.render('index.html')

    @export(name='jquery')
    def jquery(self):
        return open('jquery-1.11.0.min.js').read()

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload2')
    def upload2(self):
        return html.render('upload2.html')

    @export(name='search')
    def search(self):
        return html.render("search.html")

    @export(name='top')
    def top(self):
        return html.render("top.html")

    @export(name='most')
    def most(self):
        return html.render("most.html")

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_count')
    def image_count(self):
        return image.image_count()

    @export(name='imagelist')
    def imagelist(self):
        return html.render("imagelist.html")

    # receive file data from form, add image and metadata to db
    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        img_name = request.form['img_name']
        img_desc = request.form['desc']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(the_file.get_size())

        image.add_image(data, the_file.base_filename.split('.')[-1], img_name, \
                        img_desc)

        return quixote.redirect('./')

    # search for image based on user input
    @export(name="image_search")
    def image_search(self):
        request = quixote.get_request()

        imgKeys = image.image_search(request.form["query"])

        images = []
        
        for index, name in imgKeys.items():
            images.append("""\
                <image>
                 <index>%i</index>
                 <name>%s</name>
                </image>
                """ % (index, name))
        
        xml = """
            <images>
            %s
            </images>
            """ % ("".join(images))
        
        return xml

    # return xml of the top 10 rated images
    @export(name="get_top_rated")
    def get_top_rated(self):
        request = quixote.get_request()

        # call of to db to get the indexes of top 10 images
        imgKeys = image.get_top_rated()

        images = []
        
        for i in imgKeys:
            images.append("""\
                <image>
                 <index>%i</index>
                 <rating>%s</rating>
                </image>
                """ % (i[0], i[1]))
        
        xml = """
            <images>
            %s
            </images>
            """ % ("".join(images))
        
        return xml

    # return xml of the 10 most rated images
    @export(name="get_most_rated")
    def get_most_rated(self):
        request = quixote.get_request()

        imgKeys = image.get_most_rated()

        images = []
        
        for i in imgKeys:
            images.append("""\
                <image>
                 <index>%i</index>
                 <rating>%s</rating>
                </image>
                """ % (i[0], i[1]))
        
        xml = """
            <images>
            %s
            </images>
            """ % ("".join(images))
        
        return xml
    

    # return an image from the db
    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()
        
        try:
            index = int(str(request.form["index"]).split('#')[0])
        except:
            index = 0
            
        img = image.get_image(index)

        imgtype = img.filetype

        if imgtype in ("jpg", "jpeg"):
            response.set_content_type('image/jpeg')
        elif imgtype in ("tif", "tiff"):
            response.set_content_type("image/tiff")
        else:
            response.set_content_type("image/png")
        
        return img.data


    # get comment from post request, save in db
    @export(name="add_comment")
    def add_comment(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            index = int(request.form["index"])
        except:
            index = 0

        try:
            comment = request.form["comment"]
        except:
            return

        image.add_comment(index, comment)


    # return xml of the comments for an image
    @export(name="get_comments")
    def get_comments(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            index = int(request.form['index'])
        except:
            index = 0

        all_comments = []

        comments = image.get_comments(index)

        #build the xml to pass to page
        for comment, timestamp in comments:
            all_comments.append("""\
                <comment>
                 <text>%s</text>
                 <timestamp>%s</timestamp>
                </comment>
                """ % (comment, timestamp))

        xml = """
            <comments>
            %s
            </comments>
            """ % ("".join(all_comments))

        return xml

    # return xml of an images metadata
    @export(name="get_meta_data")
    def get_meta_data(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            index = int(request.form['index'])
        except:
            index = 0

        meta_data = image.get_meta_data(index)

        #build the xml to pass to page

        xml = """
            <metadata>
            <name>%s</name>
            <desc>%s</desc>
            <rating>%.2f</rating>
            <count>%i</count>
            <timestamp>%s</timestamp>
            </metadata>
            """ % (meta_data[0], meta_data[1], meta_data[2], meta_data[3], \
                   meta_data[4])

        return xml

    # update rating change of an image 
    @export(name="update_rating")
    def update_rating(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            index = int(str(request.form["index"]).split('#')[0])
        except:
            index = 0
        
        try:
            rating = int(request.form["rating"])
        except:
            return

        image.update_rating(index, rating)

##    @export(name='create')
##    def create(self):
##        return html.render('create_account.html')

##    @export(name='home')
##    def home(self):
##        return html.render('home.html')

##    @export(name="create_account")
##    def create_account(self):
##        request = quixote.get_request()
##
##        username = request.form["username"]
##        password = request.form['password']
##        confirmPw = request.form['confirm']
##
##        # very simple password comparison check
##        # if password == confirmPw:
##            
##        # if username didn't exist redirect to home
##        if image.create_account(username, password):
##            quixote.redirect("/home?user=" + username)

##    @export(name="login")
##    def login(self):
##        request = quixote.get_request()
##
##        username = request.form["username"]
##        password = request.form['password']
##
##        if image.login(username, password):
##            quixote.redirect("/home?user=" + username)

