import datetime
import pymysql

host = '101.43.65.22'
port = 8978
user = 'root'
passwd = 'rootroot'
db = 'opendoor'


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


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

    def connect(self):
        self.__conn = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, password=self.__passwd,
                                      db=self.__db)
        self.__cursor = self.__conn.cursor()

    def close(self):
        self.__cursor.close()
        self.__conn.close()

    def execute(self, sql: str, values: tuple):
        data = self.__cursor.execute(sql, values)
        self.__conn.commit()
        return data

    def check_user_by_cno(self, c_no):
        sql = 'select * from user where c_no = %s'
        values = (c_no,)
        return self.execute(sql, values)

    def add_user(self, s_id, c_no, name):
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = 'insert into user (s_id, c_no, name, time) values (%s, %s, %s, %s)'
        values = (s_id, c_no, name, create_time)
        self.execute(sql, values)

    def del_user(self, s_id):
        sql = 'delete from user where s_id = %s'
        values = (s_id,)
        self.execute(sql, values)

    def modify_user(self, s_id, c_no, name):
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = 'update user set c_no = %s, name = %s, time = %s where s_id = %s'
        values = (c_no, name, create_time, s_id)
        self.execute(sql, values)

