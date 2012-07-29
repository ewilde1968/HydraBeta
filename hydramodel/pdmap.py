from google.appengine.ext import db

import hydramap

class PDMap(hydramap.HydraMap):
    """The base type for any entity in a gaming session"""
    masks = db.ListProperty(db.Key, indexed=False)

    def clone(self, newOwner):
        result = super(PDMap, self).clone( newOwner)

        result.masks = []
        for mask in self.masks:
            result.masks.append( db.get(mask).clone( result))

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if len(self.masks) == len(other.masks):
            for i in range( len(self.masks)):
                s = self.masks[i]
                o = other.masks[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
            return False

        return super(PDMap, self).__eq__(other)
