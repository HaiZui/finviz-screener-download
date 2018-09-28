
import database_io as dio
import finviz as fin
import pandas as pd

if __name__ == '__main__':     # if the function is the main function ...
    table_name = 'valuation'
    columns, table = fin.screener_table(table_name, page_max=3)

    print('Saving data to database')
    config = dio.read_config('config_mysql.ini')
    
    data_pd = pd.DataFrame(data=table, columns=columns)
    dio.writeTablePrestage(config, data_pd, table_name)

