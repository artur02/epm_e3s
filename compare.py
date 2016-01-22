# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 15:42:52 2016

@author: Artur_Herczeg
"""

import pandas as pd
import numpy as np

def report_diff(x):
    return x[0] if x[0] == x[1] else '{} AAAAAAAAAAAAA {}'.format(*x)

def getDiffLines(df1, df2):
    return df1.index[np.any(df1 != df2,axis=1)]
    
def loadData(fileName):
    return pd.read_pickle(fileName)
    
df1 = loadData("compare/data1.pickle")
df2 = loadData("compare/data2.pickle")

ne_stacked = (df1 != df2).stack()
changed = ne_stacked[ne_stacked]
changed.index.names = ['id', 'col']

difference_locations = np.where(df1 != df2)
changed_from = df1.values[difference_locations]
changed_to = df2.values[difference_locations]
changes = pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)

print(changes)