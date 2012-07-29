import webapp2
import jinja2
import os

from hydracontroller.homepage import HomePage
from hydracontroller.itempage import ItemPage


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


app = webapp2.WSGIApplication([('/', HomePage),
                               ('/item', ItemPage)
                               ],
                              debug=True)
