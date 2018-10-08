#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 19:55:43 2018

@author: haizui

Nasdaq web page (https://www.nasdaq.com/) 
related functions
"""

from bs4 import BeautifulSoup
import requests
import time
import datetime as dt

month_names = {1:'Jan'
               , 2:'Feb'
               , 3:'Mar'
               , 4:'Apr'
               , 5:'May'
               , 6:'Jun'
               , 7:'Jul'
               , 8:'Aug'
               , 9:'Sep'
               , 0:'Oct'
               , 11:'Nov'
               , 12:'Dec'}

def DividendCalendarTableColumns(soup):
    try:
        return [col.text.strip() 
                for col 
                in soup.find('table',{'class':'DividendCalendar'})
                            .find_all('tr')[0] #First row = column names
                            .find_all('th')]
    except:
        return None
    

def DividendCalendarTableSoup(date : dt.date):
    year = str(date.year)
    month = month_names[date.month]
    day = str(date.day)
    url = 'https://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date={0}-{1}-{2}'.format(year, month, day)
    # Read first page
    r = requests.get(url)
    the_page = r.text
    soup = BeautifulSoup(the_page,'lxml')
    return soup

def DividendCalendarTable(date):
    soup = DividendCalendarTableSoup(date)

    # Find column names
    columns = DividendCalendarTableColumns(soup)
    # If data not available, return None
    if columns is None:
        return None, None
    columns.append('Timestamp')
    # Treat all subpages
    # Initializations
    data = []
    timestamp = time.time()
    rows = soup.find_all('tr',{'class':'genTablealt'})
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip().replace(u'\xa0', u' ') for ele in cols]
        cols.append(timestamp)
        if len(cols) == len(columns):
            data.append([ele for ele in cols if ele]) # Get rid of empty values
    return columns,data
