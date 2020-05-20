#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------
import argparse
from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS, cross_origin
from waitress import serve
from collections import defaultdict
# Holds flask configurations
import config
from pyneogame.Engine import Game
from pyneogame.Agent.RandomAgent import RandomAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.PolicyGradient import ReInforce
from pyneogame.Agent.DeepQAgent import DeepQAgent

app = Flask(__name__, 
            static_folder="Web/build/",
            template_folder="Web/build")
CORS(app)  # , support_credentials=True)

game = Game()

# TODO: Loop over several available models. Maybe check entire models folders
DQ_FILE = 'AI/models/dq_best.h5'
PG_FILE = 'AI/models/pg_best.h5'

# Create PG model
pg_agent = ReInforce(state_size=len(game.get_player_state()),
                     actions=game.get_actions())
pg_agent.load(PG_FILE, custom_objects={'reward_loss': pg_agent.reward_loss})

dq_agent = DeepQAgent(state_size=len(game.get_player_state()),
                     actions=game.get_actions()).load(DQ_FILE)

# All agents included is listed here
agent_dict = {'Random': RandomAgent(),
              'Greedy': GreedyAgent(),
              'DeepQ': dq_agent
#               'PolicyGrad': pg_agent
              }


# Serve the webpage
@app.route('/')
def index():
    return render_template('index.html')


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
    # get_action has to be treated in two separate ways due to an
    # early(and poor) choice on how to implement the epsilon greed
    # explore vs exploit strategy. # TODO: Strategy as a building block
    if isinstance(agent, (DeepQAgent, ReInforce)):
        return_dict['opponent_action'] = agent.get_action(
            game.get_opponent_state(),
            actions,
            explore_exploit='exploit').tolist()
    else:
        return_dict['opponent_action'] = agent.get_action(
            game.get_opponent_state(),
            actions).tolist()

    return_dict['player_hand'] = game.player_hand.tolist()
    return_dict['player_table'] = game.player_table.tolist()
    return_dict['opponent_hand'] = game.opponent_hand.tolist()
    return_dict['opponent_table'] = game.opponent_table.tolist()
    return jsonify(return_dict)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Changing between development and production')
    parser.add_argument('--env', metavar='N', type=str, required=True,
                        help='dev or prod.')
    parser.add_argument('--host', type=str, required=False, default='0.0.0.0',
                        help='host')
    parser.add_argument('--port', type=str, required=False, default='8080',
                        help='port')

    args = vars(parser.parse_args())

    if 'prod' in args['env']:
        serve(app, host=args['host'], port=args['port'])
    elif 'dev' in args['env']:
        app.run(debug=True, host='0.0.0.0') 
