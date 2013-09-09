from unleashed.resources import UnleashedResource
from unleashed.resources import fields


class Pagination(UnleashedResource):
    NumberOfItems = fields.FieldInteger()
    PageSize = fields.FieldInteger()
    PageNumber = fields.FieldInteger()
    NumberOfPages = fields.FieldInteger()