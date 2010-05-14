import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

from db_model import BlogPost

class BlogPostPage(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			path = os.path.join(os.path.dirname(__file__), 'post.html')
			self.response.out.write(template.render(path, None))
		else:
			self.redirect('/')

	def post(self):
		blog = BlogPost()
		blog.author = users.get_current_user()
		blog.content = self.request.get('content')
		blog.title = self.request.get('title')
		blog.put()
		self.redirect('/')



