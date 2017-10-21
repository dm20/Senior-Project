#    Dropbox upload script
# -- pip install dropbox --

import dropbox

file1 = open('image.jpg').read()

db = dropbox.Dropbox('ippz4jAbhKAAAAAAAAAACSgGqnfO0L2JvjAb-YJ6l7KWZqo3uGLsjSU6d6afDKse')

db.files_upload(file1,'/new_pic.jpg')

