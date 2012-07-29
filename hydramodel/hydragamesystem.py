'''
Created on Jul 22, 2012

@author: ewilde
'''

from google.appengine.ext import db

import hydracontent


class HydraGameSystem(hydracontent.HydraContent):
    '''
    Object to describe the game system used
    '''
    version = db.StringProperty()

    def clone(self, newOwner):
        result = super(HydraGameSystem, self).clone( newOwner)

        result.version = self.version

        return result

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.version != other.version:
            return False

        return super(HydraGameSystem, self).__eq__(other)
