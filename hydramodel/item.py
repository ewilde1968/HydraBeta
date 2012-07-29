from google.appengine.ext import db

import abstractitem


ABSTRACTITEM_OWNED = 0
ABSTRACTITEM_CARRIED = 1
ABSTRACTITEM_READY = 2

class Item(abstractitem.AbstractItem):
    """The base type for any entity in a gaming session"""
    mass = db.ReferenceProperty(collection_name='mass')
    size = db.ReferenceProperty(collection_name='size')
    readiness = db.IntegerProperty()

    def clone(self, newOwner):
        result = super(Item, self).clone( newOwner)

        result.mass = self.mass
        result.size = self.size
        result.readiness = self.readiness

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if not (self.mass == other.mass
                or db.get(self.mass) == db.get(other.mass)):
            return False

        if not (self.size == other.size
                or db.get(self.size) == db.get(other.size)):
            return False
            
        return super(Item, self).__eq__(other)
