from google.appengine.ext import db

import adventure

class Campaign(adventure.Adventure):
    """The base type for any entity in a gaming session"""
    adventures = db.ListProperty(db.Key, indexed=False)
    pcs = db.ListProperty(db.Key, indexed=False)
    sessions = db.ListProperty(db.Key, indexed=False)

    def clone(self, newOwner):
        result = super(Campaign, self).clone( newOwner)

        result.adventures = []
        for adventure in self.adventures:
            result.adventures.append( db.get(adventure).clone( result))

        result.pcs = []
        for pc in self.pcs:
            result.pcs.append( db.get(pc).clone( result))

        result.sessions = []
        for session in self.sessions:
            result.sessions.append( db.get(session).clone( result))

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if len(self.adventures) == len(other.adventures):
            for i in range( len(self.adventures)):
                # key compare
                if self.adventures[i] != other.adventures[i]:
                    return False

        if len(self.pcs) == len(other.pcs):
            for i in range( len(self.pcs)):
                # key compare
                if self.pcs[i] != other.pcs[i]:
                    return False

        if len(self.sessions) == len(other.sessions):
            for i in range( len(self.sessions)):
                # key compare
                if self.sessions[i] != other.pcs[i]:
                    return False

        return True
