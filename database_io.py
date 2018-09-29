#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 19:52:40 2018

@author: haizui

Functions for mysql database connections and common executions.
"""
import sqlalchemy
import mysql.connector
from configparser import ConfigParser

def readConfig(file_name: str):
    config = ConfigParser()
    try:
        config.read(file_name)
        return config
    except IOError:
        print("No file named {} found".format(file_name))
        return 1

def connectMySQL(config):
    host = config['server']['host']
    user = config['server']['user']
    passwd = config['server']['passwd']
    db = config['server']['db']
    unix_socket = config['server']['unix_socket']

    conn_mysql = mysql.connector.connect(host=host
                                    ,user=user
                                    ,passwd=passwd
                                    ,db=db
                                    ,unix_socket=unix_socket)
    return conn_mysql

def connectSqlalchemy(config):
    host = config['server']['host']
    user = config['server']['user']
    passwd = config['server']['passwd']
    db = config['server']['db']
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(user, passwd, 
                                                      host, db))
    return database_connection
def executeQuery(config, execute_string):
    conn_mysql = connectMySQL(config)
    cursor = conn_mysql.cursor()
    try:
        try:
            cursor.execute(execute_string)
            conn_mysql.commit()
        except (mysql.Error, mysql.Warning) as e:
            print(e)
            return None
    finally:
        cursor.close()
        conn_mysql.close()
    
def truncateTable(config, target_schema, target_table):
    executeQuery(config, 'truncate table {}.{}'.format(target_schema,target_table))
    return True

def checkTableExists(dbcon, schema_name, table_name):
    dbcur = dbcon.cursor()
    dbcur.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_name = '{0}'
                    AND table_schema = '{1}'
                    """.format(table_name,schema_name))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

def checkSchemaExists(dbcon, schema_name):
    dbcur = dbcon.cursor()
    dbcur.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.schemata
                    WHERE schema_name = '{0}'
                    """.format(schema_name.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

def commonColumns(config
                 , source_schema
                 , source_table
                 , target_schema
                 , target_table):
    
    conn_mysql = connectMySQL(config)
    cursor = conn_mysql.cursor()
    # Common columns between source and target table
    execute_string = """
                    select pre.COLUMN_NAME
                    from information_schema.COLUMNS as pre
                    join information_schema.COLUMNS as stage
                    on pre.COLUMN_NAME = stage.COLUMN_NAME
                    where pre.TABLE_SCHEMA = '{0}'
                    AND stage.TABLE_SCHEMA = '{1}'
                    and pre.table_name = '{2}'
                    and stage.table_name = '{3}'
                    """.format(source_schema
                              , target_schema
                              , source_table
                              , target_table)
    # Result set
    cursor.execute(execute_string)
    result = cursor.fetchall()
    rows = [i[0] for i in result]
    cursor.close()
    conn_mysql.close()
    return rows

    
    
    