# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""


import os, re
import datetime as dt
import os.path as op


basedir = r'C:\Users\gonzalo\Projects\data\Espectros'

audits = [op.join(d[0], 'audita.txt') for d in os.walk(basedir) 
            if 'audita.txt' in d[2]]

total_time = 0
records = []

for audit in audits:
    with open(audit) as au:
        path_list = op.normpath(audit).split('\\') # ('/') # for linux
        user_name, sample_name, expno = path_list[-4:-1]
        
        contents = au.read()
        
        # find starting time
        start_str = re.findall(r'started at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3} \+\d{4})',
                           contents)
        # check for starting time matching
        if len(start_str) == 1:
            start_time = dt.datetime.strptime(start_str[0], '%Y-%m-%d %H:%M:%S.%f %z')
        else:
            print('Starting time not found for: %s' % op.dirname(audit))
            continue
        # find starting time
        finish_str = re.findall(r'finished successfully at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3} \+\d{4})',
                           contents)        
        if len(finish_str) == 1:
            finish_time = dt.datetime.strptime(finish_str[0], '%Y-%m-%d %H:%M:%S.%f %z')
        else:
            print('Finish time not found for: %s' % op.dirname(audit))
            continue

        duration = finish_time - start_time

            
        print(audit, user_name, sample_name, expno, start_time.ctime(), finish_time.ctime(), duration)
            
        