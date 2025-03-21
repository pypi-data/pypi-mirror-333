from .adapters import HTTPAdapter
from .models import Request, Response
from .exceptions import RequestException

class Session:
    """支持高级连接池的会话管理"""
    def __init__(self):
        self.adapters = {
            'http://': HTTPAdapter(),
            'https://': HTTPAdapter()
        }
        self.headers = {}
        self._closed = False

    def request(self, method, url, data=None, files=None, timeout=10, **kwargs):
        if self._closed:
            raise RequestException("Session has been closed")

        full_request = Request(
            method=method,
            url=url,
            headers=self.headers.copy(),
            data=data,
            files=files
        )

        try:
            scheme = 'https://' if url.startswith('https') else 'http://'
            adapter = self.adapters[scheme]
            raw_response = adapter.send(full_request, timeout=timeout)
            return Response(raw_response, url)
        except Exception as e:
            raise RequestException(f"Request failed: {str(e)}")

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, data=None, files=None, **kwargs):
        return self.request('POST', url, data=data, files=files, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request('PUT', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def close(self):
        """完全关闭会话和所有适配器"""
        if not self._closed:
            for adapter in self.adapters.values():
                adapter.close()
            self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()