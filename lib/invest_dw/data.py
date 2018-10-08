#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 19:57:55 2018

@author: haizui
"""


def write_csv(table,name):
    with open('%s.csv' % name, 'w+') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
        spamwriter.writerows(table)