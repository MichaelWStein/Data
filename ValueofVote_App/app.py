import os

import pandas as pd
import numpy as np

# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template,redirect
# from flask_sqlalchemy import SQLAlchemy
import pymongo
# from config import username,pwd,host
import pymysql
import json


import logging

# # Create an instance of Flask
app = Flask(__name__)

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)


@app.route("/")
def index():
    return render_template('index.html') 


@app.route("/prov_geojson")
def prov():
    """Return geojson for provinces"""

    prov_json_v2=os.path.join('data','test_prov_v2.json')

    with open(prov_json_v2, 'r') as pj:
        prov_data = json.load(pj)
       

    return jsonify(prov_data)

# @app.route("/prov_bubble")
# def prov_bubble():
#     """Return data for bubble chart for provinces"""

#     csvfile=os.path.join('data','prov_2016.csv')

#     csvfile="data/prov_2016.csv"
#     df_prov=pd.read_csv(csvfile)

#     data = {
#         "geo_name": df_prov['Geo_name'].values.tolist(),
#         "population": df_prov['Total'].values.tolist(),
#         "ridings": df_prov['Ridings'].values.tolist(),
#         "val_vote":df_prov['%ValueofVote'].values.tolist()
#     }
       
#     return jsonify(data)

@app.route("/electoral_districts")
def elec_dist():
    return render_template('electoral_districts.html') 


@app.route("/ed_geojson")
def ed_data():
    """Return geojson for provinces"""

    ed_json=os.path.join('data','electoral_2016.json')

    with open(ed_json, 'r') as ej:
        ed_data = json.load(ej)
       
        
    return jsonify(ed_data)

@app.route("/languages")
def languages():
    app.logger.info(f'/languages getting data from mongodb')
    db = client.analysis
    db_dist_languages_wcalc = db.dist_languages_wcalc
    db_prov_languages_wcalc = db.prov_languages_wcalc
    db_seat_value_language = db.seat_value_language

    df_dist_languages_wcalc= pd.DataFrame(list(db_dist_languages_wcalc.find()))
    df_dist_languages_wcalc.columns = df_dist_languages_wcalc.iloc[0]
    df_dist_languages_wcalc = df_dist_languages_wcalc.iloc[:, :-1]
    df_dist_languages_wcalc.reindex(df_dist_languages_wcalc.index.drop(0))
    df_dist_languages_wcalc.set_index('district',inplace=True) 
    app.logger.info(df_dist_languages_wcalc)
  
    #return render_template('languages.html', dist_json=json_str)
    return render_template('languages.html',  tables=[df_dist_languages_wcalc.to_html(classes='data')], titles=df_dist_languages_wcalc.columns.values)


@app.route("/about")
def about():

    return render_template('about.html')


if __name__ == "__main__":
    #app.run()
    app.run(debug=True)
