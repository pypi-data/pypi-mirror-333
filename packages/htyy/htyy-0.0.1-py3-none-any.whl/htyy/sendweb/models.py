import mimetypes
import os
from io import BufferedReader
from .exceptions import HTTPError, FileUploadError

class Request:
    """增强型请求封装，支持混合数据和文件上传"""
    def __init__(self, method, url, headers=None, data=None, files=None):
        self.method = method.upper()
        self.url = url
        self.headers = headers or {}
        self.data = None
        self.files = files

        self._prepare_request(data, files)

    def _prepare_request(self, data, files):
        if files:
            if data:
                # 混合表单数据和文件
                self._prepare_multipart(data, files)
            else:
                # 纯文件上传
                self._prepare_multipart(files=files)
        elif data:
            # 普通表单数据
            self.data = self._encode_data(data)
            if 'Content-Type' not in self.headers:
                self.headers['Content-Type'] = 'application/x-www-form-urlencoded'

    def _encode_data(self, data):
        if isinstance(data, (bytes, str)):
            return data.encode('utf-8') if isinstance(data, str) else data
        elif isinstance(data, dict):
            return '&'.join(
                f"{k}={v}" for k, v in data.items()
            ).encode('utf-8')
        else:
            raise ValueError("Unsupported data type")

    def _prepare_multipart(self, data=None, files=None):
        boundary = f"--------{os.urandom(16).hex()}"
        self.headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        parts = []

        # 添加表单数据
        if data:
            for name, value in data.items():
                part = (
                    f'--{boundary}\r\n'
                    f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                    f'{value}\r\n'
                ).encode('utf-8')
                parts.append(part)

        # 添加文件数据
        if files:
            for name, file_info in files.items():
                filename, fileobj = self._parse_file_info(file_info)
                content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

                part_header = (
                    f'--{boundary}\r\n'
                    f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
                    f'Content-Type: {content_type}\r\n\r\n'
                ).encode('utf-8')

                parts.append(part_header)
                parts.append(self._read_file(fileobj))
                parts.append(b'\r\n')

        parts.append(f'--{boundary}--\r\n'.encode('utf-8'))
        self.data = b''.join(parts)

    def _parse_file_info(self, file_info):
        if isinstance(file_info, (tuple, list)):
            if len(file_info) >= 2:
                return file_info[0], file_info[1]
            else:
                raise FileUploadError("Invalid file tuple format")
        elif hasattr(file_info, 'read'):
            filename = getattr(file_info, 'name', 'file.bin')
            return os.path.basename(filename), file_info
        elif isinstance(file_info, str):
            return os.path.basename(file_info), open(file_info, 'rb')
        else:
            raise FileUploadError("Unsupported file type")

    def _read_file(self, fileobj):
        try:
            if isinstance(fileobj, str):
                with open(fileobj, 'rb') as f:
                    return f.read()
            elif hasattr(fileobj, 'read'):
                pos = fileobj.tell()
                content = fileobj.read()
                fileobj.seek(pos)  # 保持文件指针位置
                return content
            else:
                raise FileUploadError("Cannot read file object")
        except Exception as e:
            raise FileUploadError(f"File read error: {str(e)}")

class Response:
    """增强型响应处理"""
    def __init__(self, raw_response, url):
        self.status_code = raw_response['status']
        self.headers = raw_response['headers']
        self.url = url
        self._content = raw_response['body']
        self._text = None
        self._json = None

    @property
    def text(self):
        if self._text is None:
            charset = self._detect_charset()
            self._text = self._content.decode(charset, errors='replace')
        return self._text

    def json(self):
        if self._json is None:
            import json
            try:
                self._json = json.loads(self.text)
            except ValueError as e:
                raise ValueError("Invalid JSON response") from e
        return self._json

    def _detect_charset(self):
        content_type = self.headers.get('Content-Type', '')
        if 'charset=' in content_type:
            return content_type.split('charset=')[-1].split(';')[0].strip()
        return 'utf-8'

    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            raise HTTPError(
                f"{self.status_code} Client Error for url: {self.url}",
                response=self
            )