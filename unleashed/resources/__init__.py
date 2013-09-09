import json


__all__ = ['UnleashedResource', 'UnleashedResourceCollection']


class MetaResource(type):
    def __new__(mcs, name, bases, dct):
        """
        Looks for attributes whith a `__resourcefield__`  attribute and adds them to `__resourcefields__`.
        Replace the attribute with a property so its value can be directly accessed.
        """

        dct['__resourcefields__'] = {}
        dct['__embeddedresources__'] = {}

        for attr_name, attr in dct.iteritems():
            if hasattr(attr, '__resourcefield__') and attr.__resourcefield__:
                dct['__resourcefields__'][attr_name] = attr
                attr.__fieldname__ = attr_name
                attr.__parentresource__ = name
            elif hasattr(attr, '__metaclass__') and attr.__metaclass__ == mcs:
                dct['__embeddedresources__'][attr_name] = attr

        return super(MetaResource, mcs).__new__(mcs, name, bases, dct)

    def __init__(cls, name, bases, dct):
        cls.guess_endpoint()
        cls.convert_fields()
        cls.convert_embedded_resources()
        super(MetaResource, cls).__init__(name, bases, dct)

    def guess_endpoint(cls):
        """
        If the class does not specify an `__endpoint__`, derive one from its name.
        """

        # Inheriting __endpoint__ is not enough, ensure it's in the class __dict__.
        # Otherwise it will also inherit it's base class' endpoint.
        # (Probably not what you want)
        if '__endpoint__' in cls.__dict__ and cls.__endpoint__ is not None:
            return
        else:
            cls.__endpoint__ = cls.__name__

    def convert_fields(cls):
        """
        Convert all the collected resource fields into class properties.
        """

        for attr_name in cls.__resourcefields__.iterkeys():
            def getter(attr_name):
                def getter(cls):
                    return cls.__resourcefields__[attr_name].value

                return getter

            def setter(attr_name):
                def setter(cls, value):
                    cls.__resourcefields__[attr_name].value = value

                return setter

            setattr(cls, attr_name, property(getter(attr_name), setter(attr_name)))

    def convert_embedded_resources(cls):
        """
        Convert all the collected embedded resources into class properties.
        """

        for attr_name in cls.__embeddedresources__.iterkeys():
            def getter(attr_name):
                def getter(cls):
                    return cls.__embeddedresources__[attr_name]

                return getter

            def setter(attr_name):
                def setter(cls, value):
                    # Allow property to be set from dict or instance of the resource
                    if isinstance(value, dict):
                        cls.__embeddedresources__[attr_name].from_dict(value)
                    else:
                        cls.__embeddedresources__[attr_name] = value

                return setter

            setattr(cls, attr_name, property(getter(attr_name), setter(attr_name)))


class UnleashedResource(object):
    __metaclass__ = MetaResource

    # Override if necessary
    __endpoint__ = None

    # Created by metaclass
    __resourcefields__ = {}
    __embeddedresources__ = {}

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
            out.update({name: field.to_dict()})

        for name, resource in self.__embeddedresources__.iteritems():
            out.update({name: resource.to_dict()})

        # Reduce dict to a single null if all it's values are None
        if all(map(lambda v: v is None, out.itervalues())):
            out = None

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