
import invest_dw as idw
import invest_dw.database_etl as etl
import invest_dw.database_io as dio
import invest_dw.kauppalehti as kl
import pandas as pd

def load_kauppalehti_table():
	service_name = 'kauppalehti'
	table_name = 'price'	
	columns, table = kl.stock_data()
	
	print('Saving data to database')
	config = dio.readConfig('config_mysql.ini')
	
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

if __name__ == '__main__':     # if the function is the main function ...
    # Daily tables
    load_kauppalehti_table()


