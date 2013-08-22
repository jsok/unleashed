from mock import Mock
from nose.tools import (
    assert_true, assert_false,
    assert_equals,
    assert_is_none,
    assert_raises
)
from unittest import TestCase

from unleashed.fields import Field, FieldEmbeddedResource, FieldValueException


class FieldTestCase(TestCase):
    def test_init_as_null(self):
        f = Field('test')
        assert_is_none(f.value)

    def test_set_value(self):
        f = Field('test')
        f.set_value('foo')
        assert_equals(f.value, 'foo')

    def test_to_dict_null(self):
        f = Field('test')
        assert_equals(f.to_dict(), {'test': None})

    def test_to_dict_null(self):
        f = Field('test')
        f.value = 'foo'
        assert_equals(f.to_dict(), {'test': 'foo'})


class FieldEmbeddedResourceTestCase(TestCase):
    def test_to_dict(self):
        resource = Mock()
        resource.to_dict = Mock(return_value=None)
        f = FieldEmbeddedResource('test', resource)
        d = f.to_dict()

        assert_equals(d, {'test': None})
        assert_true(resource.to_dict.called)

    def test_set_value(self):
        resource = Mock()
        resource.from_dict = Mock()
        f = FieldEmbeddedResource('test', resource)

        val = {'test': None}
        f.set_value(val)

        resource.from_dict.assert_called_once_with(val)

    def test_set_value_not_a_dict(self):
        resource = Mock()
        resource.from_dict = Mock()
        f = FieldEmbeddedResource('test', resource)

        with assert_raises(FieldValueException):
            f.set_value(['array', 'value'])

        assert_false(resource.from_dict.called)

    # TODO: Add some nested embedded resource tests