from bs4 import BeautifulSoup
import re
import csv
import requests
import time
import sqlalchemy
from configparser import ConfigParser
import mysql.connector

def table_id(name):
    dict = {'valuation':121,
            'financial':161,
            'ownership':131,
            'technical':171}
    return dict[name]

def write_csv(table,name):
    with open('%s.csv' % name, 'w+') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
        spamwriter.writerows(table)

def read_config(file_name: str):
    config = ConfigParser()
    try:
        config.read(file_name)
        return config
    except IOError:
        print("No file named {} found".format(file_name))
        return 1

def screener_table_columns(soup):
    return [col.text.strip() for col in soup.find_all('td',{'class':re.compile('table-top*')})]

def screener_table_soup(name, page=1, rows_per_page=20):
    url_base = 'https://finviz.com/screener.ashx?v=%d&r=' % table_id(name)
    url = url_base + str(1+rows_per_page*page)
    # Read first page
    r = requests.get(url)
    the_page = r.text
    soup = BeautifulSoup(the_page,'lxml')
    return soup

def screener_table(name, page_max=1000):
    soup = screener_table_soup(name, page=1)

    # Find column names
    columns = screener_table_columns(soup)
    columns.append('Timestamp')
    # Treat all subpages
    # Initializations
    rows_per_page = 20
    n = 1
    n_page = 1
    written_rows = rows_per_page
    data = []
    while written_rows == rows_per_page and n_page<=page_max:
        print('Page: %d' % n_page)
        timestamp = time.time()
        written_rows = 0
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td',{'class':'screener-body-table-nw'})
            cols = [ele.text.strip() for ele in cols]
            cols.append(timestamp)
            if len(cols) == len(columns):
                data.append([ele for ele in cols if ele]) # Get rid of empty values
                written_rows += 1
        # Fetch new page
        n += rows_per_page
        n_page += 1
        soup = screener_table_soup(name, n_page, rows_per_page)
        
    return columns,data

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

def connect_sqlalchemy(host, user, passwd, db):
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(user, passwd, 
                                                      host, db))
    return database_connection

if __name__ == '__main__':     # if the function is the main function ...
    output_folder = 'output'
    table_name = 'ownership'
    columns, table = screener_table(table_name, page_max=3)
    write_csv(table, '%s/screener_table_%s' % (output_folder, table_name))

    print('Saving data to database')
    config = read_config('config_mysql.ini')
    host = config['server']['host']
    user = config['server']['user']
    passwd = config['server']['passwd']
    db = config['server']['db']
    unix_socket = config['server']['unix_socket']

    mydb = mysql.connector.connect(host=host
                                    ,user=user
                                    ,passwd=passwd
                                    ,db=db
                                    ,unix_socket=unix_socket)
    
    mydb = mysql.connector.connect(host=host
            ,user=user
            ,passwd=passwd
            ,db=db
            ,unix_socket=unix_socket)
            
    if not checkSchemaExists(mydb, 'stage'):
        cursor = mydb.cursor()
        cursor.execute('CREATE SCHEMA stage') 

    if not checkTableExists(mydb, 'stage', table_name):
        createStageTable(mydb, 'stage', table_name, columns)

    cursor = mydb.cursor()

