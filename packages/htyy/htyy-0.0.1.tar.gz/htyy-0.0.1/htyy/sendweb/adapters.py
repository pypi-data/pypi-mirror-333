import http
from urllib.parse import urlparse
from .pool import AdvancedConnectionPool
from .exceptions import ConnectionError, Timeout, PoolClosedError

class BaseAdapter:
    """传输适配器基类"""
    def __init__(self, pool=None):
        self.pool = pool or AdvancedConnectionPool()
        self._closed = False

    def send(self, request, timeout=10):
        raise NotImplementedError

    def close(self):
        if not self._closed:
            self.pool.close()
            self._closed = True

class HTTPAdapter(BaseAdapter):
    """增强型HTTP适配器"""
    def send(self, request, timeout=10):
        if self._closed:
            raise PoolClosedError("Adapter has been closed")

        parsed = urlparse(request.url)
        is_https = parsed.scheme == 'https'
        host = parsed.hostname
        port = parsed.port

        try:
            conn = self.pool.get_connection(
                host=host,
                port=port,
                is_https=is_https,
                timeout=timeout
            )

            path = parsed.path or '/'
            if parsed.query:
                path += '?' + parsed.query

            headers = request.headers.copy()
            if request.data and 'Content-Length' not in headers:
                headers['Content-Length'] = str(len(request.data))

            conn.request(
                method=request.method,
                url=path,
                body=request.data,
                headers=headers
            )

            response = conn.getresponse()
            resp_data = {
                'status': response.status,
                'headers': dict(response.getheaders()),
                'body': response.read()
            }

            # 根据Keep-Alive决定是否释放连接
            keep_alive = response.getheader('Connection', '').lower() == 'keep-alive'
            if keep_alive:
                self.pool.release_connection(conn, host, port, is_https)
            else:
                conn.close()

            return resp_data

        except (http.client.HTTPException, OSError) as e:
            conn.close()
            raise ConnectionError(f"Connection failed: {str(e)}")
        except TimeoutError:
            raise Timeout("Request timed out")
        except Exception as e:
            conn.close()
            raise