import uuid

from unittest import TestCase
from nose.tools import assert_equals

from unleashed.auth import UnleashedAuth


UNLEASHED_URL = "https://api.unleashedsoftware.com/"
UNLEASHED_ID = str(uuid.uuid4())
UNLEASHED_KEY = 86 * 'x'


class UnleashedAuthTestCase(TestCase):
    def setUp(self):
        self.auth = UnleashedAuth(UNLEASHED_ID, UNLEASHED_KEY)

    def test_get_query_simple_request(self):
        url = UNLEASHED_URL + '/Customers?customerCode=ACME'
        assert_equals(self.auth.get_query(url), 'customerCode=ACME')

    def test_get_query_multiple_params_request(self):
        url = UNLEASHED_URL + '/Customers?customerCode=ACME&customerName=ACMECorp'
        assert_equals(self.auth.get_query(url), 'customerCode=ACME&customerName=ACMECorp')

    def test_get_query_empty_after_question_mark(self):
        url = UNLEASHED_URL + '/Customers?'
        assert_equals(self.auth.get_query(url), '')

    def test_get_query_no_question_mark(self):
        url = UNLEASHED_URL + '/Customers'
        assert_equals(self.auth.get_query(url), '')