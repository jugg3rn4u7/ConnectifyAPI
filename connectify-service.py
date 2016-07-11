'''
ConnectifyAPI

This is a backend api service for Connectify Web, Android and iOS applications.

Licensed by Connectify.

Designed and Coded by Shrikant.
'''
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import dbsettings
import json
import sys

HOST = "0.0.0.0"
PORT = 3000
ALLOWED_ORIGINS = "*"

connection = dbsettings.connection
mongoClient = MongoClient(connection['HOST'], connection['PORT'])
db = mongoClient[connection['DATABASE']]

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})

@app.route("/connectifyapi/hello")
@cross_origin()
def hello():
    return "Hello User! This is the Connectify backend API for Web, Android and iOS applications. Welcome aboard !"

@app.route("/connectifyapi/register", methods=["POST"])
@cross_origin()
def create_user():
    try:
        json_data = request.get_json(force=True)
    	#dataDict = json.load(json_data)
    	users = db['user-collection']
    	users.insert(json_data)
    	return jsonify(result='ok')
    except:
	e = sys.exc_info()[0]
  	print('error %s' % e)
	return jsonify(result='error')

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
