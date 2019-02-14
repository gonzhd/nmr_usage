# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""


import os, re
import datetime as dt
import os.path as op
import pandas as pd


icon_acc_file = r'C:\Users\gonzalo\Projects\nmrlab\Inmracct.full'

total_time = 0
records = []

# read accounting log file
with open(icon_acc_file) as au:
    contents = au.read()
    
exps = [x for x in re.split('-{44}\n', contents) if x.startswith('#Experiment')]    
    
def gen_records(exps, start=0, end=-1):
    if end == -1 :
        end = len(exps)
    records = []
    for exp in exps[start:end]:
        record =  {}
        
        items = [e.strip().split(":",1) for e in exp.split("\n") if e and not e.startswith("#") and ':' in e]
        print(items)
        items = {k.strip():v.strip() for k,v in items}
        
        if not items.get('fileName'):
            continue

        if not items.get('timeOfStart') or not items.get('timeOfTermination'):
            continue

        it = re.findall(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', items['timeOfStart'])[0]
        record['Fecha Comienzo'] = dt.datetime.strptime(it, r'%m/%d/%Y %H:%M:%S')

        it = re.findall(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', items['timeOfTermination'])[0]
        record['Fecha Fin'] = dt.datetime.strptime(it, r'%m/%d/%Y %H:%M:%S')
                    
        record['Duración'] =  record['Fecha Fin'] - record['Fecha Comienzo']
        
        its = items['nameOfExperiment'].strip().split()
        record['Experimento'] = its[0] if len(its)==1 else its[1]
        
        record['Núcleo'] = items['NUCLEUS']
        record['Solvente'] = items['solvent']
        
        it = items['fileName'].split()
        record['Muestra'] = it[0]
        record['#Exp'] = it[1]
        record['Usuario'] = it[3].split('\\')[-1]
        
        records.append(record)
        
    return pd.DataFrame(records)