import datetime
import re
import uuid


class FieldValueException(Exception):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __repr__(self):
        msg = "FieldValueException: Could not set value '{value}' of field {name}".format(
            value=self.value,
            name=self.field.__fieldname__
        )
        return msg


class FieldValueLengthException(FieldValueException):
    def __repr__(self):
        msg = "FieldValueLengthException: Value '{value}' exceeded maximum length of {length} for field {name}".format(
            value=self.value,
            length=self.field.max_length,
            name=self.field.__fieldname__
        )
        return msg


class Field(object):
    """
    Field is the base class for the fields which make up an
    Unleashed Resource.
    """
    __resourcefield__ = True

    def __init__(self, required=False):
        self.required = required
        self._value = self.default()

    def __repr__(self):
        return "<{name} {value}>".format(
            name=self.__class__.__name__,
            value=self.value
        )

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
        return self.value

    def get_value(self):
        return self._value

    def set_value(self, value):
        """
        Set the value of this Field.
        The simplest case is a simple assignment.
        More complex Fields may be given more complex structures as `val`.
        """
        self._value = value

    value = property(get_value, set_value)


class FieldGuid(Field):
    def default(self):
        return str(uuid.uuid4())


class FieldString(Field):
    def __init__(self, length=None, required=False):
        self.max_length = length
        super(FieldString, self).__init__(required=required)

    def set_value(self, value):
        if value and self.max_length and len(value) > self.max_length:
            raise FieldValueLengthException(self, value)
        self._value = value

    value = property(Field.get_value, set_value)


class FieldBoolean(Field):
    pass


class FieldNullableBoolean(Field):
    pass


class FieldInteger(Field):
    pass


class FieldNullableDecimal(Field):
    pass


class FieldNullableDateTime(Field):
    dt = re.compile(r'^/Date\((-?\d+)\)/')

    def _from_epoch_milliseconds(self, ms):
        """
        Convert given number of milliseconds from epoch to datetime.
        """
        value = datetime.datetime.fromtimestamp(ms/1000.00)
        return value

    def get_value(self):
        return self._value

    def set_value(self, value):
        try:
            groups = FieldNullableDateTime.dt.match(value)
            ms = int(groups.group(1))
        except AttributeError:
            raise FieldValueException(self, value)

        self._value = self._from_epoch_milliseconds(ms)

    value = property(get_value, set_value)


class FieldResourceList(Field):
    def __init__(self, field_type):
        self.field_type = field_type
        super(FieldResourceList, self).__init__(required=True)

    # def __repr__(self):
    #     return "<{name} length={length}>".format(
    #         name=self.__class__.__name__,
    #         length=len(self.value)
    #     )

    def default(self):
        return []

    def is_null(self):
        return self.value is []

    def to_dict(self):
        list_values = []
        for item in self.value:
            list_values.append(item.to_dict())

        return list_values

    def set_value(self, dict_list):
        self.value = []
        for d in dict_list:
            item = self.field_type()
            item.from_dict(d)
            self.value.append(item)