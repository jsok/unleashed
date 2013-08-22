import binascii
import hashlib
import hmac

import requests.auth


class UnleashedAuth(requests.auth.AuthBase):
        """
        Unleashed Authentication protocol implemented as an requests AuthBase.
        Usage:
            requests.get(auth=UnleashedAuth(id, key))

        We must sign according to the API docs:
        Only the query parameters portion of the URL is used in calculating the signature

        e.g. for the request:
            /Customers?customerCode=ACME

        calculate the signature of the string:
            'customerCode=ACME'

        Do not include the endpoint name in the method signature.
        Do not include the query indicator '?' in the method signature.

        For more details see: https://api.unleashedsoftware.com/AuthenticationHelp
        """

        def __init__(self, api_id, api_key):
            self.api_id = api_id
            self.api_key = api_key

        def get_query(self, url):
            parts = url.split('?')
            if len(parts) > 1:
                return parts[1]
            else:
                return ""

        def __call__(self, r):
            query = self.get_query(r.url)

            hashed = hmac.new(self.api_key, query, hashlib.sha256)
            signature = binascii.b2a_base64(hashed.digest())[:-1]

            r.headers['api-auth-signature'] = signature
            r.headers['api-auth-id'] = self.api_id
            return r