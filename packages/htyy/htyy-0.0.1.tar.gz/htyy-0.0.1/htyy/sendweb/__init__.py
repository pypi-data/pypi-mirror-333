from .api import request, get, post, put, delete
from .sessions import Session
from .exceptions import RequestException, HTTPError, Timeout, ConnectionError, FileUploadError

__version__ = '2.0.0'
__all__ = [
    'request',
    'get',
    'post',
    'put',
    'delete',
    'Session',
    'RequestException',
    'HTTPError',
    'Timeout',
    'ConnectionError',
    'FileUploadError'
]