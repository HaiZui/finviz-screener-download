#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 19:55:43 2018

@author: haizui

Finviz stock-screener (https://finviz.com/screener.ashx) 
related functions
"""

from bs4 import BeautifulSoup
import re
import requests
import time

def TableId(name):
    dict = {'valuation':121,
            'financial':161,
            'ownership':131,
            'technical':171}
    return dict[name]


def screenerTableColumns(soup):
    return [col.text.strip() for col in soup.find_all('td',{'class':re.compile('table-top*')})]

def screener_table_soup(name, page=1, rows_per_page=20):
    url_base = 'https://finviz.com/screener.ashx?v=%d&r=' % TableId(name)
    url = url_base + str(1+rows_per_page*(page-1))
    # Read first page
    r = requests.get(url)
    the_page = r.text
    soup = BeautifulSoup(the_page,'lxml')
    return soup

def screenerTable(name, page_max=1000):
    soup = screener_table_soup(name, page=1)

    # Find column names
    columns = screenerTableColumns(soup)
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
