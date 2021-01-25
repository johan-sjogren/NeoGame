import random
from .pyneogame.gym import Gym
from .pyneogame.Agent.GreedyAgent import GreedyAgent
from .pyneogame.Agent.DeepQAgent import DeepQAgent
from .pyneogame.Agent.RandomAgent import RandomAgent
from .pyneogame.Engine import Game
from pathlib import Path

# This will be run by the eval worker

def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    print("Starting Evaluation.....")

    output = {}
    output["result"] = [
    {
        "test_split": {
        }
    }
    ]

    N_GAMES = 100000
    DQ_FILE = str(Path(__file__).parent.absolute())+'/models/dq_agent.h5'

    print("Evaluating model: {}".format(user_submission_file))

    game = Game()
    player = DeepQAgent(state_size=len(game.get_player_state()),
                           actions=game.get_actions())
    player.load(user_submission_file)
    random_agent = RandomAgent()
    greedy_agent = GreedyAgent()
    dq_agent = DeepQAgent(state_size=len(game.get_player_state()),
                         actions=game.get_actions()).load(DQ_FILE)

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
        output["result"][0]["test_split"]["Score_vs_" + agent_name] = score

    output["result"][0]["test_split"]["Total"] = total_score
    output["submission_result"] = output["result"][0]

    print(output)
    print("Evaluation Done!")
    return output
