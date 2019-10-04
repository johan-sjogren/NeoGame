#/usr/bin/python3
"""A sample training script for training and testing agents playing NeoGame"""

from pyneogame.gym import Gym
from pyneogame.Agent.QTableAgent import QTableAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent

# a) Setup the agents
player = QTableAgent(unexplored=1)
opponent = GreedyAgent()

# b) Setup the gym
gym = Gym(player, opponent)

# c) Run training
gym.train()
gym.eval_exp_table()

# d) Run test
gym.test()
gym.eval()
