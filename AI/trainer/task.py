#!/usr/bin/python3
"""A sample training script for training agents playing NeoGame on GCP"""

import os
import sys
import argparse

from .context import pyneogame
from pyneogame.gym import Gym
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.DeepQAgent import DeepQAgent
from pyneogame.Engine import Game

TASK_PATH = os.path.dirname(__file__)
TASK_NAME = os.path.basename(__file__).rstrip('.py')

TEST_ITERATIONS = 10000 # TODO: Should be defined in argparser

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", type=str, default="/".join([TASK_PATH, TASK_NAME]))
parser.add_argument("-e", "--train-episodes", type=int, default=5)
parser.add_argument("-i", "--train-iter", type=int, default=100000)
args = parser.parse_args()

output = args.output
train_episodes = args.train_episodes
train_iter = args.train_iter

if __name__ == "__main__":

    # Setup session
    if not os.path.exists(output):
        os.makedirs(output)

    game = Game()
    player = DeepQAgent(state_size=len(game.get_player_state()),
                        actions=game.get_actions(),
                        update_interval=train_iter//train_episodes, 
                        filename="/".join([output, TASK_NAME]))
    opponent = GreedyAgent()
    gym = Gym(player, opponent, game, disable_progress_bar=True)

    # Train
    for i in range(train_episodes):
        gym.train(num_episodes=train_iter//train_episodes)
        gym.eval_exp_table()
        gym.test(TEST_ITERATIONS//train_episodes)
        gym.eval()

    # Test
    gym.test(TEST_ITERATIONS)
    gym.eval()

    # Save model
    model = type(player).__name__
    player.save("/".join([output, model]))
