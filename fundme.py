from flask import Flask
from flask import render_template
from pymongo import MongoClient
import collections
import json
import ssl

MONGODB_HOST = '34.210.191.245'
MONGODB_PORT = 27017
DBS_NAME = 'main'
COLLECTION_NAME = 'startups'
FUNDS = {'name': True, 'funding_rounds': True, '_id': False}

connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DBS_NAME][COLLECTION_NAME]
app = Flask(__name__)

@app.route("/data/flare.json")
def flare():
    return render_template("flare.json")

@app.route('/')
def main():
    funds_collection = collection.find(projection=FUNDS)

    not_filtered = []
    for i in funds_collection:
        for k in i['funding_rounds']:
            temp = {
                'name': k['funded_year'],
                'children': {'name': i['name'], 'size': k['raised_amount']}
            }
            not_filtered.append(temp)
    print not_filtered
    final_structure = []
    year = 2012
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
    return render_template("index.html")

# app.run(host='0.0.0.0', port=5000, debug=True)

ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ctx.load_cert_chain('/etc/pki/tls/private/ssl.cert', '/etc/pki/tls/private/ssl.key')
app.run(use_reloader=True, host='0.0.0.0',port=443,ssl_context =ctx)
