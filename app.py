"""
Simple Flask server that can host a single round-robin tournament (in-memory, for now).
"""
import json
import os

from flask import Flask, jsonify, redirect, request, url_for

from registry import Player
from round_robin import get_matchups, round_robin

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8888

app = Flask(__name__)

PLAYER_POOL = None
ROUND_ROBIN_GENERATOR = None
CURRENT_ROUND = 0


@app.route('/', methods=['GET'])
def index():
    global CURRENT_ROUND
    global PLAYER_POOL
    global ROUND_ROBIN_GENERATOR
    matchups_str = "No players registered"
    if ROUND_ROBIN_GENERATOR is not None:
        try:
            matchups = get_matchups(next(ROUND_ROBIN_GENERATOR), PLAYER_POOL)
            matchups_str = '\n'.join(["{0} ({1}) v. {2} ({3})".format(
                p1.name, p1_seed, p2.name, p2_seed) for ((p1, p1_seed), (p2, p2_seed)) in matchups])
            CURRENT_ROUND += 1
        except StopIteration:
            CURRENT_ROUND = 0
            matchups_str = "Tournament finished!"

    if CURRENT_ROUND == 0:
        return matchups_str
    else:
        return f"""Round {CURRENT_ROUND}
        {matchups_str}"""


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
