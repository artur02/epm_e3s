# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 13:15:38 2016

@author: Artur_Herczeg
"""

from E3S.Employees.data import EmployeeData
import numpy as np
import pandas as pd

emps1 = EmployeeData(table="employees_2016-01-22")
emps2 = EmployeeData(table="employees_2016-01-22")

df1 = emps1.dataFrame
df2 = emps2.dataFrame
#df2.loc[22, 'title'] = 'AAAAAAAAAAAAAAAAAAAAAAAA'

ne_stacked = (df1 != df2).stack()
changed = ne_stacked[ne_stacked]
changed.index.names = ['id', 'col']

difference_locations = np.where(df1 != df2)
changed_from = df1.values[difference_locations]
changed_to = df2.values[difference_locations]
changes = pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)

print(changes[changes['from'].notnull() & changes['to'].notnull()])