from .sessions import Session
import os

def request(method, url, **kwargs):
    with Session() as session:
        return session.request(method, url, **kwargs)

def get(url, params=None, **kwargs):
    return request('GET', url, params=params, **kwargs)

def post(url, data=None, **kwargs):
    return request('POST', url, data=data, **kwargs)

def put(url, data=None, **kwargs):
    return request('PUT', url, data=data, **kwargs)

def delete(url, **kwargs):
    return request('DELETE', url, **kwargs)

def stream_upload(url, file_path, chunk_size=1024*1024):
    """流式大文件上传"""
    def file_generator():
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(os.path.getsize(file_path))
    }

    return put(
        url,
        data=file_generator(),
        headers=headers
    )