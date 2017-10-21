import dropbox 

access = ''

db = dropbox.Dropbox(access)
db.users_get_current_account()

return 0
