#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 22:06:52 2018

@author: haizui
"""

import time
import database_io as dio

def hashExcludedColumns():
    list = ['Timestamp']
    return list

def hashedColumns(columns):
    return list(set(columns)-set(hashExcludedColumns()))

def calculateHash(config, schema_name, table_name, columns, hash_column = 'Sha256'):
    # Build hash select query
    # Do not include determined columns into hash
    hashed_columns = hashedColumns(columns)
    execute_string = """
                    update {}.{} 
                    set {} = SHA2(cast(`{}` as char(255)), 256)""".format(schema_name
                        , table_name
                        , hash_column
                        , "` as char(255))+cast(`".join(hashed_columns))  
    print('Calculating hash {0}.{1}'.format(schema_name, table_name))
    dio.executeQuery(config, execute_string)
    return True    

def createStageTable(dbcon, schema_name, table_name, columns, calculate_hash=True):
    dbcur = dbcon.cursor()
    # Build execution string
    execute_string = "CREATE TABLE {}.{} (`".format(schema_name, table_name)
    for column in columns[:-1]:
        execute_string += '{}` varchar(255),`'.format(column)
    # Append last column
    if calculate_hash:
        hash_column = 'Sha256'
        execute_string += '{}` varchar(255), `{}` varbinary(256))'.format(columns[-1], hash_column)
        dbcur.execute(execute_string)
    else:
        execute_string += '{}` varchar(255))'.format(columns[-1])
    dbcur.close()
    return True


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
    dio.truncateTable(config, target_schema, target_table)
    
    print('Writing {}'.format(target_schema))
    conn_sqlalch = dio.connectSqlalchemy(config)
    data_pd.to_sql(if_exists='append'
                   , name=table_name
                   , schema=target_schema
                   , con=conn_sqlalch
                   , index=False)
    conn_sqlalch.close()
    return True

def loadTableHash(config
                 , source_schema
                 , source_table
                 , target_schema
                 , target_table
                 , hash_column = 'Sha256'
                 , truncate_target = False):
    """
    Loads table from source table to target table and calculates hash.
    Only common fields (with exactly same names) are inserted.
    """
        
    if truncate_target:
        dio.truncateTable(config, target_schema, target_table)

    common_columns = dio.commonColumns(config
                 , source_schema
                 , source_table
                 , target_schema
                 , target_table)
    
    # Insert begins
    print('Inserting into {0}.{1}'.format(target_schema, target_table))
    execute_string = """insert into {0}.{1} (`{2}`) select `{2}`
                    from {3}.{4};
                    """.format(target_schema
                              , target_table
                              , "`,`".join(common_columns)
                              , source_schema
                              , source_table)
    dio.executeQuery(config, execute_string)
    # Calculate hash
    calculateHash(config
                  , target_schema
                  , target_table
                  , common_columns
                  , hash_column)
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
    
    conn_mysql = dio.connectMySQL(config)
    
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
    conn_mysql.close()
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
    conn_mysql = dio.connectMySQL(config)
    
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
    conn_mysql.close()
    return rows
                        
def loadTableSCD(config
                 , source_schema
                 , source_table
                 , target_schema
                 , target_table
                 , hash_column='Sha256'):
    return True