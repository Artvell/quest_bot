# -*- coding:utf-8 -*-
from con_to_db import getConnection

def get_from_db(n,t,q):#запрос,условие
    connection=getConnection()
    if q=='':
        sql=f"SELECT {n} FROM Quests_quest;"
    else:
        sql=f"SELECT {n} FROM Quests_quest WHERE {t} LIKE '%{q}%'"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        keys=[b[0] for b in cursor.description]
        result=[]
        for row in cursor:
            result.append([row[key] for key in keys])
        connection.close()
        return result
    except Exception:
        connection.close()
        return -2
def get_from_db_maps():
    connection=getConnection()
    strok="123"
    sql=f'SELECT longitude,latitude FROM Quests_quest WHERE longitude NOT LIKE {strok};'
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        keys=[b[0] for b in cursor.description]
        result=[]
        for row in cursor:
            result.append([row[key] for key in keys])
        connection.close()
        return result
    except Exception as e:
        connection.close()
        return e

def add_user(user_id):
    connection=getConnection()
    sql=f"INSERT INTO users(user_id) VALUES({user_id})"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()
    except Exception:
        connection.close()

def get_user_id():
    connection=getConnection()
    sql="SELECT * FROM users"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        keys=[b[0] for b in cursor.description]
        result=[]
        for row in cursor:
            result.append([row[key] for key in keys])
        connection.close()
        return result
    except Exception as e:
        connection.close()

def delete_user(user_id):
    connection=getConnection()
    sql=f"DELETE FROM users WHERE user_id={user_id}"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        connection.close()

def num_of_users():
    users=get_user_id()
    return len(users)