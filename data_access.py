# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:02:36 2016

@author: Artur_Herczeg
"""

import json
import os.path

from requests.auth import HTTPBasicAuth

from utilities import load_json_file, create_dir
import E3S.Employees.DSL as dsl
from E3S.Employees.data import EmployeeData
import E3S.connection as e3s
import E3S.Employees.stats as stats

FOLDER_DATA = 'data'

def get_auth_data():
    config = load_json_file("password.cfg")

    user = config["service"]["user"]
    pas = config["service"]["pass"]
    return (user, pas)



def get_employees(auth, name, filters):

    def evaluate_filters(query):
        for f in filters:
            query = f(query)
        return query

    query = e3s.get_empty_query()
    evaluate_filters(query)

    query_full = {
        'metaType': 'meta:people-suite:people-api:com.epam.e3s.app.people.api.data.EmployeeEntity',
        'query': json.dumps(query)
    }

    raw_data_path = os.path.join(FOLDER_DATA, 'rawdata.json')

    if not os.path.exists(raw_data_path):
        print("No local data cache (rawdata.json) found, getting data from service...")
        result = e3s.execute_query(query_full, auth)
        empdata = EmployeeData(data=result)
        empdata.save_as_json(raw_data_path)
    else:
        print("Local data cache (%s) found, reading..." % raw_data_path)
        result = load_json_file(raw_data_path)
        empdata = EmployeeData(data=result)

    empdata.save_as_sqlite(name)

    print("Total number of employees: %d" % result["total"])
    return empdata.data_frame

def print_stat(df, title, plot=None):
    print("================ %s ================ \n" % title)
    print(df)
    print("--- Count: %d" % len(df))
    if plot is not None:
        df.plot(kind=plot)
    print("\n")

def process_java_hungary_employees(auth):
    java_hungary_filters = [
        lambda x: dsl.filter_by_country(x, "Hungary"),
        lambda x: dsl.filter_by_primaryskill(x, "Java"),
        lambda x: e3s.set_limits(x, (0, 1000))
    ]
    data = get_employees(auth, name='JavaHungary', filters=java_hungary_filters)
    empstat = stats.EmployeeStats(data)

    print_stat(empstat.get_nonbillables(), "Non-billables")
    print_stat(empstat.get_RMs(), "RMs")
    print_stat(empstat.get_cities(), "Cities")
    print_stat(empstat.get_title_count(), "Titles", plot='barh')

create_dir(FOLDER_DATA)

USER, PASSWORD = get_auth_data()
AUTH = HTTPBasicAuth(USER, PASSWORD)

process_java_hungary_employees(AUTH)
