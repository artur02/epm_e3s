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

    def get_nonbillables(self):
        #pylint: disable=C0121
        nonbillable = self.df.billable == False
        active = self.df.status != dsl.EMPLOYEE_STATUS['EXTENDEDLEAVE']

        return self.df[nonbillable & active][self.selectedColumns]

    def get_RMs(self):
        #pylint: disable=C0121
        return self.df[self.df.isRM == True][self.selectedColumns]

    def get_cities(self):
        return self.df.groupby(self.df.city).city.count().to_frame(name='cities')

    def get_title_count(self):
        return self.df.groupby(self.df.title).title.count().sort_values().to_frame(name='title count')
