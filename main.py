# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 10:41:19 2016

@author: Artur_Herczeg
"""
import data_access
import os
from data_access import process_java_hungary_employees
from data_access import process_dotnet_hungary_employees
from visualize import Dump
import E3S.Employees.stats as stats

from config import DATA_PATH

def get_data(steps):
    return { name:df for name, df in [step(data_access.AUTH) for step in steps]}

def dump_stats(result, console=True, excel=True):
    def dump_stat(s):
        dump = Dump(s)
        if console:
            dump.to_console()
        if excel:
            dump.to_excel(full_path, dump.name)
    
    for name, df in exec_result.items():
        full_path = os.path.join(DATA_PATH, "%s.xlsx" % name)

        print("*************** %s *******************" % name)        
        if excel:
            print("Writing to excel file: '%s'" % full_path)
        
        empstat = stats.EmployeeStats(df)
        
        stat_list = [
            ("Non-billables", empstat.get_nonbillables()),
            ("RMs", empstat.get_RMs()),
            ("Cities", empstat.get_cities()),
            ("Titles", empstat.get_title_count())
        ]
        
        [dump_stat(stat) for stat in stat_list]

def dump_data(data):
    visualizers = [Dump(result) for result in data.items()]
    [vis.to_console() for vis in visualizers]
        

data_collectors = [
    process_dotnet_hungary_employees,
    process_java_hungary_employees
]

exec_result = get_data(data_collectors)
dump_stats(exec_result, console=False)
