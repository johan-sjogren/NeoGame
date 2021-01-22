import random
from pyneogame.gym import Gym
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.DeepQAgent import DeepQAgent
from pyneogame.Agent.RandomAgent import RandomAgent
from pyneogame.Engine import Game


BENCHMARK_FILE = 'models/dq_agent.h5'
DQ_FILE = 'models/dq_agent.h5'

print("Starting Evaluation.....")
N_GAMES = 1000



print("Benchmarking model: {}".format(BENCHMARK_FILE))
game = Game()
player = DeepQAgent(state_size=len(game.get_player_state()),
                       actions=game.get_actions())
player.load(BENCHMARK_FILE)
random_agent = RandomAgent()
greedy_agent = GreedyAgent()
dq_agent = DeepQAgent(state_size=len(game.get_player_state()),
                     actions=game.get_actions()).load(DQ_FILE)
#agent_list = [random_agent, greedy_agent, dq_agent]

# All agents included is listed here
agent_dict = {'Random': random_agent,
              'Greedy': greedy_agent,
              'DeepQ': dq_agent
}

total_score = 0
for agent_name in agent_dict:
    gym = Gym(player, agent_dict[agent_name])
    gym.test(N_GAMES)
    n_wins, n_losses = gym.get_results()
    score = n_wins - n_losses
    total_score += score
    print("got score {} vs {} agent".format(score, agent_name))

print("Total score is: {}".format(total_score))
