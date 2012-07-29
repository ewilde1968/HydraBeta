import abstractitem

class Adventure(abstractitem.AbstractItem):
    """The base type for any entity in a gaming session"""

    def clone(self, newOwner):
        result = super(Adventure, self).clone( newOwner)

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        return super(Adventure, self).__eq__(other)
