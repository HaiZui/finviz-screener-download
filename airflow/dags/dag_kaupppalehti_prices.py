from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

import invest_dw as idw
import invest_dw.database_etl as etl
import invest_dw.database_io as dio
import invest_dw.kauppalehti as kl
import pandas as pd


invest_dw_dir = '/home/haizui/Documents/GIT/github/invest-dw'
config_dir = invest_dw_dir + '/config_mysql.ini'


def load_kauppalehti_table(exchange):
	service_name = 'kauppalehti'
	table_name = '{}_prices'.format(exchange.lower())
	columns, table = kl.stock_data(exchange)
	
	print('Saving data to database')
	config = dio.readConfig(config_dir)
	
	data_pd = pd.DataFrame(data=table, columns=columns)
	etl.writeTablePrestage(config, data_pd, service_name+'_'+table_name)
	
	etl.loadTableHash(config
	         , 'prestage'
	         , service_name+'_'+table_name
	         , 'stage'
	         , service_name+'_'+table_name
	         , hash_column = 'Sha256'
	         , truncate_target = True)
	
	etl.loadTableSCD(config
	         , 'stage'
	         , service_name+'_'+table_name
	         , service_name
	         , table_name
	         , hash_column='Sha256')
	return 'Done'

def load_kauppalehti_xhel_table():
    load_kauppalehti_table('xhel')

def load_kauppalehti_xsto_table():
    load_kauppalehti_table('xsto')
    
def load_kauppalehti_xcse_table():
    load_kauppalehti_table('xcse')
    
def load_kauppalehti_fnfi_table():
    load_kauppalehti_table('fnfi')
    
dag = DAG('dag_load_kauppalehti_xhel_prices', description='Load stock prices from Kauppalehti HEX exchange',
                        schedule_interval='*/5 * * * *', # Every 5 minutes
                        start_date=datetime(2018, 10, 29), catchup=False)


dummy_operator = DummyOperator(task_id='dummy_task', dag=dag)
price_operator_xhel = PythonOperator(task_id='task_load_kauppalehti_xhel_prices', python_callable=load_kauppalehti_xhel_table, dag=dag)
price_operator_xsto = PythonOperator(task_id='task_load_kauppalehti_xsto_prices', python_callable=load_kauppalehti_xsto_table, dag=dag)
price_operator_xcse = PythonOperator(task_id='task_load_kauppalehti_xcse_prices', python_callable=load_kauppalehti_xcse_table, dag=dag)
price_operator_fnfi = PythonOperator(task_id='task_load_kauppalehti_fnfi_prices', python_callable=load_kauppalehti_fnfi_table, dag=dag)
dummy_operator >> price_operator_xhel >> price_operator_xsto >> price_operator_xcse >> price_operator_fnfi

