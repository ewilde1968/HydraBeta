'''
Created on Jul 22, 2012

@author: ewilde
'''
from google.appengine.ext import db

from hydramodel import hydracontent


class LyonnesseCreatureHistory(hydracontent.HydraContent):
    '''
    classdocs
    '''
    logEntries = db.ListProperty(db.Key, indexed=False)
    # description is the main history item
        
    def clone(self, newOwner):
        result = super(LyonnesseCreatureHistory, self).clone( newOwner)

        result.logEntries = []
        for l in self.logEntries:
            newEntry = db.get(l).clone(newOwner)
            newEntry.put()
            result.logEntries.append(newEntry.key())
            
        return result