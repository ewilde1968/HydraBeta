'''
Created on Jul 28, 2012

@author: ewilde
'''
import webapp2
import jinja2
import os

from google.appengine.api import users

from lyonnessemodel import lyonnessemass
from lyonnessemodel import lyonnesseitem
from hydramodel import hydracontent
from hydramodel import hydrauser


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname( os.path.pardir)))


class ItemPage(webapp2.RequestHandler):
    '''
    Item view HTML
    '''
    def get(self):
        currentUser = users.get_current_user()
        if not currentUser:
            # logged out, log the user back in
            url = users.create_login_url(self.request.uri)

            self.redirect(url)
        else:
            action = self.request.get("action")
            if action and action == 'new':
                # creating a new item
                hu = hydrauser.get_hydra_user(currentUser.nickname(), True)
                item = hydracontent.create_hydra_content(lyonnesseitem.LyonnesseItem,
                                                         owner=hu,
                                                         originalPublisher=hu
                                                         )

                template = jinja_environment.get_template('lyonnesseview/itemdetail.html')

            else:
                item = None

                template = jinja_environment.get_template('lyonnesseview/itemchoice.html')

            template_values = {
                               'logoutURL': users.create_logout_url(self.request.uri),
                               'currentUserID': currentUser.nickname(),
                               'massRBG0': lyonnessemass.get_lyonnessemass( lyonnessemass.LYONNESSEMASS_NEGLIGIBLE).valName,
                               'massRBG1': lyonnessemass.get_lyonnessemass( lyonnessemass.LYONNESSEMASS_TINY).valName,
                               'massRBG2': lyonnessemass.get_lyonnessemass( lyonnessemass.LYONNESSEMASS_SMALL).valName,
                               'massRBG3': lyonnessemass.get_lyonnessemass( lyonnessemass.LYONNESSEMASS_AVERAGE).valName,
                               'massRBG4': lyonnessemass.get_lyonnessemass( lyonnessemass.LYONNESSEMASS_LARGE).valName,
                               'massRBG5': lyonnessemass.get_lyonnessemass( lyonnessemass.LYONNESSEMASS_HUGE).valName
                               }
            if item:
                template_values['item'] = item

            self.response.out.write(template.render(template_values))
