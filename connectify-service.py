'''
ConnectifyAPI

This is a backend api service for Connectify Web, Android and iOS applications.

Licensed by Connectify.

Designed and Coded by Shrikant.
'''
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello User! This is the Connectify backend API for Web, Android and iOS applications. Welcome aboard !"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
