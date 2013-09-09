import json


__all__ = ['UnleashedResource', 'UnleashedResourceCollection']


class MetaResource(type):
    def __new__(mcs, name, bases, dct):
        """
        Looks for attributes whith a `__resourcefield__`  attribute and adds them to `__resourcefields__`.
        Replace the attribute with a property so its value can be directly accessed.
        """

        dct['__resourcefields__'] = {}

        for attr_name, attr in dct.iteritems():
            if hasattr(attr, '__resourcefield__') and attr.__resourcefield__:
                dct['__resourcefields__'][attr_name] = attr
                attr.__fieldname__ = attr_name
                attr.__parentresource__ = name

        for attr_name in dct['__resourcefields__'].iterkeys():
            del dct[attr_name]

            def getter(attr_name):
                def getter(cls):
                    return cls.__resourcefields__[attr_name].value
                return getter

            def setter(attr_name):
                def setter(cls, value):
                    cls.__resourcefields__[attr_name].value = value
                return setter

            dct[attr_name] = property(getter(attr_name), setter(attr_name))

        return super(MetaResource, mcs).__new__(mcs, name, bases, dct)

    def __init__(cls, name, bases, dct):
        cls.guess_endpoint(name, dct)
        super(MetaResource, cls).__init__(name, bases, dct)

    def guess_endpoint(cls, name, dct):
        """
        If the class does not specify an `__endpoint__`, derive one from its name.
        """
        if '__endpoint__' not in dct:
            cls.__endpoint__ = name
        elif hasattr(cls, '__endpoint__') and cls.__endpoint__ is None:
            cls.__endpoint__ = name


class UnleashedResource(object):
    __metaclass__ = MetaResource
    __endpoint__ = None

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

        for field, value in dict_val.iteritems():
            if hasattr(self, field):
                setattr(self, field, value)

    def to_dict(self):
        """
        Convert the Resource to dictionary representation.
        (Suitable for JSON encoding).
        """
        out = {}
        for name, field in self.__resourcefields__.iteritems():
            out.update({name: getattr(self, name)})
            #out.update({name: field.to_dict()})

        # Reduce dict to a single null if all it's values are None
        # if all(map(lambda v: v is None, out.itervalues())):
        #     out = None

        return out

    def to_json(self):
        out = self.to_dict()
        return json.dumps(out)


class OldUnleashedResource(object):
    """
    Base class for a resource which is accessible through the Unleashed API.
    """
    # The API endpoint this resource exists at
    ENDPOINT = ''

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

    def set_guid(self, guid):
        raise NotImplementedError("Resource does not define a Guid field")

    def add__get_query(self):
        raise NotImplementedError("Resource does not define an endpoint to add or update")

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


class UnleashedResourceCollection(UnleashedResource):
    """
    Base class for a resource listing returned by the Unleashed API.
    """

    fields = []
    COLLECTION_FOR = UnleashedResource

    def __init__(self, paginated=False):
        import unleashed.fields as fields

        self.fields = [fields.FieldResourceList("Items", self.COLLECTION_FOR)]

        if paginated:
            from unleashed.resources.pagination import Pagination

            self.fields.append(fields.FieldEmbeddedResource("Pagination", Pagination()))

        super(UnleashedResourceCollection, self).__init__()