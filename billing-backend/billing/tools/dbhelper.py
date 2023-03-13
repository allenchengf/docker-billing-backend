import pymysql


class DBHelper:

    def __init__(self):
        self.host = "10.88.55.121"
        self.user = "rdadmin"
        self.password = "Kz8Zq)Rod^5qeZML"
        self.db = "billing"

    def __connect__(self):
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql, params=None):
        self.__connect__()
        self.cur.execute(sql, params)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def fetchone(self, sql, params=None):
        self.__connect__()
        self.cur.execute(sql, params)
        result = self.cur.fetchone()
        self.__disconnect__()
        return result

    def execute(self, sql, params=None):
        self.__connect__()
        self.cur.execute(sql, params)
        self.con.commit()
        self.__disconnect__()
