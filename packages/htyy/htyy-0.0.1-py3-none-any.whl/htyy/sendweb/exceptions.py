class RequestException(Exception):
    """所有请求异常的基类"""

class HTTPError(RequestException):
    """HTTP 错误响应 (4xx, 5xx)"""

class Timeout(RequestException):
    """请求超时异常"""

class ConnectionError(RequestException):
    """网络连接错误"""

class FileUploadError(RequestException):
    """文件上传错误"""

class PoolClosedError(RequestException):
    """连接池已关闭异常"""