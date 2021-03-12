# !/usr/bin/python3
"""A sample training script for training and testing agents playing NeoGame"""

from pyneogame.gym import Gym
from pyneogame.Agent.QTableAgent import QTableAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.DeepQAgent import DeepQAgent
from pyneogame.Agent.RandomAgent import RandomAgent
from pyneogame.Engine import Game

# change this to what you want to name your model
MODEL_NAME = "models/new_dq_agent.h5"
RELOAD = False

# DQ model for training opponent
DQ_FILE = 'models/dq_agent.h5'

TRAINING_ITERATIONS = 100000
NUM_EPISODES = 5
UPDATE_INTERVAL = int(TRAINING_ITERATIONS / NUM_EPISODES)
TEST_ITERATIONS = 10000

# a) Setup the agents
game = Game()
player = DeepQAgent(state_size=len(game.get_player_state()),
                    actions=game.get_actions(), 
                    update_interval=UPDATE_INTERVAL, 
                    filename=MODEL_NAME,
                    verbose=1)

if RELOAD:
    player.load(MODEL_NAME)

random_agent = RandomAgent()
greedy_agent = GreedyAgent()
dq_agent = DeepQAgent(state_size=len(game.get_player_state()),
                     actions=game.get_actions()).load(DQ_FILE)

# Choose which agent your model will train against (random_agent, greedy_agent, or dq_agent)
opponent = greedy_agent

# b) Setup the gym
gym = Gym(player, opponent, game)

# c) Run training
for i in range(NUM_EPISODES):
    gym.train(num_episodes=UPDATE_INTERVAL)
    gym.eval_exp_table()
    gym.test(TEST_ITERATIONS)
    gym.eval()

player.save(MODEL_NAME)
