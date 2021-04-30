import argparse
import sys
import os
import zipfile
from pathlib import Path

sys.path.append(str(Path(Path(__file__).parent, '..').resolve()))

from pyneogame.Trainer import Gym
from pyneogame.Agent.RandomAgent import RandomAgent
from pyneogame.Engine import Game


class BadSubmissionError(Exception):
    """Exception raised for incorrect submission files."""

    def __init__(self):
        self.message = ("Submitted Zipfile doesn't contain expected files")
        super().__init__(self.message)


def evaluate(user_submission_file):
    # This will be run by the eval worker
    print("Starting Evaluation.....")

    output = {}
    output["result"] = [
        {
            "test_split": {}
        }
    ]

    N_GAMES = 50
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

    print('Testing agent')
    game.test_player(player)

    print('Running test cycle')
    total_score = 0
    for agent_name in agent_dict:
        gym = Gym(player, agent_dict[agent_name], game=game)
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('agentfile', help='Relative path to the Agent file')
    parser.add_argument('--additional', help='Additional csv or h5 file')
    args = parser.parse_args()

    submission_file_name = "submission.zip"
    with zipfile.ZipFile(submission_file_name, 'w') as outzip:
        outzip.write(args.agentfile, arcname='CustomAgent.py')
        if args.additional:
            file_type = args.additional.split('.')[-1]
            outzip.write(args.additional, arcname=f'CustomAgent.{file_type}')
    evaluate(submission_file_name)
