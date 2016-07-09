'''
ConnectifyAPI

This is a backend api service for Connectify Web, Android and iOS applications.

Licensed by Connectify.

Designed and Coded by Shrikant.
'''
from flask import Flask
from flask_cors import CORS, cross_origin

HOST = "0.0.0.0"
PORT = 3000
ALLOWED_ORIGINS = "*"

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})

@app.route("/connectifyapi/hello")
@cross_origin()
def hello():
    return "Hello User! This is the Connectify backend API for Web, Android and iOS applications. Welcome aboard !"

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
