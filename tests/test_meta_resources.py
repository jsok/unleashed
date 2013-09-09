from nose.tools import (
    assert_true, assert_false,
    assert_equals,
    assert_is_none,
    assert_raises
)
from unittest import TestCase

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