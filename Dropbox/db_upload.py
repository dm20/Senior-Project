#    Dropbox upload script
# -- pip install dropbox --

import dropbox

file = open('test.txt')

db = dropbox.Dropbox('ippz4jAbhKAAAAAAAAAACSgGqnfO0L2JvjAb-YJ6l7KWZqo3uGLsjSU6d6afDKse')

db.files_upload(file,'/uploaded.txt')

file.close()

