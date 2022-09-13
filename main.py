import mitmproxy.http
from mitmproxy import ctx
from database import *


@Singleton
class Control:

    def __init__(self):
        self.__db = DataBase()
        # 转发映射，可添加新的映射
        self.__method_to_url_map = {
            'ShuaKaLiuCheng': 'http://210.35.98.178:7101//LMWeb/WebApi/HCommon.ashx?KaHao=515FF572&MacID=28'
                              '%3A52%3AF9%3A18%3A84%3A67&Method=ShuaKaLiuCheng ',
            'SaveRemoteOpenDoor': 'http://210.35.98.178:7101/LMWeb/WebApi/HShiYanShi.ashx?Method'
                                  '=SaveRemoteOpenDoor&ShiYanShiID=&KaHao=515FF572&MacID=28%3A52%3AF9%3A18'
                                  '%3A84%3A67 '}

    # 根据method判断请求类型，返回相应的url
    def __is_open_or_register(self, method: str):
        if method is not None and method in self.__method_to_url_map:
            return self.__method_to_url_map[method]
        else:
            return None

    # 判断用户是否存在
    def __user_exists(self, c_no: str):
        try:
            self.__db.connect()
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
    Control()
]
