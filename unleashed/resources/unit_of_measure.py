from unleashed.resources import UnleashedResource
from unleashed.resources import fields


class UnitOfMeasure(UnleashedResource):
    __endpoint__ = 'UnitOfMeasures'

    Guid = fields.FieldGuid(required=True)
    Name = fields.FieldString(length=20, required=True)