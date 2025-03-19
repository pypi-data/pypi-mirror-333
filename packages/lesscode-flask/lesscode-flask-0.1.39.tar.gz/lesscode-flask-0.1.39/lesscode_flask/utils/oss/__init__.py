import os
from io import BytesIO

from lesscode_flask.utils.helpers import app_config
from lesscode_flask.utils.oss.ks3_oss import Ks3Oss


class CommonOss:
    def __init__(self, storage_type, data_type="stream", **kwargs):
        """
        初始化OSS
        Args:
            storage_type (str): 存储类型，目前支持ks3和file
            data_type (str): 数据类型，目前支持stream和file_path
            storage_config (dict): 存储配置，目前支持ks3和file,file_name
        """
        self.storage_type = storage_type
        self.data_type = data_type
        self.storage_config = kwargs.get("storage_config", {}) if kwargs.get("storage_config", {}) else app_config.get(
            "STORAGE_CONFIG", {})

    def _save(self, key, io_stream: BytesIO = None, file_path: str = None):
        file_url_obj = dict()
        if self.storage_type == "ks3":
            if self.data_type == "stream":
                storage_config = self.storage_config or dict()
                ks3 = Ks3Oss(**storage_config)
                url = ks3.save(key=key, string_data=io_stream.getvalue(), content_type="string", policy="public-read")
                file_url_obj = {"key": key, "url": url}
            elif self.data_type == "file_path":
                storage_config = self.storage_config or dict()
                ks3 = Ks3Oss(**storage_config)
                url = ks3.save(key=key, filename=file_path, content_type="filename", policy="public-read")
                file_url_obj = {"key": key, "url": url}
        elif self.storage_type == "file":
            storage_path = ""
            storage_dir = self.storage_config.get("storage_dir", "")
            if not storage_dir:
                storage_dir = app_config.get("STORAGE_DIR")
            if not storage_dir:
                raise Exception("storage_dir is empty")
            if self.data_type == "stream":
                if "\\" in key:
                    key_list = key.split("\\")
                elif "/" in key:
                    key_list = key.split("/")
                else:
                    key_list = [key]
                storage_path = storage_dir
                if key_list:
                    for k in key_list:
                        storage_path = os.path.join(storage_path, k)
                dir_path = os.path.dirname(storage_path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
            elif self.data_type == "file_path":
                with open(file_path, 'rb') as infile:
                    io_stream = BytesIO(infile.read())
            if storage_path:
                with open(storage_path, 'wb') as outfile:
                    outfile.write(io_stream.getvalue())
                file_url_obj = {"key": key, "url": storage_path}
        return file_url_obj

    def upload(self, **kwargs):
        """上传文件
        Args:
            files (list): 文件列表 可以是文件流列表，也可以是字典列表，字典格式为{"key":"文件key，可以是带路径的文件","stream":"文件流"}
        Returns:
            file_url_list: 文件url列表[{"key":"文件key，可以是带路径的文件","url":"本地文件存储的文件的全路径，对象存储，存放的是文件的下载地址"}]
        """
        file_url_list = []
        files = kwargs.get("files", [])
        if not files:
            raise Exception("files is empty")
        if self.data_type == "stream":
            for f in files:
                if not isinstance(f, dict):
                    key = f.filename
                    stream = f.stream.read()
                    file_stream = BytesIO(stream)
                else:
                    key = f.get("key", "")
                    _steam = f.get("stream")
                    stream = _steam.stream.read()
                    file_stream = BytesIO(stream)
                file_url_obj = self._save(key=key, io_stream=file_stream)
                file_url_list.append(file_url_obj)

        elif self.data_type == "file_path":
            for f in files:
                if not isinstance(f, dict):
                    if "\\" in f:
                        file_name = f.split("\\")[-1]
                    elif "/" in f:
                        file_name = f.split("/")[-1]
                    else:
                        file_name = f
                    key = file_name
                    _file_path = f
                else:
                    key = f.get("key", "")
                    _file_path = f.get("file_path")
                file_url_obj = self._save(key=key, file_path=_file_path)
                file_url_list.append(file_url_obj)
        return file_url_list

    def download(self, key):
        """下载文件，返回文件流
        Args:
            key (str): 上面接口返回的文件key
        Returns:
            file_stream: 文件流
        """
        if self.storage_type == "ks3":
            storage_config = self.storage_config or dict()
            ks3 = Ks3Oss(**storage_config)
            return ks3.get_file(key)
        if self.storage_type == "file":
            storage_dir = self.storage_config.get("storage_dir", "")
            if not storage_dir:
                storage_dir = app_config.get("STORAGE_DIR")
            if "\\" in key:
                key_list = key.split("\\")
            elif "/" in key:
                key_list = key.split("/")
            else:
                key_list = [key]
            file_path = storage_dir
            if key_list:
                for k in key_list:
                    file_path = os.path.join(file_path, k)
            with open(file_path, 'rb') as f:
                return f.read()
