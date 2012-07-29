import creature

class PlayerCharacter(creature.Creature):
    """The base type for any entity in a gaming session"""

    def clone(self, newOwner):
        result = super(PlayerCharacter, self).clone( newOwner)

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        return super(PlayerCharacter, self).__eq__(other)
