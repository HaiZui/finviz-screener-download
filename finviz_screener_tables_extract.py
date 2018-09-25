from bs4 import BeautifulSoup
import urllib
import re
import csv
import requests
# py3
from urllib.request import Request, urlopen
from urllib.parse import urlencode

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

#def main():
def screener_table(name):
    url_base = 'https://finviz.com/screener.ashx?v=%d&r=' % table_id(name)
    
    url = url_base + '1'

    rows_per_page = 20

    # Read first page
    r = requests.get(url)
    the_page = r.text
    soup = BeautifulSoup(the_page,'lxml')
    data = []

    # Find column names
    columns = [col.text.strip() for col in soup.find_all('td',{'class':re.compile('table-top*')})]
    data.append(columns)

    # Treat all subpages
    # Initializations
    n = 1
    n_page = 1
    written_rows = rows_per_page
    while written_rows == rows_per_page:
        print('Page: %d' % n_page)
        written_rows = 0
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td',{'class':'screener-body-table-nw'})
            cols = [ele.text.strip() for ele in cols]
            if len(cols) == len(columns):
                data.append([ele for ele in cols if ele]) # Get rid of empty values
                written_rows += 1
        # Fetch new page
        n += rows_per_page
        r = requests.get(url_base + str(n))
        the_page = r.text
        soup = BeautifulSoup(the_page,'lxml')
        n_page += 1
        
    return data
 
if __name__ == '__main__':     # if the function is the main function ...
    output_folder = 'output'
    table_name = 'valuation'
    table = screener_table(table_name)
    write_csv(table, '%/screener_table_%s' % (output_folder, table_name))
