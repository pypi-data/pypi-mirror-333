import http.client
import ssl
import threading
import time
from collections import deque
from urllib.parse import urlparse
from .exceptions import PoolClosedError

class ConnectionWrapper:
    """连接包装器，记录连接状态"""
    def __init__(self, conn, last_used):
        self.conn = conn
        self.last_used = last_used
        self.in_use = False

class AdvancedConnectionPool:
    """高级连接池实现"""
    def __init__(self, max_size=10, idle_timeout=60, max_retries=3):
        self._pools = {}  # {(host, port, is_https): deque}
        self.max_size = max_size
        self.idle_timeout = idle_timeout
        self.max_retries = max_retries
        self._lock = threading.Lock()
        self._closed = False
        self._cleanup_thread = threading.Thread(target=self._cleanup, daemon=True)
        self._cleanup_thread.start()

    def _create_connection(self, host, port, is_https, timeout):
        """创建新连接"""
        if is_https:
            context = ssl.create_default_context()
            return http.client.HTTPSConnection(
                host=host,
                port=port or 443,
                timeout=timeout,
                context=context
            )
        else:
            return http.client.HTTPConnection(
                host=host,
                port=port or 80,
                timeout=timeout
            )

    def get_connection(self, host, port, is_https, timeout):
        """获取可用连接"""
        if self._closed:
            raise PoolClosedError("Connection pool is closed")

        key = (host, port, is_https)
        
        with self._lock:
            pool = self._pools.get(key, deque())
            
            # 清理过期连接
            while pool:
                conn_wrapper = pool[0]
                if self._is_expired(conn_wrapper):
                    conn_wrapper.conn.close()
                    pool.popleft()
                else:
                    break
            
            # 尝试复用连接
            for _ in range(len(pool)):
                conn_wrapper = pool.popleft()
                if not conn_wrapper.in_use and self._is_usable(conn_wrapper.conn):
                    conn_wrapper.in_use = True
                    conn_wrapper.last_used = time.time()
                    self._pools[key] = pool
                    return conn_wrapper.conn
                else:
                    conn_wrapper.conn.close()
            
            # 创建新连接
            if len(pool) < self.max_size:
                try:
                    conn = self._create_connection(host, port, is_https, timeout)
                    conn_wrapper = ConnectionWrapper(conn, time.time())
                    conn_wrapper.in_use = True
                    pool.append(conn_wrapper)
                    self._pools[key] = pool
                    return conn
                except Exception as e:
                    raise ConnectionError(f"Connection failed: {str(e)}")
            
            raise ConnectionError("Connection pool exhausted")

    def release_connection(self, conn, host, port, is_https):
        """释放连接回池"""
        if self._closed:
            conn.close()
            return

        key = (host, port, is_https)
        
        with self._lock:
            if key not in self._pools:
                self._pools[key] = deque()
            
            pool = self._pools[key]
            for wrapper in pool:
                if wrapper.conn == conn:
                    wrapper.in_use = False
                    wrapper.last_used = time.time()
                    return
            
            # 如果不在池中且池未满，则重新添加
            if len(pool) < self.max_size:
                pool.append(ConnectionWrapper(conn, time.time()))
            else:
                conn.close()

    def close(self):
        """关闭所有连接"""
        with self._lock:
            self._closed = True
            for key in self._pools:
                pool = self._pools[key]
                while pool:
                    conn_wrapper = pool.popleft()
                    conn_wrapper.conn.close()
            self._pools.clear()

    def _is_usable(self, conn):
        """检查连接是否可用"""
        try:
            conn.request("HEAD", "/", headers={"Connection": "keep-alive"})
            resp = conn.getresponse()
            resp.read()
            return resp.status < 500
        except:
            return False

    def _is_expired(self, conn_wrapper):
        """检查连接是否过期"""
        return (time.time() - conn_wrapper.last_used) > self.idle_timeout

    def _cleanup(self):
        """后台清理线程"""
        while not self._closed:
            time.sleep(self.idle_timeout / 2)
            with self._lock:
                for key in list(self._pools.keys()):
                    pool = self._pools[key]
                    
                    # 移除过期连接
                    expired = []
                    for i, wrapper in enumerate(pool):
                        if self._is_expired(wrapper):
                            expired.append(i)
                    
                    for i in reversed(expired):
                        wrapper = pool[i]
                        wrapper.conn.close()
                        del pool[i]
                    
                    # 移除空池
                    if not pool:
                        del self._pools[key]