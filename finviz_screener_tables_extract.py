
import database_io as dio
import finviz as fin
import data
import pandas as pd

import mysql.connector

if __name__ == '__main__':     # if the function is the main function ...
    output_folder = 'output'
    table_name = 'valuation'
    columns, table = fin.screener_table(table_name, page_max=3)
    data.write_csv(table, '%s/screener_table_%s' % (output_folder, table_name))

    print('Saving data to database')
    config = dio.read_config('config_mysql.ini')
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
 
         
    
    if not dio.checkSchemaExists(conn_mysql, 'stage'):
        print('Creating schema stage')
        cursor = conn_mysql.cursor()
        cursor.execute('CREATE SCHEMA stage') 
        cursor.close()
        
    if not dio.checkTableExists(conn_mysql, 'stage', table_name):
        dio.createStageTable(conn_mysql, 'stage', table_name, columns)
    
    print('Clearing stage')
    cursor = conn_mysql.cursor()
    cursor.execute('delete from {}.{}'.format('stage',table_name))
    cursor.close()
    conn_mysql.close()
    
    print('Writing stage')
    conn_sqlalch = dio.connect_sqlalchemy(host, user, passwd, db)   
    data_pd = pd.DataFrame(data=table, columns=columns)
    data_pd.to_sql(if_exists='append'
                   , name=table_name
                   , schema='stage'
                   , con=conn_sqlalch
                   , index=False)

