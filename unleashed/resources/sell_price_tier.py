from unleashed.resources import UnleashedResource
from unleashed.resources import fields


class SellPriceTier(UnleashedResource):
    Name = fields.FieldString()
    Value = fields.FieldString()

    def to_dict(self):
        if not self.Value:
            return None

        return super(SellPriceTier, self).to_dict()
