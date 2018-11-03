from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

import invest_dw as idw
import invest_dw.database_etl as etl
import invest_dw.database_io as dio
import invest_dw.finviz as fin
import pandas as pd


invest_dw_dir = '/home/haizui/Documents/GIT/github/invest-dw'
config_dir = invest_dw_dir + '/config_mysql.ini'


def load_finviz_table(screener_table_name, target_table_name = None):
    if target_table_name is None:
        target_table_name = screener_table_name
        
    columns, table = fin.screenerTable(screener_table_name, page_max=3)

    print('Saving data to database')
    config = dio.readConfig(config_dir)
    
    data_pd = pd.DataFrame(data=table, columns=columns)
    etl.writeTablePrestage(config, data_pd, screener_table_name)
    
    etl.loadTableHash(config
                 , 'prestage'
                 , screener_table_name
                 , 'stage'
                 , 'finviz_'+target_table_name
                 , hash_column = 'Sha256'
                 , truncate_target = True)

    etl.loadTableSCD(config
                 , 'stage'
                 , 'finviz_'+target_table_name
                 , 'finviz'
                 , target_table_name
                 , hash_column='Sha256') 

def load_finviz_price():
    load_finviz_table(screener_table_name='valuation', target_table_name='price')   
    return 'Done'

dag = DAG('load_finviz_prices_dag', description='Load stock prices from Finviz',
                        schedule_interval='*/5 * * * *', # Every 5 minutes
                        start_date=datetime(2018, 10, 29), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', dag=dag)
price_operator = PythonOperator(task_id='load_finviz_prices_task', python_callable=load_finviz_price, dag=dag)
dummy_operator >> price_operator

