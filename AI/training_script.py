# !/usr/bin/python3
"""A sample training script for training and testing agents playing NeoGame"""

from pyneogame.gym import Gym
from pyneogame.Agent.QTableAgent import QTableAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.PolicyGradient import ReInforce
from pyneogame.Agent.DeepQAgent import DeepQAgent
from pyneogame.Engine import Game
# Start the game
game = Game()

# a) Setup the agents
player = ReInforce(state_size=len(game.get_player_state()),
                   actions=game.get_actions())
player.load('models/pg_best.h5',
            custom_objects={'reward_loss': player.reward_loss})
# player = DeepQAgent(state_size=len(game.get_player_state()),
                #    actions=game.get_actions())
opponent = GreedyAgent()

# b) Setup the gym
gym = Gym(player, opponent, game)

# c) Run training
gym.train(num_episodes=2000)
gym.eval_exp_table()

# d) Run test
gym.test()
gym.eval()

player.save('models/pg_best.h5')
# player.save('models/dq_best.h5')
