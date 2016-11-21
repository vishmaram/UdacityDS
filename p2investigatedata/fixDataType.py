from datetime import datetime as dt
# -*- coding: utf-8 -*-

def parse_date(dateStr):
    if dateStr == '': return None
    else : return dt.strptime(dateStr,"%Y-%m-%d")

def parse_maybe_int(j):
    if j == '' : return None
    else : return int(j)
    
