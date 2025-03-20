import requests

from .types import JSONData

class Requester(object):

    def __init__(self, api_key: str) -> None:
        self.headers = {"Authorization": f"Api-Key {api_key}"}

    @property
    def post(self, url: str, data: JSONData):
        return self._factory(method="post")(url, data)

    @property
    def get(self, url: str, data: JSONData):
        return self._factory(method="get")(url, data)

    def _factory(self, method: Literal["post", "get"]):
        if method.lower() == "post":
            return self._post
        return self._get

    def _post(self, url: str, data: JSONData):
        response = requests.post(url, data=data, format=json, headers=self.headers)
        self._catch_status(response.status_code)
        return response
                
    @staticmethod
    def _catch_status(status: requestes.Response) -> requests.HTTPError:
        pass

