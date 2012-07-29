'''
Created on Jul 22, 2012

@author: ewilde
'''
from google.appengine.ext import db

import lyonnessecreature


class LyonnessePC(lyonnessecreature.LyonnesseCreature):
    '''
    classdocs
    '''
    history = db.ReferenceProperty(collection_name="history")

    def clone(self, newOwner):
        result = super(LyonnessePC, self).clone( newOwner)

        if self.history:
            newHistory = self.history.clone( newOwner)
            newHistory.put()
            result.history = newHistory
        
        return result