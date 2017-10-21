#    Dropbox upload script
# -- pip install dropbox --

import dropbox

access = ''

file1 = open('image.jpg').read()

db = dropbox.Dropbox(access)

db.files_upload(file1,'/new_pic.jpg')

