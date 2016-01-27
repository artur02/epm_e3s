# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:42:23 2016

@author: Artur_Herczeg
"""

import json
import os

from datetime import date, timedelta

def load_json_file(fileName):
    f = open(fileName)
    return json.load(f)

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
def isFileStale(path, validity = timedelta(days=1)):
    mod_date = date.fromtimestamp(os.path.getmtime(path))
    curr_date = date.today()
    delta = curr_date - mod_date
    return delta >= validity
