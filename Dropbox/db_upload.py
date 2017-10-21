#    Dropbox upload script
# -- pip install dropbox --

import dropbox

file = open('test.txt')

db = dropbox.Dropbox('9Z0y_pZ_w8sAAAAAAAAAr6wdpjNlg0XW9hTL0RIdNzkWTSfFUYZB23IQKTOjkMi8')

db.files_upload(file,'/uploaded.txt')

file.close()

