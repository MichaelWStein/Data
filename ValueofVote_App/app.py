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
    collection = db.seat_value_language
    analysis = collection.find()
    contents = list()

    contents = [data for data in analysis]

    df = pd.DataFrame(contents)
    df.set_index('rows',inplace=True)
    df = df.iloc[2:]
    df = df[['comment', 'Canada', 'id_seats', 'act_seats', 'value']]
    df.rename(columns={'id_seats': 'seats, ideal case','act_seats':'seats, calculating by district'}, inplace=True)

    app.logger.info(df.head())
    return render_template('languages.html',  tables=[df.to_html()], titles=df.columns.values)


@app.route("/about")
def about():

    return render_template('about.html')


if __name__ == "__main__":
    #app.run()
    app.run(debug=True)
