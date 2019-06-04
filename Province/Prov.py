import pandas as pd
import json
import urllib.request
import numpy as np
import pymongo

import Retrievedguids as gd
import analysis    

pd.set_option('mode.chained_assignment', None)

#conn = 'mongodb://localhost:27017'
#client = pymongo.MongoClient(conn)   
#db = client.analysis
#collection = db.districtdata

dict_data = {}
dict_value =[]

#Setting up the new dataframe

#Set up the framework 
row_names = ["district", "geo-code", "Responses", "English", "French", "Non-official", "Aboriginal", "Afro-Asiatic",\
                "Austro-Asiatic", "Austronesian", "Dravidian", "European", "Indo-Aryan", "Iranian", "East Asian", "African",\
                "Other", "Chinese", "Tibeto-Burman", "Tai-Kadai", "Turkic"]
comments = ["Electoral Districts", "Link to Stascan information", "Single Responses: Mothertongue", "None", "None", "None",\
               "None", "mainly Arabic, Hebrew, Somali", "includes Khmer, Vietnamese", "includes Tagalog (Philipino)",\
               "includes Tamil", "English and French excluded", "includes Hindi, Urdu...", "mainly Farsi and Kurdish",\
                "Japanese, Korean, Mongolic", "Niger-Congo, Nilo-Saharan and Creole", "Sign languages and other languages",\
               "mainly Mandarin and Cantonese", "None", "mainly Thai and Lao", "None"]

language_dict = {}
language_dict["rows"] = row_names
language_dict["comment"] = comments

print(f'data retrieval in progress ...')
for data in gd.provlist:
    
    url =f'https://www12.statcan.gc.ca/rest/census-recensement/CPR2016.json?lang=E&dguid={data}&topic=10&theme=5&notes=0'
    district, languages = analysis.main(url)    
    language_dict[district] = languages
    #df_copy = analysis.languages_df.copy()
    #df_copy.drop (['comment'], 1, inplace=True)
    #df_copy.set_index(['rows'], inplace=True)
    #records = json.loads(df_copy.to_json()).values()
    #collection.insert_many(records)
    


    ###print(len(languages), len(comments), len(row_names))
    # When the dictionary is complete, a new dataframe can be put together:

languages_df = pd.DataFrame.from_dict(language_dict)

    #languages_df

print(f'data retrieval done.')
languages_df.to_pickle("prov_languages.pkl")
print("DF saved")