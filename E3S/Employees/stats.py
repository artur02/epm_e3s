# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 14:47:45 2016

@author: Artur_Herczeg
"""
import E3S.Employees.DSL as dsl

class EmployeeStats(object):
    selectedColumns = ['name', 'title']
    
    def __init__(self, dataFrame):
        self.df = dataFrame
        
    def getNonbillables(self):
        nonbillable = self.df.billable == False
        active = self.df.status != dsl.EmployeeStatus.EXTENDEDLEAVE
        
        return self.df[nonbillable & active][self.selectedColumns]
        
    def getRMs(self):
        return self.df[self.df.isRM == True][self.selectedColumns]
        
    def getCities(self):
        return self.df.groupby(self.df.city).city.count()
        
    def getTitleCount(self):
        return self.df.groupby(self.df.title).title.count().sort_values()