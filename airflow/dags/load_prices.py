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

def load_finviz_valuation():
    load_finviz_table(screener_table_name='valuation', target_table_name='valuation')   
    return 'Done'

def load_finviz_financial():
    load_finviz_table(screener_table_name='financial', target_table_name='financial')   
    return 'Done'

def load_finviz_ownership():
    load_finviz_table(screener_table_name='ownership', target_table_name='ownership')   
    return 'Done'

def load_finviz_technical():
    load_finviz_table(screener_table_name='technical', target_table_name='technical')   
    return 'Done'

dag = DAG('dag_load_finviz_screener_tables', description='Load Finviz screener tables',
                        schedule_interval='00 15 * * *', # Daily at 4 AM
                        start_date=datetime(2018, 10, 29), catchup=False)


dummy_operator = DummyOperator(task_id='dummy_task', dag=dag)
price_operator_valuation = PythonOperator(task_id='task_load_finviz_valuation', python_callable=load_finviz_valuation, dag=dag)
price_operator_financial = PythonOperator(task_id='task_load_finviz_financial', python_callable=load_finviz_financial, dag=dag)
price_operator_ownership = PythonOperator(task_id='task_load_finviz_ownership', python_callable=load_finviz_ownership, dag=dag)
price_operator_technical = PythonOperator(task_id='task_load_finviz_technical', python_callable=load_finviz_technical, dag=dag)
dummy_operator >> price_operator_valuation >> price_operator_financial >> price_operator_ownership >> price_operator_technical


