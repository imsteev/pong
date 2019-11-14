import json
import requests

from flask import Flask, request

from request_helpers import IS_GET, IS_POST

app = Flask('ping-pong')


@app.route('/')
def home():
    return "hello"


@app.route('/game', methods=["GET", "POST"])
def game():
    if IS_POST():
        print(request.)

    return "Hello, time to play ping pong"


if __name__ == "__main__":
    app.run(debug=True)
