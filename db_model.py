from google.appengine.ext import db

class BlogPost(db.Model):
	author = db.UserProperty()
	content = db.TextProperty()
	title = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

