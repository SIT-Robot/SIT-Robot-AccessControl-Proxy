import mitmproxy.http
from mitmproxy import ctx

from config import Config
from database import Database
from default_config import default_config
from lock_url_builder import build_shuaka_liu_cheng_url_by_config, build_remote_open_door_url_by_config


class Control:
    def __init__(self, config: Config):
        self.__config = config
        self.__db = Database()
        # 转发映射，可添加新的映射
        self.__method_to_url_map = {
            'ShuaKaLiuCheng': build_shuaka_liu_cheng_url_by_config(config.lock),
            'SaveRemoteOpenDoor': build_remote_open_door_url_by_config(config.lock),
        }

    # 根据method判断请求类型，返回相应的url
    def __is_open_or_register(self, method: str):
        if method is not None and method in self.__method_to_url_map:
            return self.__method_to_url_map[method]
        else:
            return None

    # 判断用户是否存在
    def __user_exists(self, c_no: str):
        try:
            self.__db.connect(self.__config.database)
            return self.__db.check_user_by_cno(c_no)
        except Exception as e:
            ctx.log.info(e)

    # 拦截请求
    def request(self, flow: mitmproxy.http.HTTPFlow):
        method: str = flow.request.query.get('Method')
        c_no: str = flow.request.query.get('KaHao')

        new_url = self.__is_open_or_register(method)
        if new_url is not None and self.__user_exists(c_no):
            flow.request.url = new_url


addons = [
    Control(default_config)
]
