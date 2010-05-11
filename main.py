import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

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



class MainPage(webapp.RequestHandler):
	def get(self):
		blogquery = BlogPost.all().order('-date')
		posts = blogquery.fetch(5)
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'blogposts' : posts,
			'url': url,
			'url_linktext': url_linktext,
		}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
				[('/', MainPage),
				 ('/Post', BlogPostPage)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()

