# !/usr/bin/python3
"""A sample training script for training and testing agents playing NeoGame"""

from pyneogame.gym import Gym
from pyneogame.Agent.QTableAgent import QTableAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.DeepQAgent import DeepQAgent
from pyneogame.Engine import Game

FILE_NAME = "dq_agent"
TRAINING_ITERATIONS = 100000
NUM_EPISODES = 5
UPDATE_INTERVAL = int(TRAINING_ITERATIONS / NUM_EPISODES)
TEST_ITERATIONS = 10000

# a) Setup the agents
game = Game()
player = DeepQAgent(state_size=len(game.get_player_state()),
                    actions=game.get_actions(), 
                    update_interval=UPDATE_INTERVAL, 
                    filename=FILE_NAME)
opponent = GreedyAgent()

# b) Setup the gym
gym = Gym(player, opponent, game)

# c) Run training
for i in range(NUM_EPISODES):
    gym.train(num_episodes=UPDATE_INTERVAL)
    gym.eval_exp_table()
    gym.test(int(TEST_ITERATIONS / NUM_EPISODES))
    gym.eval()

# d) Run test
gym.test(TEST_ITERATIONS)
gym.eval()

player.save(FILE_NAME)
