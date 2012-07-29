import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.db import polymodel


def get_content_key( content):
        try:
            key = content.key()
        except:
            logging.info( 'HydraUser:get_content_key - content has no key')
            raise

        return key


def users_parent_key():
    return db.Key.from_path('userlist', 'default')

def user_key(user):
    return db.Key.from_path('userlist','default','HydraUser',user.nickname())


class HydraUser(polymodel.PolyModel):
    """Models a user of the application, including access settings"""
    userID = db.UserProperty(required=True)
    contentKeys = db.ListProperty(item_type=db.Key, indexed=False)
    
    def add_ownership(self, content):
        key = get_content_key( content)

        # insert into content if not already there
        try:
            self.contentKeys.index( key)
        except:
            if content.owner != self:
                # clone the content if not already owned
                logging.info( 'need to clone')
                newContent = content.clone(self)
                newContent.put()
                key = get_content_key( newContent)

            if not self.contentKeys:
                self.contentKeys = []
            self.contentKeys.append( key)
            
    def remove_access(self, content):
        key = get_content_key( content)

        #delete the content if already owned
        try:
            self.contentKeys.remove( key)

            if content.owner == self:
                content.delete()
        except:
            logging.info( 'did not contain key')
            pass

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        return self.userID == other.userID


def load_hydra_users():
    """Load all the users from the database and return a set"""
    logging.info( 'load_hydra_users')
    usersQuery = HydraUser.all().ancestor( users_parent_key())
    result = []
    for user in usersQuery:
        result.append(user)

    return result


def create_hydra_user(user):
    """Class Factory for HydraUser, use factory to set parent"""
    result = HydraUser(userID = user or users.get_current_user(),
                       key_name = user.nickname(),
                       parent = users_parent_key())
    result.put()
    logging.info( 'created HydraUser %s', user.nickname())

    return result


def get_hydra_user(userStr, create=False):
    """Find the HydraUser if it exists in the db"""
    logging.info("Looking for HydraUser ")
    logging.info(userStr)

    # Find or create the hydrauser for the existing user
    if len(userStr) > 0:
        user = users.User(userStr)
    else:
        user = users.get_current_user()
    result = db.get(user_key(user))
    logging.info(result)

    if not result:
        logging.info('did not find')
        if create:
            return create_hydra_user(user)

    return result
