from google.appengine.ext import db

import hydracontent

class PDFContent(hydracontent.HydraContent):
    """The base type for any entity in a gaming session"""
    file = db.ReferenceProperty(collection_name='file')

    def clone(self, newOwner):
        result = super(PDFContent, self).clone( newOwner)

        result.file = self.file

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if self.file != other.file:
            # key compare
            return False

        return super(PDFContent, self).__eq__(other)
