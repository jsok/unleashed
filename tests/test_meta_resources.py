from nose.tools import (
    assert_true, assert_false,
    assert_equals,
    assert_is_none,
    assert_raises
)
from unittest import TestCase


from unleashed.resources.fields import Field
from unleashed.resources import UnleashedResource


class EndpointTestCase(TestCase):
    def test_endpoint_autocreated(self):
        class NoEndpoint(UnleashedResource):
            pass

        res = NoEndpoint()
        assert_equals(res.__endpoint__, 'NoEndpoint')

    def test_endpoint_is_none(self):
        class NoneEndpoint(UnleashedResource):
            __endpoint__ = None

        res = NoneEndpoint()
        assert_equals(res.__endpoint__, 'NoneEndpoint')

    def test_endpoint_not_overwritten(self):
        class HasEndpoint(UnleashedResource):
            __endpoint__ = 'original'

        res = HasEndpoint()
        assert_equals(res.__endpoint__, 'original')

    def test_endpoint_not_inherited(self):
        class BaseEndPoint(UnleashedResource):
            __endpoint__ = 'base'

        class MyEndpoint(BaseEndPoint):
            pass

        res = MyEndpoint()
        assert_equals(res.__endpoint__, 'MyEndpoint')


class DummyEmbeddedResource(UnleashedResource):
    Qux = Field()
    Fred = Field()


class DummyResource(UnleashedResource):
    __endpoint__ = "MyEndPoint"

    Foo = Field()
    Bar = Field()
    Baz = DummyEmbeddedResource()


class ResourceFieldsTestCase(TestCase):
    def test_fields_accessible_as_attributes(self):
        r = DummyResource()

        assert_true(hasattr(r, 'Foo'))
        assert_true(hasattr(r, 'Bar'))
        assert_true(hasattr(r, 'Baz'))
        assert_true(hasattr(r.Baz, 'Qux'))
        assert_true(hasattr(r.Baz, 'Fred'))

    def test_fields_settable_as_attributes(self):
        r = DummyResource()
        r.Foo = 42
        r.Bar = True

        assert_equals(r.Foo, 42)
        assert_equals(r.Bar, True)

    def test_from_dict(self):
        r = DummyResource()

        dict_value = {
            'Foo': 1,
            'Bar': 2,
            'Baz': {
                'Qux': 3,
                'Fred': 4
            }
        }

        r.from_dict(dict_value)

        assert_equals(r.Foo, 1)
        assert_equals(r.Bar, 2)

    def test_to_dict(self):
        r = DummyResource()
        r.Foo = 1
        r.Bar = 2
        r.Baz.Qux = 3
        r.Baz.Fred = 4

        dict_val = r.to_dict()

        assert_equals(
            dict_val,
            {
                'Foo': 1,
                'Bar': 2,
                'Baz': {
                    'Qux': 3,
                    'Fred': 4
                }
            }
        )

    def test_to_dict_overwrite_embedded(self):
        r = DummyResource()
        r.Foo = 1
        r.Bar = 2

        baz = DummyEmbeddedResource()
        baz.Qux = 3
        baz.Fred = 4
        r.Baz = baz

        dict_val = r.to_dict()

        assert_equals(
            dict_val,
            {
                'Foo': 1,
                'Bar': 2,
                'Baz': {
                    'Qux': 3,
                    'Fred': 4
                }
            }
        )