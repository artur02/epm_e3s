# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:42:23 2016

@author: Artur_Herczeg
"""

import json
import os

def load_json_file(fileName):
    f = open(fileName)
    return json.load(f)

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
