#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------
from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS, cross_origin
from collections import defaultdict
# Holds flask configurations
import config
from pyneogame.Engine import Game
from pyneogame.Agent.RandomAgent import RandomAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent

app = Flask(__name__,
            static_folder="Web/build/static",
            template_folder="Web/build")
CORS(app, support_credentials=True)

game = Game()

# All agents included is listed here
agent_dict = {'Random': RandomAgent(),
              'Greedy': GreedyAgent()}


# Serve the webpage
@app.route('/')
def index():
    return render_template('index.html')
    # return send_file('Web/public/index.html')
    # return send_file('Web/public/index.html')    


# GET for getting game info and available agents
@app.route('/ai/game/v1.0', methods=['GET'])
def get_game():
    return_dict = {}
    return_dict['opponents'] = list(agent_dict.keys())
    return jsonify(return_dict)


# POST for game state and opponent action from specific agent/opponent
@app.route('/ai/game/v1.0', methods=['POST'])
def post_game():
    return_dict = {}
    opp_name = request.json.get('opponent_name', "")
    try:
        agent = agent_dict[opp_name]
        return_dict['opponent_name'] = opp_name
    except KeyError:
        agent = RandomAgent()
        return_dict['opponent_name'] = 'Default'

    actions = game.get_actions()
    game.deal_cards()
    return_dict['version'] = '0.1'
    return_dict['opponent_action'] = agent.get_action(
        game.get_opponent_state(),
        actions).tolist()

    return_dict['player_hand'] = game.player_hand.tolist()
    return_dict['player_table'] = game.player_table.tolist()
    return_dict['opponent_hand'] = game.opponent_hand.tolist()
    return_dict['opponent_table'] = game.opponent_table.tolist()
    return jsonify(return_dict)


if __name__ == '__main__':
    app.run(debug=True)
