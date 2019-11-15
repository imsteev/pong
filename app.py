import json
import requests

from flask import Flask, request


app = Flask('ping-pong')


@app.route('/')
def home():
    return "hello"


@app.route('/game', methods=["GET", "POST"])
def game():

    return "Hello, time to play ping pong"


if __name__ == "__main__":
    app.run(debug=True)
