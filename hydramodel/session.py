from google.appengine.ext import db

import hydracontent

class Session(hydracontent.HydraContent):
    """Models content in the application"""
    referees = db.ListProperty(db.Key, indexed=False)
    players = db.ListProperty(db.Key, indexed=False)
    lastUpdated = db.DateTimeProperty(auto_now=True)
    currentEncounter = db.ReferenceProperty(collection_name='currentEncounter')

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if len(self.referees) == len(other.referees):
            for i in range( len(self.referees)):
                s = self.referees[i]
                o = other.referees[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
            return False
        
        if len(self.players) == len(other.players):
            for i in range( len(self.players)):
                s = self.players[i]
                o = other.players[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
            return False
        
        if self.currentEncounter != other.currentEncounter:
            return False
        
        return super(Session, self).__eq__(other)
