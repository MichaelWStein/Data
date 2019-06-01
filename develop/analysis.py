import pandas as pd
import json
import urllib.request
import numpy as np


#Setting up the first column with information - this needs to be automated for all electoral districts. key is the name of the electoral district, 
#languages the calculated numbers for the languages (from the dataframe)
# A single cell is extracted with df.loc[index, "columname"]

#Functions for calaculating more complex language groups
def european():
    languages = [139, 140, 141, 160, 164, 176, 196, 204, 258]
    return(calculation(languages))

def asiatic():
    languages = [203, 206, 207]
    return(calculation(languages))

def african():
    languages = [209, 226, 127]
    return(calculation(languages))

def other():
    languages =[229, 263]
    return(calculation(languages))
    
def calculation(languages):
    speakers = 0
    for i in range(0, len(languages)):
        speakers = speakers + surv2_df.loc[languages[i], "DATA"]
    return(speakers)
        


def main(url):
    global surv2_df
    global languages_df
    #This program rreads in the statscan data for one specific district. It is not complete, probably not needed, 
    #because we will be going the *.csv route.
    ###print("start")
    #url = "https://www12.statcan.gc.ca/rest/census-recensement/CR2016Geo.json?lang=E&geos=FED&cpt=35"
    #url = "https://www12.statcan.gc.ca/rest/census-recensement/CPR2016.json?lang=E&dguid=2013A000435004&topic=10&notes=0"
    data = urllib.request.urlopen(url).read()

    #Statscan data has a 'head' that needs to be removed, then the json can be read properly.
    data1 = data[2:]
    output = json.loads(data1)
    # content = json.dumps(output, indent = 4, sort_keys=True) - only needed if we want to check transfer
    # print(content)


    #Getting the information for creation of the dataframe

    info_surv = output.get("DATA")
    column_names = output.get("COLUMNS")


    #Creating the dataframe

    info_surv2 = np.transpose(info_surv)

    data_dict = {}

    for i in range (0, len(column_names)):
        data_dict[column_names[i]] = info_surv2[i]

    surv_df = pd.DataFrame.from_dict(data_dict)

    surv_df.rename(columns={'TEXT_NAME_NOM':'TEXT','T_DATA_DONNEE':'DATA'}, inplace=True)
    surv_df.head(10)


    #need complete display for analysis
    pd.set_option('display.max_rows', 1000)
    ###print(list(surv_df))
    #Simplifying Dataframe - Really unnecessary, but makes work easier
    surv2_df = surv_df[['PROV_TERR_NAME_NOM','GEO_UID','GEO_NAME_NOM', 'HIER_ID', 'TEXT', 'DATA']]
    surv2_df.drop(surv2_df.index[0:12], axis=0, inplace=True)
    surv2_df.drop(surv2_df.index[269:], axis=0, inplace=True)
    surv2_df = surv2_df.reset_index()
    surv2_df.drop(['index'], axis=1, inplace=True)

    #Checking if numeric information in data
    #print(surv2_df.loc[0, "DATA"] - surv2_df.loc[1, "DATA"])

    surv2_df

    #may want to change column name for T_DATA...; also make sure that there are numbers in there - may bestrings (as from JSON)

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
    
    
    languages = [surv2_df.loc[1, "GEO_NAME_NOM"], surv2_df.loc[1, "GEO_UID"], surv2_df.loc[1, "DATA"], surv2_df.loc[3, "DATA"],\
                surv2_df.loc[4, "DATA"], surv2_df.loc[5, "DATA"], surv2_df.loc[6, "DATA"], surv2_df.loc[90, "DATA"],\
                (surv2_df.loc[110, "DATA"]+surv2_df.loc[137, "DATA"]), surv2_df.loc[114, "DATA"], surv2_df.loc[131, "DATA"],\
                european(), surv2_df.loc[178, "DATA"], surv2_df.loc[191, "DATA"], asiatic(), african(), other(),\
                surv2_df.loc[234, "DATA"], surv2_df.loc[243, "DATA"], surv2_df.loc[248, "DATA"], surv2_df.loc[252, "DATA"]]
    district =  surv2_df.loc[1, "GEO_NAME_NOM"]  
    ###print(district)

    language_dict[district] = languages

    ###print(len(languages), len(comments), len(row_names))
    # When the dictionary is complete, a new dataframe can be put together:
    languages_df = pd.DataFrame.from_dict(language_dict)

    languages_df
