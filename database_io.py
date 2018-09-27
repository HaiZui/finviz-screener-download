#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 19:52:40 2018

@author: haizui

Functions for mysql database connections
"""
import sqlalchemy
from configparser import ConfigParser

def read_config(file_name: str):
    config = ConfigParser()
    try:
        config.read(file_name)
        return config
    except IOError:
        print("No file named {} found".format(file_name))
        return 1
    
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

def createStageTable(dbcon, schema_name, table_name, columns):
    dbcur = dbcon.cursor()
    # Build execurion string
    execute_string = "CREATE TABLE {}.{} (`".format(schema_name, table_name)
    for column in columns[:-1]:
        execute_string += '{}` varchar(255),`'.format(column)
    # Append last column
    execute_string += '{}` varchar(255))'.format(columns[-1])
    
    dbcur.execute(execute_string)
    dbcur.close()
    return True

def connect_sqlalchemy(host, user, passwd, db):
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(user, passwd, 
                                                      host, db))
    return database_connection