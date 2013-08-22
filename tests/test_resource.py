from mock import Mock
from nose.tools import (
    assert_true, assert_false,
    assert_equals,
    assert_is_none,
    assert_raises
)
from unittest import TestCase

from unleashed.fields import Field
from unleashed.resource import UnleashedResource


class DummyResource(UnleashedResource):
    def __init__(self):
        self.fields = [
            Field('Foo'),
            Field('Bar'),
            Field('Baz')
        ]
        super(DummyResource, self).__init__()


class UnleashedResourceTestCase(TestCase):
    def test_fields_accessible_as_attributes(self):
        r = DummyResource()

        assert_true(hasattr(r, 'Foo'))
        assert_true(hasattr(r, 'Bar'))
        assert_true(hasattr(r, 'Baz'))

    def test_from_dict(self):
        r = DummyResource()

        dict_value = {
            'Foo': 1,
            'Bar': 2,
            'Baz': 3
        }

        r.from_dict(dict_value)

        assert_equals(r.Foo.value, 1)
        assert_equals(r.Bar.value, 2)
        assert_equals(r.Baz.value, 3)

    def test_to_dict(self):
        r = DummyResource()
        r.Foo.set_value(1)
        r.Bar.set_value(2)
        r.Baz.set_value(3)

        dict_val = r.to_dict()

        assert_equals(
            dict_val,
            {
                'Foo': 1,
                'Bar': 2,
                'Baz': 3
            }
        )