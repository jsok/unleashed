from unleashed.resources import UnleashedResource
from unleashed.resources import fields


class ProductGroup(UnleashedResource):
    __endpoint__ = 'ProductGroups'

    Guid = fields.FieldGuid(required=True)
    GroupName = fields.FieldString(length=500)
