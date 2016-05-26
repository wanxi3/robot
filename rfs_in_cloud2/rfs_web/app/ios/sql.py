import mysql.connector
import re
import sys
db_info = {'user': 'tbj',
                        'pwd': 'tbj900900',
                        'host': '192.168.1.9',
                        'db_base': 'tbj'}
class mysql_connect:
    def __init__(self, db_info):
        self.db_user = db_info['user']
        self.db_pw = db_info['pwd']
        self.db_host = db_info['host']
        self.database = db_info['db_base']
        self.cnx = mysql.connector.connect(user=self.db_user, password=self.db_pw, host=self.db_host, database=self.database)
        self.cursor = self.cnx.cursor()

    def sql_exec(self, sql_com, need_return=0):
        if need_return == 1:
            try:
                self.cursor.execute(sql_com)
                print self.cursor
                return self.cursor
            except mysql.connector.Error as err:
                #time_print("Error: {}".format(err.msg))
                sys.exit()
            #finally:
            cnx.commit()
        elif need_return == 0:
            try:
                self.cursor.execute(sql_com)
            except mysql.connector.Error as err:
                #time_print("Error: {}".format(err.msg))
                sys.exit()
            #finally:
            self.cnx.commit()

    def sql_assign_exec(self, sql_com):
        value = 'not find'
        for i in self.sql_exec(sql_com, 1):
            value = i[0]
        return value

