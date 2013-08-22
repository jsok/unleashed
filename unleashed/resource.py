import json


class UnleashedResource(object):
    """
    Base class for a resource which is accessible through the Unleashed API.
    """

    fields = []

    def __init__(self):
        """
        The resource's fields are described as a list of Field instances:
        self.fields = [
            Field('Field1'),
            Field('Field2'),
            ...
        ]

        Resource fields are accessible by name as class attributes:
        self.Field1.set_value('foo')
        """

        for field in self.fields:
            setattr(self, field.name, field)

    def __repr__(self):
        return json.dumps(
            self.to_dict(),
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )

    def from_dict(self, dict_val):
        """
        Set all the resource's field values from a dictionary.
        """
        if not dict_val:
            return

        for field_name, val in dict_val.iteritems():
            if hasattr(self, field_name):
                field = getattr(self, field_name)
                field.set_value(val)

    def to_dict(self):
        """
        Convert the Resource to dictionary representation.
        (Suitable for JSON encoding).
        """
        out = {}
        for field in self.fields:
            out.update(field.to_dict())

        # Reduce dict to a single null if all it's values are None
        if all(map(lambda v: v is None, out.itervalues())):
            out = None

        return out

    def to_json(self):
        out = self.to_dict()
        return json.dumps(out)