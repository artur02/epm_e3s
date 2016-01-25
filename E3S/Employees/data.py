# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 11:04:55 2016

@author: Artur_Herczeg
"""

import json
import datetime
import pandas as pd

from sqlalchemy import create_engine

class EmployeeData(object):

    data_dir = "data"
    engine = create_engine('sqlite:///%s/e3s.db' % data_dir, echo=False)

    def __init__(self, *args, **kwargs):
        #pylint: disable=R0204
        self._data = kwargs.get('data', None)

        if self._data is not None:
            self.data_frame = self.getdataframe(self._data)
        else:
            table = kwargs.get('table', None)
            self.data_frame = pd.read_sql_table(table, self.engine)


    def save_as_json(self, path):
        raw_file = open(path, 'w')
        raw_file.truncate()
        raw_file.write(json.dumps(self._data))
        raw_file.close()

    @classmethod
    def getdataframe(cls, jsondata):
        items = jsondata['items']

        idx = pd.Series([item['data']['upsaidSum'] for item in items])
        # pylint: disable=C0301
        d = {
            'name': pd.Series([item['data']['fullNameSum']['full'] for item in items], index=idx),
            'city': pd.Series([item['data']['citySum'] for item in items], index=idx),
            'country': pd.Series([item['data']['countrySum'] for item in items], index=idx),
            'email': pd.Series([item['data']['emailSum'] for item in items], index=idx),
            'manager': pd.Series([item['data']['manager'] for item in items], index=idx),
            'native name': pd.Series([item['data']['nativename'] for item in items], index=idx),
            'primary skill': pd.Series([item['data']['primarySkillSum'] for item in items], index=idx),
            'start work date': pd.Series([item['data']['startworkdate'] for item in items], index=idx),
            'superior': pd.Series([item['data']['superior'] for item in items], index=idx),
            'unit': pd.Series([item['data']['unit'] for item in items], index=idx),
            'upsaid': pd.Series([item['data']['upsaidSum'] for item in items], index=idx),
            'billable': pd.Series([item['data']['billable'] > 0 for item in items], index=idx),
            'title': pd.Series([item['data']['titleSum'] for item in items], index=idx),
            'orgcategory': pd.Series([item['data'].get('orgcategory') for item in items], index=idx),
            'project': pd.Series([item['data'].get('project') for item in items], index=idx),
            'isRM': pd.Series([item['data'].get('isRm') for item in items], index=idx, dtype=bool),
            'status': pd.Series([item['data'].get('status') for item in items], index=idx),
        }
        # pylint: enable=C0301

        df = pd.DataFrame(d, index=idx)
        return df

    def save_as_sqlite(self, name):
        filename = "employees_%s_%s" % (name, str(datetime.date.today()))
        self.data_frame.to_sql(filename, self.engine, if_exists='replace')
