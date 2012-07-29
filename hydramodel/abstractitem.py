from google.appengine.ext import db

import hydracontent


class AbstractItem(hydracontent.HydraContent):
    """The base type for any entity in a gaming session"""
    category = db.CategoryProperty()
    location = db.ListProperty(float, indexed=False) # Location
    playerDescription = db.TextProperty()           # 1MB limit
    imageURL = db.LinkProperty()

    def clone(self, newOwner):
        result = super(AbstractItem, self).clone( newOwner)

        result.category = self.category
        result.playerDescription = self.playerDescription
        result.imageURL = self.imageURL

        result.location = []
        for coordinate in self.location:
            result.location.append( coordinate)

        return result

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.category != other.category:
            return False

        if self.location != other.location:
            if len(self.location) == len(other.location):
                for i in range( len(self.location)):
                    if self.location[i] != other.location[i]:
                        return False
            else:
                return False

        if self.playerDescription != other.playerDescription:
            # key compare
            return False
            
        return super(AbstractItem, self).__eq__(other)
