# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:42:23 2016

@author: Artur_Herczeg
"""

import json
import os

def loadJsonFile(fileName):
    f = open(fileName)
    return json.load(f)
    
def createDir(path):
    if not os.path.exists(path):
        os.makedirs(path)