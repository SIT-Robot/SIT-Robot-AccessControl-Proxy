import datetime
import pymysql
from util import Singleton

host = '101.43.65.22'
port = 8978
user = 'root'
passwd = 'rootroot'
db = 'opendoor'


@Singleton
class DataBase:
    def __init__(self):
        self.__conn = None
        self.__cursor = None
        self.__host = host
        self.__port = port
        self.__user = user
        self.__passwd = passwd
        self.__db = db

    # 连接数据库
    def connect(self):
        self.__conn = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, password=self.__passwd,
                                      db=self.__db)
        self.__cursor = self.__conn.cursor()

    # 关闭数据库
    def close(self):
        self.__cursor.close()
        self.__conn.close()

    # 执行sql语句并返回结果
    def execute(self, sql: str, values: tuple):
        data = self.__cursor.execute(sql, values)
        self.__conn.commit()
        return data

    # 通过卡号检查用户是否存在
    def check_user_by_cno(self, c_no):
        sql = 'select * from user where c_no = %s'
        values = (c_no,)
        return self.execute(sql, values)

    # 添加用户
    def add_user(self, s_id, c_no, name):
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = 'insert into user (s_id, c_no, name, time) values (%s, %s, %s, %s)'
        values = (s_id, c_no, name, create_time)
        self.execute(sql, values)

    # 删除用户
    def del_user(self, s_id):
        sql = 'delete from user where s_id = %s'
        values = (s_id,)
        self.execute(sql, values)

    # 修改用户信息
    def modify_user(self, s_id, c_no, name):
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = 'update user set c_no = %s, name = %s, time = %s where s_id = %s'
        values = (c_no, name, create_time, s_id)
        self.execute(sql, values)


__all__ = [
    DataBase,
]
