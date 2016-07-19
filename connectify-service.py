'''
ConnectifyAPI

This is a backend api service for Connectify Web, Android and iOS applications.

Licensed by Connectify.

Designed and Coded by Shrikant.
'''
# Imports
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from twilio.rest import TwilioRestClient 
from twilio import TwilioRestException
import dbsettings
import json
import sys
import os
import time
import md5
import re
from random import randint

# CONSTANTS
HOST = "0.0.0.0"
PORT = 3000
ALLOWED_ORIGINS = "*"

TWILIO_AUTH_TOKEN = "561ba8512c01086b5b770673bd6c3043"
TWILIO_ACCOUNT_SID = "ACbd24bae146abdebcad083493af4a7017"
TWILIO_SENDER_NUMBER = "+12013800248"

connection = dbsettings.connection
mongoClient = MongoClient(connection['HOST'], connection['PORT'])
db = mongoClient[connection['DATABASE']]

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, 'files')

VALID_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

@app.route("/connectifyapi/hello")
@cross_origin()
def hello():
    return "Hello User! This is the Connectify backend API for Web, Android and iOS applications. Welcome aboard !"

@app.route("/connectifyapi/register", methods=["POST"])
@cross_origin()
def create_user():
    try:
        json_data = request.get_json(force=True)
	phoneNumber = re.sub('[()-]', '', json_data["phoneNumber"])
	password = json_data["password"]
    	users = db['user-collection']
	m = md5.new()
	m.update(phoneNumber + "_" + password)
	salt = m.hexdigest()
	print(phoneNumber)
	print(password) 
	print(salt)
    	users.find_one_and_update({ "phoneNumber": phoneNumber }, { "$set": { "password": password, "salt": salt }})
    	return jsonify(result='ok')
    except Exception as e:
	e = sys.exc_info()[0]
  	print('error %s' % e)
	print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
	return jsonify(result='error')

@app.route("/connectifyapi/send-code", methods=["POST"])
@cross_origin()
def send_code():
    try:
	json_data = request.get_json(force=True)
	receiverPhoneNumber = json_data["phoneNumber"]
	twilioClient = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
	
	code = randint(10000, 99999)
	txtMessage = "Hi User! This is Connectify. Your verification code is {0}.".format(code)
	twilioClient.messages.create(body=txtMessage, from_=TWILIO_SENDER_NUMBER, to=receiverPhoneNumber)
	users = db['user-collection']
	_user = users.find_one({"phoneNumber": receiverPhoneNumber})
	if(_user == None):
		users.insert({ "phoneNumber": receiverPhoneNumber, "password": "", "verified": 0, "code": code, "salt": "" })
	else:
		users.update_one(_user, { 
			"$set": { "phoneNumber": receiverPhoneNumber, "password": "", "verified": 0, "code": code, "salt": "" }
		})
	return jsonify(result='ok')
    except TwilioRestException as e:
	print(e)
	return jsonify(result='error')

@app.route("/connectifyapi/verify-code", methods=["POST"])
@cross_origin()
def verify_code():
    try:
	json_data = request.get_json(force=True)
	phoneNumber = json_data["phoneNumber"]
	code = json_data["code"]
	users = db["user-collection"]
	_user = users.find_one({ "phoneNumber": phoneNumber })
	saved_code = _user["code"]
	if(saved_code == code):
	    users.update(users.find_one({ "phoneNumber": phoneNumber }), { "$set": { "verified": 1 }})
	    return jsonify(result='verified')
	else:
	    return jsonify(result='unverified')
    except Exception as e:
        print('error %s' % e)
	print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        return jsonify(result='error')

@app.route("/connectifyapi/check-number", methods=["POST"])
@cross_origin()
def checkNumber():
    try:
	json_data = request.get_json(force=True)
        phoneNumber = json_data["phoneNumber"]
        users = db["user-collection"]
        _user = users.find_one({ "phoneNumber": phoneNumber })
        if(_user == None):
            return jsonify(result='ok')
        else:
            return jsonify(result='exists')
    except Exception as e:
	print('error %s' % e)
	print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        return jsonify(result='error')

@app.route("/connectifyapi/upload-avatar", methods=["POST"])
@cross_origin()
def uploadAvatar():
    try:
	raw_data = request.data
	unix_time = str(time.time()).split(".")[0]
	new_file = os.path.join(UPLOAD_FOLDER, unix_time)
	with open(new_file, "w+") as f:
	    f.write(raw_data)
	return jsonify(result="ok")
    except Exception as e:
	print('Error %s' % e)
	return jsonify(result="error")

@app.route("/connectifyapi/authenticate", methods=["POST"])
@cross_origin()
def authenticate():
    try:
	json_data = request.get_json(force=True)
	salt = json_data["salt"]
	users = db["user-collection"]
        _user = users.find_one({ "salt": salt })
        if(_user == None):
            return jsonify(result='invalid')
        else:
            return jsonify(result='valid')
    except Exception as e:
	print('Error %s' % e)
	return jsonify(result="error")

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
