# -*- coding: utf-8 -*-
import mysql.connector
from datetime import datetime


ENV_SERVER = 0

def create_conn ():
    if ENV_SERVER == 0:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="stats"
            )
    else:
        conn = mysql.connector.connect(
            host="localhost",
            user="felipe",
            password="",                #PRIMERO CAMBIAR Y LUEGO INSERTAR PASSWORD
            database="stats"
            )
    return conn


def get_election():
    conn = create_conn()
    cursor = conn.cursor()
    
    query = "select * from execution_mode WHERE id IN (SELECT max(id) FROM execution_mode)"
    cursor.execute(query)
    record = cursor.fetchall()
    
    conn.close()

    return record


def get_max_id_arbitraje():
    conn = create_conn()
    cursor = conn.cursor()
    
    query = "select max(id) from arbitraje_stats"
    cursor.execute(query)
    record = cursor.fetchall()
    
    conn.close()

    return record[0][0]
    

def insert_mode(mode, election):
    conn = create_conn()
    cursor = conn.cursor()
    
    query = 'INSERT INTO execution_mode (type,election) VALUE (%s,%s);'
    to_insert = (str(mode), str(election))
    cursor.execute(query, to_insert)
    
    conn.commit()
    conn.close()
 
    
def insert_new_strategy(sym):
    conn = create_conn()
    cursor = conn.cursor()
    
    date = str(datetime.now())
    
    query = 'INSERT INTO trading_stats (state, symbol, created_at, updated_at) VALUES (%s,%s,%s,%s);'
    record = (0, sym, date, date)
    cursor.execute(query,record)
    
    conn.commit()
    conn.close()


def update_strategy():
    conn = create_conn()
    cursor = conn.cursor()
    
    date = str(datetime.now())

    query = 'UPDATE trading_stats SET state=1, updated_at=%s WHERE id IN (SELECT max(id) FROM trading_stats)'
    cursor.execute(query, (date,))
    
    conn.commit()
    conn.close()
    
    
def insert_new_arbitraje(sym, way = -1):
    conn = create_conn()
    cursor = conn.cursor()
    
    date = str(datetime.now())
    if way == 0:
        query = 'INSERT INTO arbitraje_stats (state, symbol, way, created_at,updated_at) VALUES (%s,%s,%s,%s,%s);'
        record = (0, sym, way, date, date)
        cursor.execute(query,record)
    elif way == 1:
        query = 'INSERT INTO arbitraje_stats (state, symbol, way, created_at,updated_at) VALUES (%s,%s,%s,%s,%s);'
        record = (0, sym, way, date, date)
        cursor.execute(query,record)
    else:
        query = 'INSERT INTO arbitraje_stats (state, symbol, created_at,updated_at) VALUES (%s,%s,%s,%s);'
        record = (0, sym, date, date)
        cursor.execute(query,record)
    
    conn.commit()
    conn.close()


def update_arbitraje():
    conn = create_conn()
    cursor = conn.cursor()
    
    date = str(datetime.now())

    query = 'UPDATE arbitraje_stats SET state=1, updated_at=%s WHERE id IN (SELECT max(id) FROM arbitraje_stats)'
    cursor.execute(query, (date,))
    
    conn.commit()
    conn.close()

    
def clean_all():
    conn = create_conn()
    cursor = conn.cursor()
    
    query = 'TRUNCATE TABLE execution_mode'
    cursor.execute(query)
    
    query = 'TRUNCATE TABLE trading_stats'
    cursor.execute(query)
    
    query = 'TRUNCATE TABLE arbitraje_stats'
    cursor.execute(query)
    
    conn.close()
