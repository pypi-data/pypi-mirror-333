import requests
from tenacity import retry, stop_after_attempt, wait_exponential


class HttpClient:
    def __init__(self, base_url=None, headers=None, timeout=60):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint
        headers = {**self.headers, **kwargs.pop('headers', {})}
        resp = requests.request(method, url, headers=headers, timeout=self.timeout, **kwargs)
        resp.raise_for_status()  # 抛出HTTP错误
        return resp.json()  # 假设返回的是JSON数据

    def get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        return self._request('POST', endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint, data=None, json=None, **kwargs):
        return self._request('PUT', endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)
