#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------
# ----------------------------------------------
# TODO: Game måste blanda korten
from flask import Flask, jsonify, request, send_file
from collections import defaultdict
import sys
import os
sys.path.append(os.path.abspath('AI'))

from pyneogame.Engine import Game
from pyneogame.Agent.RandomAgent import RandomAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent

app = Flask(__name__)
game = Game()

agent_dict = {'Random': RandomAgent(),
              'Greedy': GreedyAgent()}


# Serve the webpage
@app.route('/')
def index():
    return send_file('Web/src/index.html')
    # return app.send_static_file('index.html')


# GET for getting game info and available agents
@app.route('/ai/game/v1.0', methods=['GET'])
def get_game():
    return_dict = {}
    return_dict['Available models'] = list(agent_dict.keys())
    print(return_dict)
    return jsonify(return_dict)


# POST for game state and opponent action from specific agent/opponent
@app.route('/ai/game/v1.0', methods=['POST'])
def post_game():
    return_dict = {}
    opp_name = request.json.get('opponent_name', "")
    print(opp_name)
    try:
        agent = agent_dict[opp_name]
        return_dict['opponent_name'] = opp_name  # 'RandomAgent'
    except KeyError:
        agent = RandomAgent()
        return_dict['opponent_name'] = 'Agent not found'
    # if opp_name == 'Random':
    #     agent = RandomAgent()
    # elif opp_name == 'Greedy':
    #     agent = GreedyAgent()
    # else:
    #     return_dict['opponent_name'] = "Random"  # 'RandomAgent'
    #     agent = RandomAgent()

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
