
import database_etl as etl
import database_io as dio
import finviz as fin
import pandas as pd

def load_finviz_table(table_name):
    columns, table = fin.screenerTable(table_name, page_max=3)

    print('Saving data to database')
    config = dio.readConfig('config_mysql.ini')
    
    data_pd = pd.DataFrame(data=table, columns=columns)
    etl.writeTablePrestage(config, data_pd, table_name)
    
    etl.loadTableHash(config
                 , 'prestage'
                 , table_name
                 , 'stage'
                 , 'finviz_'+table_name
                 , hash_column = 'Sha256'
                 , truncate_target = True)

    etl.loadTableSCD(config
                 , 'stage'
                 , 'finviz_'+table_name
                 , 'finviz'
                 , table_name
                 , hash_column='Sha256')    

if __name__ == '__main__':     # if the function is the main function ...
    # Daily tables
    load_finviz_table('valuation')
    load_finviz_table('financial')
    load_finviz_table('ownership')
    # Rapidly updating table
    load_finviz_table('technical')


