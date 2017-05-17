from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

MONGODB_HOST = '34.210.191.245'
MONGODB_PORT = 27017
DBS_NAME = 'main'
COLLECTION_NAME = 'startups'
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DBS_NAME][COLLECTION_NAME]
FIELDS = {'name': True, 'image': True, '_id': False}
FUNDS = {'name': True, 'funding_rounds': True, '_id': False}

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/getData")
# def get_startups_test():
#     startups = collection.find(projection=FIELDS)
#     startups_names = []
#     for i in startups:
#         if i['name'] == 'Wetpaint':
#             startups_names.append(i['image'])
#     startups_names = json.dumps(startups_names, default=json_util.default)
#     connection.close()
#     return startups_names

@app.route("/data/flare.json")
def flare():
    return render_template("flare.json")


@app.route("/getFunds")
def get_funds_per_year():
    x = 'Frazier Technology Ventures'
    y = 2007
    funding = collection.find(projection=FUNDS)
    funds_collection = []
    for i in funding:
        for k in i['funding_rounds']:
            if k['funded_year'] == y:
                for l in k['investments']:
                    financial_org = l['financial_org']
                    if financial_org:
                        if financial_org['name'] == x:
                            temp = {
                                'fund': x,
                                'year': y,
                                'paid': k['raised_amount'],
                                'target': i['name']
                            }
                            funds_collection.append(temp)
    funds_collection = json.dumps(funds_collection, default=json_util.default)
    connection.close()
    return funds_collection

@app.route('/testData')
def test():
    funding = collection.find(projection=FUNDS)
    funds_collection = []
    for i in funding:
        for k in i['funding_rounds']:
            funds_collection.append(k['funded_year'])
            funds_collection.sort()
    funds_collection = json.dumps(funds_collection, default=json_util.default)
    connection.close()
    return funds_collection

app.run(host='0.0.0.0',port=5000,debug=True)
