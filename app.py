"""
Simple Flask server that can host a single round-robin tournament (in-memory, for now).
"""
import json
import os

from flask import Flask, jsonify, redirect, request, url_for

from models.player import Player
from round_robin import construct_matchups, round_robin

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8888

app = Flask(__name__)

PLAYER_POOL = None
ROUND_ROBIN_GENERATOR = None
CURRENT_ROUND = 0
CURRENT_MATCHUPS = None


@app.route('/', methods=['GET'])
def index():
    global CURRENT_MATCHUPS
    global CURRENT_ROUND
    global PLAYER_POOL
    global ROUND_ROBIN_GENERATOR

    if CURRENT_MATCHUPS:
        matchups_str = '\n'.join(
            ["{0} ({1}) v. {2} ({3})".format(p1.name, p1_seed, p2.name, p2_seed)
             for ((p1, p1_seed), (p2, p2_seed)) in CURRENT_MATCHUPS])
        return f"""Round {CURRENT_ROUND}
        {matchups_str}"""
    else:
        CURRENT_ROUND = 0
        return "No matchups. Reset the tournament or start a new one!"


@app.route('/tournament', methods=['GET', 'POST'])
def tournament():
    global PLAYER_POOL
    global ROUND_ROBIN_GENERATOR
    if ROUND_ROBIN_GENERATOR is None:
        PLAYER_POOL = [Player(**p) for p in request.get_json()]
        ROUND_ROBIN_GENERATOR = round_robin(len(PLAYER_POOL))
    return jsonify(PLAYER_POOL)


@app.route('/next_round', methods=['GET'])
def next_round():
    global CURRENT_MATCHUPS
    global CURRENT_ROUND
    global ROUND_ROBIN_GENERATOR
    if ROUND_ROBIN_GENERATOR is not None:
        try:
            CURRENT_MATCHUPS = construct_matchups(next(ROUND_ROBIN_GENERATOR), PLAYER_POOL)
            CURRENT_ROUND += 1
        except StopIteration:
            CURRENT_MATCHUPS = None
    return redirect(url_for('index'))


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
