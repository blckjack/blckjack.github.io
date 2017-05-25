from flask import Flask
from flask import render_template
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps
import collections
import json
import re

app = Flask(__name__)

MONGODB_HOST = '34.210.191.245'
MONGODB_PORT = 27017
DBS_NAME = 'main'
COLLECTION_NAME = 'startups'
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DBS_NAME][COLLECTION_NAME]
FUNDS = {'name': True, 'funding_rounds': True, '_id': False}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data/flare.json")
def flare():
    return render_template("flare.json")

@app.route('/updateFundingsData')
def getAllFundsAlpha():
    funds_collection = collection.find(projection=FUNDS)
    
    not_filtered = []
    for i in funds_collection:
        for k in i['funding_rounds']:
            temp = {
                'name': k['funded_year'],
                'children': {'name': i['name'], 'size': k['raised_amount']}
            }
            not_filtered.append(temp)

    final_structure = []
    year = 2005
    while year < 2015:
        i = 0
        filtered_data = []
        while i < len(not_filtered):
            child = not_filtered[i]['children']
            if not_filtered[i]['name'] == year:
                filtered_data.append(child)
            i += 1
        structured_data = {
            'name': year,
            'children': filtered_data
        }
        final_structure.append(structured_data)
        year += 1
            
    output = {
        'name': 'funds',
        'children': final_structure
    }

    with open('templates/flare.json', 'w') as outfile:
        output = json.dump(output, outfile)
    connection.close()

    return 'Data updated!'


def pure_number(s):
    s = re.sub('^\\D*', '', s)
    mult = 1
    
    num_replace = {
        'B' : 1000000000,
        'M' : 1000000,
        'k' : 1000
    }
    
    while s[-1] in num_replace:
        mult *= num_replace[s[-1]]
        s = s[:-1]

    return float(s) * mult


app.run(host='0.0.0.0',port=5000,debug=True)
