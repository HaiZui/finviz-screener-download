# coding: utf-8
import re
import requests
import time
import logging
import invest_dw.scraping as scraping
from bs4 import BeautifulSoup
import ast

def find_parens(s):
    # Helping function for finding the closing parenthesis
    toret = {}
    pstack = []

    for i, c in enumerate(s):
        if c == '[':
            pstack.append(i)
        elif c == ']':
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[pstack.pop()] = i

    if len(pstack) > 0:
        #raise IndexError("No matching opening parens at: " + str(pstack.pop()))
        # We want only closing parenthesis (of the first encountered list)
        pass

    return toret

def stock_data(exchange):
    columns = ['closePrice'
               , 'marketValue'
               , 'tradeCurrency'
               , 'tickSize'
               , 'company'
               , 'closeDateTime'
               , 'insRef'
               , 'internalTurnover'
               , 'isin'
               , 'internalQuantity'
               , 'name'
               , 'quantity'
               , 'turnover'
               , 'dayLowPrice'
               , 'lastPrice'
               , 'openPrice'
               , 'dayHighPrice'
               , 'changePercent1m'
               , 'askPrice'
               , 'changePercent'
               , 'bidPrice'
               , 'symbol'
               #, 'numberOfShares'
               #, 'totalCompanyShares'
               ]
    all_columns = columns.copy()
    all_columns.append('numberOfShares')
    all_columns.append('totalCompanyShares')
    all_columns.append('Timestamp')

    #url = 'https://www.kauppalehti.fi/5/i/porssi/porssikurssit/lista.jsp'
    url = 'https://www.kauppalehti.fi/porssi/kurssit/{}'.format(exchange.upper())


    r = scraping.request_random_header(url)
    the_page = r.text
    soup = BeautifulSoup(the_page,'lxml')
    
    # Find list containing share prices etc. from the string
    i = soup.text.find('shares')
    # Adjust
    i += 8

    list_str = soup.text[i:]

    # List of  interest starts at position i
    # Find location of enclosing parenthesis
    list_str = list_str[:find_parens(list_str)[0]+1]
   
    list_obj = ast.literal_eval(list_str)
    
    # Construct returned data
    data = []    

    for stock in list_obj:
        timestamp = time.time()
        row = []
        for column in columns:
            try:
                row.append(stock[column])
            except:
                row.append(None)		
        row.append(stock['quoteShares'][0]['numberOfShares'])
        row.append(stock['quoteShares'][0]['totalCompanyShares'])
        row.append(timestamp)
        data.append(row)


    return all_columns,data
	
