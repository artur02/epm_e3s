# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 10:41:19 2016

@author: Artur_Herczeg
"""
import data_access
from data_access import process_java_hungary_employees
from data_access import process_dotnet_hungary_employees

def executeSteps(steps):
    return { name:df for name, df in [step(data_access.AUTH) for step in steps]}

steps = [ 
    process_dotnet_hungary_employees, 
    process_java_hungary_employees 
]

exec_result = executeSteps(steps)
