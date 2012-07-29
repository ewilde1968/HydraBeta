'''
Created on Jul 26, 2012

@author: ewilde
'''
import webapp2
import jinja2
import os

from google.appengine.api import users

from hydramodel import hydrauser


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname( os.path.pardir)))


class HomePage(webapp2.RequestHandler):
    '''
    Entry page for web application
    '''
    def get(self):
        currentUser = users.get_current_user()
        if not currentUser:
            # logged out, log the user back in
            url = users.create_login_url(self.request.uri)

            self.redirect(url)
        else:
            hydrauser.get_hydra_user(currentUser.nickname(), True)
            
            template = jinja_environment.get_template('lyonnesseview/index.html')

            template_values = {
                               'logoutURL': users.create_logout_url(self.request.uri),
                               'currentUserID': currentUser.nickname()
                               }

            self.response.out.write(template.render(template_values))
