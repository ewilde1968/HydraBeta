'''
Created on Jul 22, 2012

@author: ewilde
'''
from google.appengine.ext import db

from hydramodel import hydracontent


class LyonnesseLogEntry(hydracontent.HydraContent):
    '''
    classdocs
    '''
    eventDate = db.DateTimeProperty( auto_now_add=True)

    def clone(self, newOwner):
        result = super(LyonnesseLogEntry, self).clone( newOwner)

        result.eventDate = self.eventDate;
        
        return result