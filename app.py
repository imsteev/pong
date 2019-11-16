"""
Simple Flask server that can host a single round-robin tournament (in-memory, for now).
"""
import json
import os

from flask import Flask, jsonify, redirect, request, url_for

from registry import Player
from round_robin import round_robin

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8888

app = Flask(__name__)

PLAYER_POOL = None
ROUND_ROBIN_GENERATOR = None
CURRENT_ROUND = 0


@app.route('/', methods=['GET'])
def index():
    global CURRENT_ROUND
    global ROUND_ROBIN_GENERATOR
    matchups = "No players registered"
    if ROUND_ROBIN_GENERATOR is not None:
        try:
            matchups = next(ROUND_ROBIN_GENERATOR)
            CURRENT_ROUND += 1
        except StopIteration:
            matchups = "Tournament finished!"

    return f"Round {CURRENT_ROUND}: {matchups}"


@app.route('/tournament', methods=['GET', 'POST'])
def tournament():
    global PLAYER_POOL
    global ROUND_ROBIN_GENERATOR
    if ROUND_ROBIN_GENERATOR is None:
        PLAYER_POOL = [Player(**p) for p in request.get_json()]
        ROUND_ROBIN_GENERATOR = round_robin(len(PLAYER_POOL))
    return jsonify(PLAYER_POOL)


@app.route('/reset', methods=['GET'])
def reset():
    global CURRENT_ROUND
    global PLAYER_POOL
    global ROUND_ROBIN_GENERATOR
    CURRENT_ROUND = 0
    PLAYER_POOL = None
    ROUND_ROBIN_GENERATOR = None
    return redirect(url_for('index'))


if __name__ == "__main__":

    host = os.getenv("FLASK_HOST", DEFAULT_HOST)
    port = os.getenv("FLASK_PORT", DEFAULT_PORT)
    debug = os.getenv("FLASK_DEBUG", True)

    app.run(host=host, port=port, debug=debug)
