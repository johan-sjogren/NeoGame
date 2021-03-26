import random
import os
import zipfile
from .pyneogame.gym import Gym
from .pyneogame.Agent.GreedyAgent import GreedyAgent
from .pyneogame.Agent.DeepQAgent import DeepQAgent
from .pyneogame.Agent.RandomAgent import RandomAgent
from .pyneogame.Engine import Game
from pathlib import Path


class BadSubmissionError(Exception):
    """Exception raised for incorrect submission files."""

    def __init__(self):
        self.message = ("Submitted Zipfile doesn't contain expected files")
        super().__init__(self.message)


def evaluate(test_annotation_file, user_submission_file,
             phase_codename, **kwargs):
    # This will be run by the eval worker
    print("Starting Evaluation.....")

    output = {}
    output["result"] = [
        {
            "test_split": {}
        }
    ]

    N_GAMES = 5000
    DQ_FILE = str(Path(__file__).parent.absolute())+'/models/dq_agent.h5'
    game = Game()

    print("Evaluating model: {}".format(user_submission_file))
    print('Extracting from zipfile')
    files_to_remove = []
    zipf = zipfile.ZipFile(user_submission_file)
    agentfile = [x for x in zipf.namelist() if 'CustomAgent.py' in x]
    h5file = [x for x in zipf.namelist() if 'CustomAgent.h5' in x]
    csvfile = [x for x in zipf.namelist() if 'CustomAgent.csv' in x]
    if len(h5file) + len(csvfile) > 2:
        raise BadSubmissionError()

    if len(agentfile) == 1:
        agentfile = agentfile[0]
        files_to_remove.append(zipf.extract(agentfile))
    else:
        raise BadSubmissionError()

    if len(h5file) == 1:
        h5file = h5file[0]
        files_to_remove.append(zipf.extract(h5file))
    else:
        h5file = None

    if len(csvfile) == 1:
        csvfile = csvfile[0]
        files_to_remove.append(zipf.extract(csvfile))
    else:
        csvfile = None

    print('Instantiating submitted agent')
    from CustomAgent import CustomAgent
    if h5file is not None:
        player = CustomAgent.from_game_and_h5(game, h5file)
    elif csvfile is not None:
        player = CustomAgent.from_game_and_csv(game, csvfile)
    else:
        player = CustomAgent.from_game(game)

    print('Instantiate opponents')
    agent_dict = {}
    random_agent = RandomAgent()
    agent_dict['Random'] = random_agent
    greedy_agent = GreedyAgent()
    agent_dict['Greedy'] = greedy_agent
    try:
        dq_agent = DeepQAgent(state_size=len(game.get_player_state()),
                              actions=game.get_actions()).load(DQ_FILE)
        agent_dict['DeepQ'] = dq_agent
    except IOError:
        print('DQ file not found. Excluded from test')

    print('Running test cycle')
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
    print("Clean up")

    for filename in files_to_remove:
        if os.path.isfile(filename):
            os.remove(filename)
    return output
