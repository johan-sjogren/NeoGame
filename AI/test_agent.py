
#/usr/bin/python3
"""load a trained model and test it!"""

from pyneogame.gym import Gym
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.DeepQAgent import DeepQAgent
from pyneogame.Engine import Game


name = "dq_agent.h5"

game = Game()
player = DeepQAgent(state_size=len(game.get_player_state()),
                       actions=game.get_actions())
player.load(name)
opponent = GreedyAgent()



# b) Setup the gym
gym = Gym(player, opponent)

# d) Run test
gym.test(50000)
gym.eval()