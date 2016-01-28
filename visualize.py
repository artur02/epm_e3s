# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:37:39 2016

@author: Artur_Herczeg
"""

import os.path

import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook

from config import DATA_PATH


class Dump(object):
    
    def __init__(self, result, plot_kind=None, plot_name=None):
        self.name, self.df = result
        self.plot_kind = plot_kind
        self.plot_name = plot_name
    
    def _print_plot(self):
        if self.plot_kind is not None:
            fig = plt.figure()
            self.df.plot(kind=self.plot_kind, title=self.name)
            return fig
        else:
            return None
    
    def _save_plot(self, fig):
        if self.plot_name is not None:
            figurepath = os.path.join(DATA_PATH, '%s_%s.png' % (self.plot_name, self.name))

            plt.gcf().subplots_adjust(left=0.35)
            fig.savefig(figurepath, dpi=300)
       
    def to_console(self):
        print("================ %s ================ \n" % self.name)
        print(self.df)
        print("--- Count: %d" % len(self.df))
        fig = self._print_plot()
        self._save_plot(fig)
        
        print("\n")
        
    def to_excel(self, path=None, sheet='Sheet1'):
        if path is None:
            path = "%s.%s" % (os.path.join(DATA_PATH, self.name), 'xlsx')
        
        if os.path.exists(path):
            book = load_workbook(path)
            writer = pd.ExcelWriter(path, engine='openpyxl')
            writer.book = book
            writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
            self.df.to_excel(writer, sheet)
            writer.save()
        else:
            self.df.to_excel(path, sheet)