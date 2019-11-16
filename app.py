"""
Simple Flask server that can host a single round-robin tournament (in-memory, for now).
"""
import json
import os

from flask import Flask, jsonify, redirect, request, send_from_directory, url_for

from models.player import Player
from round_robin import construct_matchups, format_matchup, round_robin

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8888

app = Flask(__name__, static_url_path='/static')

CACHE = dict()
CACHE['players'] = None
CACHE['round_robin'] = None
CACHE['current_round'] = None
CACHE['current_round_num'] = 0


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/tournament', methods=['GET', 'POST'])
def tournament():
    global CACHE
    if CACHE['round_robin'] is None:
        CACHE['players'] = [Player(**p) for p in request.get_json()]
        CACHE['round_robin'] = round_robin(len(CACHE['players']))
    return f"{len(CACHE['players'])} player(s) registered. Navigate to /next_round to start!"


@app.route('/players', methods=['GET', 'POST'])
def players():
    global CACHE
    if request.method == 'GET':
        return jsonify(CACHE['players'])
    return url_for('index')


@app.route('/next_round', methods=['GET'])
def next_round():
    global CACHE
    if CACHE['round_robin']:
        try:
            next_round = next(CACHE['round_robin'])
            CACHE['current_round'] = construct_matchups(next_round, CACHE['players'])
            CACHE['current_round_num'] += 1
        except StopIteration:
            return redirect(url_for('reset'))
    return redirect(url_for('index'))


@app.route('/reset', methods=['GET'])
def reset():
    global CACHE
    CACHE['round_robin'] = None
    CACHE['current_round'] = None
    CACHE['current_round_num'] = 0
    return redirect(url_for('index'))


if __name__ == "__main__":

    host = os.getenv("FLASK_HOST", DEFAULT_HOST)
    port = os.getenv("FLASK_PORT", DEFAULT_PORT)
    debug = os.getenv("FLASK_DEBUG", True)

    app.run(host=host, port=port, debug=debug)
