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
    
    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(the_file.get_size())

        image.add_image(data, the_file.base_filename.split('.')[-1])

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()
        
        try:
            img = image.get_image(int(request.form["index"]))
        except KeyError:
            img = image.get_latest_image()

        imgtype = img.filetype

        if imgtype in ("jpg", "jpeg"):
            response.set_content_type('image/jpeg')
        elif imgtype in ("tif", "tiff"):
            response.set_content_type("image/tiff")
        else:
            response.set_content_type("image/png")
        
        return img.data

    @export(name='image_count')
    def image_count(self):
        return image.image_count()

    @export(name='imagelist')
    def imagelist(self):
        return html.render("imagelist.html")
