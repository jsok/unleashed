from unleashed.resources import UnleashedResource
from unleashed.resources import fields


class Supplier(UnleashedResource):
    __endpoint__ = 'Suppliers'

    Guid = fields.FieldGuid(required=True)
    SupplierCode = fields.FieldString(required=True)
    SupplierName = fields.FieldString(required=True)
