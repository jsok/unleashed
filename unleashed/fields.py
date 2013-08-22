import uuid


class FieldValueException(Exception):
    pass


class Field(object):
    """
    Field is the base class for the fields which make up an
    Unleashed Resource.
    """
    def __init__(self, name, required=False):
        self.name = name
        self.required = required
        self.value = self.default()

    def __repr__(self):
        return "<{name} {value}>".format(
            name=self.__class__.__name__,
            value=self.value
        )

    def get_name(self):
        return self.name

    def default(self):
        """
        The default value of this field.
        In JSON: None -> null
        """
        return None

    def is_null(self):
        return self.value is None

    def to_dict(self):
        """
        Convert this Field to it's Dictionary representation.
        """
        return {self.name: self.value}

    def set_value(self, val):
        """
        Set the value of this Field.
        The simplest case is a simple assignment.
        More complex Fields may be given more complex structures as `val`.
        """
        self.value = val


class FieldGuid(Field):
    def default(self):
        return str(uuid.uuid4())


class FieldString(Field):
    pass


class FieldBoolean(Field):
    pass


class FieldNullableBoolean(Field):
    pass


class FieldNullableDecimal(Field):
    pass


class FieldEmbeddedResource(Field):
    def __init__(self, name, resource, required=False):
        """
        A Field which Embeds a Resource.
        The value of this field is a reference to a resource (which
        may in turn have more Fields inside of it).
        """
        super(FieldEmbeddedResource, self).__init__(name, required=required)
        self.value = resource

    def to_dict(self):
        """
        Wrap the dictionary representation of the resource.
        """
        return {self.name: self.value.to_dict()}

    def set_value(self, val):
        """
        Set the value of the underlying resource from the given value.
        """
        if not isinstance(val, dict):
            raise FieldValueException("Cannot set value of FieldEmbeddedResource from non-dict type")
        # TODO: Support setting from an instance of the resource
        # elif isinstance(val, type(self.value)):
        #     self.value = val

        self.value.from_dict(val)


class FieldResourceList(Field):
    def __init__(self, name, field_type):
        self.field_type = field_type
        super(FieldResourceList, self).__init__(name, required=True)

    def __repr__(self):
        return "<{name} length={length}>".format(
            name=self.__class__.__name__,
            length=len(self.value)
        )

    def default(self):
        return []

    def is_null(self):
        return self.value is []

    def to_dict(self):
        list_values = []
        for item in self.value:
            list_values.append(item.to_dict())

        return {self.name: list_values}

    def set_value(self, dict_list):
        self.value = []
        for d in dict_list:
            item = self.field_type()
            item.from_dict(d)
            self.value.append(item)