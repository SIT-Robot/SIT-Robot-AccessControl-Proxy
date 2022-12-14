import _io
import json
import config


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


def JsonDecodeToConfig(file_name: str):
    fp = open(file_name)
    config_dict = json.load(fp=fp)
    return config.Config(database=config.DatabaseConfig(**config_dict.get("database")),
                         lock=config.LockConfig(**config_dict.get("lock")))


# 指明util模块中需要导出的对象
__all__ = [
    "Singleton",
    "JsonDecodeToConfig"
]
