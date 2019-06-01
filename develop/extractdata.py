import pandas as pd
import json
import urllib.request
import numpy as np
import pymongo

import districtlist 
import analysis     
pd.set_option('mode.chained_assignment', None)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)   
db = client.analysis
collection = db.districtdata

dict_data = {}
dict_value =[]
print(f'data retrieval in progress ...')
for data in districtlist.distlist:
    
    url =f'https://www12.statcan.gc.ca/rest/census-recensement/CPR2016.json?lang=E&dguid={data}&topic=10&theme=5&notes=0'
    analysis.main(url)
    df_copy = analysis.languages_df.copy()
    df_copy.drop (['comment'], 1, inplace=True)
    df_copy.set_index(['rows'], inplace=True)
    records = json.loads(df_copy.to_json()).values()
    collection.insert_many(records)
    
print(f'data retrieval done.')
 