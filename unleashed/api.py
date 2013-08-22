import requests

from auth import UnleashedAuth


class UnleashedApi(object):
    """
    Unleashed API client library.
    """

    def __init__(self, api_url, api_id, api_key):
        self.api_url = api_url
        self.auth = UnleashedAuth(api_id, api_key)

    def _get_request(self, method, params=None):
        params = params or {}
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
        }
        resp = requests.get(
            self.api_url + '/' + method,
            headers=headers,
            params=params,
            auth=self.auth
        )
        return resp

    def _post_request(self, method, body):
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
        }
        resp = requests.post(
            self.api_url + '/' + method,
            body,
            headers=headers,
            auth=self.auth
        )
        return resp