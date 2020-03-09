# -*- coding:utf-8 -*-
from pymysql import cursors,connect

def getConnection():
    connection=connect(host="host",
                        user='user',
                        password='password',
                        db='db_name',
                        cursorclass=cursors.DictCursor)
    return connection
