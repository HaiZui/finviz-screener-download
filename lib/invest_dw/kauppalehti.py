# coding: utf-8
import re
import requests
import time
import logging
import invest_dw.scraping as scraping
from bs4 import BeautifulSoup



def stock_data():
    columns = ['Nimi',
                'Viim',
                'Muutos',
                'Aika',
                'Osto',
                'Myynti',
                'Ylin',
                'Alin',
                'MiljE',
                'Porssi',
                'Teollisuus',
                'Timestamp']

    #url = 'https://www.kauppalehti.fi/5/i/porssi/porssikurssit/lista.jsp'
    url = 'https://www.kauppalehti.fi/5/i/porssi/porssikurssit/lista.jsp?reverse=false&order=alpha&markets=XHEL&markets=XSTO&markets=XCSE&volume=cur&psize=50&listIds=kaikki&rdc=166f95744d8&gics=0&refresh=60&currency=euro'

    r = scraping.request_random_header(url)
    the_page = r.text
    soup = BeautifulSoup(the_page,'lxml')
    
    
    table = soup.find_all('div',{'id':'taulukonTiedot'})
    rows = table[0].find_all('tr')
    
    data = []    
    group = ""
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols) == 1:
            group = row.find_all('td')[0].text
            continue
        
        if row['class'][0] != "strong":
            cols.append(group)
            timestamp = time.time()
            cols.append(timestamp)
            data.append([ele for ele in cols if ele]) # Get rid of empty values

    return columns,data
	
