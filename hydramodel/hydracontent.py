import logging

from google.appengine.ext import db
from google.appengine.ext.db import polymodel


class HydraContent(polymodel.PolyModel):
    """Models content in the application"""
    owner = db.ReferenceProperty(required=True, collection_name='owner')
    originalPublisher = db.ReferenceProperty()      # Paid Publisher
    paid = db.BooleanProperty(default=False)        # protected content
    contentSet = db.ListProperty(db.Key, indexed=False) # Content
    nativeSystem = db.ReferenceProperty(collection_name='nativeSystem')
    instanceName = db.StringProperty()
    description = db.TextProperty()                 # 1MB limit
    rating = db.RatingProperty()                    # social rating
        
    def determine_owner_object(self, holder):
        # determine if root owned object or contained object
        if isinstance( holder, HydraContent):
            return holder.owner
        return holder

    def determine_container_object(self, holder):
        # determine if root owned object or contained object
        if isinstance( holder, HydraContent):
            return holder
        return None

    def clone_content(self, newContent):
        # recurse through the content set and clone the items
        if self.contentSet:
            newContent.contentSet = []
            for content in self.contentSet:
                newContent.contentSet.append( content.clone( newContent))
        
    def clone(self, holder):
        # create a new object of the right type with properties
        newType = self.__class__
        newOwner = self.determine_owner_object(holder)

        result = newType(owner = newOwner,
                         originalPublisher = self.originalPublisher,
                         paid = self.paid,
                         nativeSystem = self.nativeSystem,
                         instanceName = self.instanceName,
                         description = self.description,
                         rating = self.rating,
                         parent = newOwner)
        self.clone_content( result)

        # add to new owner's contentSet
        newContainer = self.determine_container_object(holder)
        if isinstance( newContainer, HydraContent):
            if not newContainer.contentSet:
                newContainer.contentSet = []
            newContainer.contentSet.append( result)

        return result

    def __ne__(self, other):
        return not self==other
    
    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if self.owner.key() != other.owner.key():
            return False

        if self.originalPublisher != other.originalPublisher:
            return False

        if self.paid != other.paid:
            return False

        if len(self.contentSet) == len(other.contentSet):
            for i in range( len(self.contentSet)):
                s = self.contentSet[i]
                o = other.contentSet[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
            return False

        if self.nativeSystem != other.nativeSystem:
            return False

        if self.instanceName != other.instanceName:
            return False

        if self.description != other.description:
            return False

        if self.rating != other.rating:
            return False

        return True


def load_hydra_content( parent):
    """Load all the content for this parent"""
    logging.info( 'load_hydra_content')
    logging.info( parent.key())
    query = HydraContent.all().ancestor( parent.key())
    result = []
    for content in query:
        result.append(content)

    return result

def create_hydra_content( kind, **kwargs):
    if not kind:
        raise Exception('invalid model object', 'None kind not valid')

    if not issubclass( kind, HydraContent):
        raise Exception('invalid model object',
                        'kind must be subclass of HydraContent')

    if not kwargs.get('owner'):
        raise Exception('invalid model object', 'no owner argument')

    if not kwargs.get('parent'):
        kwargs['parent'] = kwargs['owner']

    result = kind( **kwargs)
    return result

