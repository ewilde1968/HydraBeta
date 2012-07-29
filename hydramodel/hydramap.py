from google.appengine.ext import db

import hydracontent

class HydraMap(hydracontent.HydraContent):
    """The base type for any entity in a gaming session"""
    encounters = db.ListProperty(db.Key, indexed=False)
    location = db.ListProperty(float, indexed=False)
    image = db.BlobProperty()

    def clone(self, newOwner):
        result = super(HydraMap, self).clone( newOwner)

        result.encounters = []
        for encounter in self.encounters:
            result.encounters.append( db.get(encounter).clone( result))

        result.location = []
        for coordinate in self.location:
            result.location.append( coordinate)

        result.image = self.image

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if self.image != other.image:
            return False

        if len(self.encounters) == len(other.encounters):
            for i in range( len(self.encounters)):
                s = self.encounters[i]
                o = other.encounters[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
            return False

        if len(self.location) == len(other.location):
            for i in range( len(self.location)):
                if self.location[i] != other.location[i]:
                    return False

        return super(HydraMap, self).__eq__(other)
