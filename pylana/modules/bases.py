import abc
import requests


class _API(abc.ABC):

    headers = dict()

    def get(self, url, additional_headers=None, **kwargs):
        headers = {**self.headers, **(additional_headers or dict())}
        resp = requests.get(url, headers=headers, **kwargs)
        resp.raise_for_status()
        return resp

    def post(self, url, additional_headers=None, **kwargs):
        headers = {**self.headers, **(additional_headers or dict())}
        resp = requests.post(url, headers=headers, **kwargs)
        resp.raise_for_status()
        return resp
