#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 19:52:40 2018

@author: haizui

Functions for mysql database connections
"""
import sqlalchemy
import mysql.connector
import time
from configparser import ConfigParser

def read_config(file_name: str):
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

def hashExcludedColumns():
    list = ['Timestamp']
    return list

def calculateHash(dbcon, schema_name, table_name, columns, hash_column = 'Sha256'):
    # Build hash select query
    hashed_columns = list(set(columns)-set(hashExcludedColumns()))
    execute_string = """
                    update {}.{} 
                    set {} = SHA2(cast(`{}` as char(255)), 256)""".format(schema_name
                        , table_name
                        , hash_column
                        , "` as char(255))+cast(`".join(hashed_columns))    
    dbcon.execute(execute_string)
    return True    
    

def createStageTable(dbcon, schema_name, table_name, columns, calculateHash=True):
    dbcur = dbcon.cursor()
    # Build execurion string
    execute_string = "CREATE TABLE {}.{} (`".format(schema_name, table_name)
    for column in columns[:-1]:
        execute_string += '{}` varchar(255),`'.format(column)
    # Append last column
    if calculateHash:
        hash_column = 'Sha256'
        execute_string += '{}` varchar(255), `{}` varbinary(256))'.format(columns[-1], hash_column)
        dbcur.execute(execute_string)
    else:
        execute_string += '{}` varchar(255))'.format(columns[-1])
        
    dbcur.close()
    return True

def connect_sqlalchemy(config):
    host = config['server']['host']
    user = config['server']['user']
    passwd = config['server']['passwd']
    db = config['server']['db']
    
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(user, passwd, 
                                                      host, db))
    return database_connection

def writeTablePrestage(config, data_pd, table_name):
    columns = data_pd.columns
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

    target_schema = 'prestage'
        
    if not checkSchemaExists(conn_mysql, target_schema):
        print('Creating schema {}'.format(target_schema))
        cursor = conn_mysql.cursor()
        cursor.execute('CREATE SCHEMA {}'.format(target_schema)) 
        cursor.close()
        
    if not checkTableExists(conn_mysql, target_schema, table_name):
        createStageTable(conn_mysql, target_schema, table_name, columns, calculateHash=False)
    
    print('Clearing {}'.format(target_schema))
    cursor = conn_mysql.cursor()
    cursor.execute('truncate table {}.{}'.format(target_schema,table_name))
    cursor.close()
    conn_mysql.close()
    
    print('Writing {}'.format(target_schema))
    conn_sqlalch = connect_sqlalchemy(config)
    data_pd.to_sql(if_exists='append'
                   , name=table_name
                   , schema=target_schema
                   , con=conn_sqlalch
                   , index=False)
    
    return True


def writeTableStage(config
                 , source_schema
                 , source_table
                 , target_schema
                 , target_table
                 , hash_column = 'Sha256'
                 , valid_from_col = 'Valid_From'
                 , valid_to_col = 'Valid_To'
                 , timestamp = time.time()):
    
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

    target_schema = 'stage'
        
    
    print('Clearing {}'.format(target_schema))
    cursor = conn_mysql.cursor()
    cursor.execute('truncate table {}.{}'.format(target_schema,target_table))
    cursor.close()
    conn_mysql.close()
    
    print('Writing {}'.format(target_schema))
    conn_sqlalch = connect_sqlalchemy(config)
    
    # Common columns between source and target table
    execute_string = """
                    select pre.COLUMN_NAME
                    from information_schema.COLUMNS as pre
                    join information_schema.COLUMNS as stage
                    on pre.COLUMN_NAME = stage.COLUMN_NAME
                    where pre.TABLE_SCHEMA = 'prestage'
                    AND stage.TABLE_SCHEMA = 'stage'
                    and pre.table_name = 'valuation'
                    and stage.table_name = 'valuation'
                    """
    
    
    return True  
    
def rowsUpdated(config
                 , source_schema
                 , source_table
                 , target_schema
                 , target_table
                 , hash_column = 'Sha256'
                 , valid_from_col = 'Valid_From'
                 , valid_to_col = 'Valid_To'
                 , timestamp = time.time()):
    

    conn_mysql = connectMySQL(config)
    
    # Execution begins
    cursor = conn_mysql.cursor()
    
    execute_string = """select a.{0}
                        from {1}.{2} a
                        left join {3}.{4} b
                        on a.{0} = b.{0}
                        where b.{0} is null
                        and a.{5} <= {7}
                        and a.{6} > {7}
                        """.format(hash_column
                                  , target_schema
                                  , target_table
                                  , source_schema
                                  , source_table
                                  , valid_from_col
                                  , valid_to_col
                                  , timestamp)
    cursor.execute(execute_string)
    
    # Result set
    rows = list(cursor.fetchall())
    cursor.close()
    return rows

def rowsInserted(config
                 , source_schema
                 , source_table
                 , target_schema
                 , target_table
                 , hash_column = 'Sha256'
                 , valid_from_col = 'Valid_From'
                 , valid_to_col = 'Valid_To'
                 , timestamp = time.time()):
    

    conn_mysql = connectMySQL(config)
    
    # Execution begins
    cursor = conn_mysql.cursor()
    
    execute_string = """select b.{0}
                        from {1}.{2} a
                        right join {3}.{4} b
                        on a.{0} = b.{0}
                        and a.{5} <= {7}
                        and a.{6} > {7}
                        where a.{0} is null
                        """.format(hash_column
                                  , target_schema
                                  , target_table
                                  , source_schema
                                  , source_table
                                  , valid_from_col
                                  , valid_to_col
                                  , timestamp)
                        
    cursor.execute(execute_string)
    
    # Result set
    rows = list(cursor.fetchall())
    cursor.close()
    return rows
                        

def loadTableSCD(config
                 , source_schema
                 , source_table
                 , target_schema
                 , target_table
                 , hash_column='Sha256'):
    conn_mysql = connectMySQL(config)
    
    
    