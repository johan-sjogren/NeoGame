
# !/usr/bin/python3
"""The Gym module used for training and
    evaluating agents playing NeoGame

Usage:
    from pyneogame.Gym import Gym

    gym = Gym(<Agent>, <Agent>, <Game>)

    gym.train()
    gym.eval_exp_states()

    gym.test()
    gym.eval()

TODO: Define and implement tests
TODO: Add ActiveTable specific code?
"""

from collections import defaultdict

import numpy as np
from tqdm import tqdm

from .Engine import Game

class Gym:

    def __init__(self, player, opponent, game=Game(), disable_progress_bar=False):

        self.game = game
        self.player = player
        self.opponent = opponent

        # Placeholder for bookkeeping visited states (?)
        self.exp_states = None

        self.player_wins = None
        self.opponent_wins = None
        self.num_test = None
        self.optimal_wins = None
        self.optimal_losses = None
        self.last_test = None

        self.disable_progress_bar = disable_progress_bar

    def _get_reward(self, player_score, opponent_score):
        """Get the reward of one round

        Only reward the player agent if player wins

        Arguments:
            player_score
            opponent_score

        TODO: Implement other reward functions?
        """
        return player_score - opponent_score

    def train(self, num_episodes=10000):
        """Train the player agent against the opponent

        During training the player agent deploys an exploration strategy

        Arguments:
            num_episodes (int) - The number of episodes in the training
        """

        self.game.restart()

        self.exp_states = defaultdict(int)

        for i in tqdm(range(num_episodes), disable=self.disable_progress_bar):

            self.game.deal_cards()

            possible_actions = self.game.get_actions()

            player_state = self.game.get_player_state()
            player_action = self.player.get_action(player_state,
                                                   possible_actions,
                                                   explore_exploit='explore')

            # Bookkeep visited states (?)
            player_state_str = np.array2string(player_state)
            self.exp_states[player_state_str] += 1

            opponent_state = self.game.get_opponent_state()
            opponent_action = self.opponent.get_action(opponent_state,
                                                       possible_actions)

            self.game.set_player_action(player_action)\
                     .set_opponent_action(opponent_action)

            player_score, opponent_score = self.game.get_scores()

            reward = self._get_reward(player_score, opponent_score)
            self.player.learn(player_state,
                              player_action,
                              reward)
            self.player.learn(opponent_state,
                              opponent_action,
                              -reward)
        
        print("Training done!")

    def eval_exp_table(self):
        """Get the min/max exp_states

        TODO: Add a more descriptive print
        """

        maximum = max(self.exp_states, key=self.exp_states.get)
        minimum = min(self.exp_states, key=self.exp_states.get)
        print(maximum, self.exp_states[maximum])
        print(minimum, self.exp_states[minimum])

    def test(self, num_test=1000):
        """Test the player agent against the opponent

        During test the player agent chooses the action
        producing the highest reward

        Arguments:
            num_episodes (int) - The number of test games
        """

        self.num_test = num_test
        self.player_wins = 0
        self.opponent_wins = 0
        self.optimal_wins = 0
        self.optimal_losses = 0

        self.game.restart()

        for test in range(num_test):
            self.game.deal_cards()
            possible_actions = self.game.get_actions()

            player_state = self.game.get_player_state()
            player_action = self.player.get_action(player_state,
                                                   possible_actions,
                                                   explore_exploit='exploit')
            opponent_state = self.game.get_opponent_state()
            opponent_action = self.opponent.get_action(opponent_state,
                                                       possible_actions)

            (self.game.set_player_action(player_action)
                      .set_opponent_action(opponent_action))
            player_score, opponent_score = self.game.get_scores()

            if player_score > opponent_score:
                self.player_wins += 1
            elif opponent_score > player_score:
                self.opponent_wins += 1

            optimal_result = self.game.get_optimal_result()
            if optimal_result > 0:
                self.optimal_wins += 1
            elif optimal_result < 0:
                self.optimal_losses += 1

        print("Testing done!")

    def eval(self):
        """Evaluate performance of the two agents
            Prints win, loss, tie ratio for player
            and compares this to optimal play
        """

        ratio_player_win = self.player_wins / self.num_test
        ratio_opponent_win = self.opponent_wins / self.num_test
        ratio_tie = 1.0 - ratio_player_win - ratio_opponent_win

        print("\nPlayer Test Results:")
        print("\tWins   {0:.2f}%".format(100.0 * ratio_player_win))
        print("\tLosses {0:.2f}%".format(100.0 * ratio_opponent_win))
        print("\tTie {0:.2f}%".format(100.0 * ratio_tie))

        ratio_optimal_win = self.optimal_wins / self.num_test
        ratio_optimal_loose = self.optimal_losses / self.num_test
        ratio_optimal_tie = 1.0 - ratio_optimal_win - ratio_optimal_loose

        print("\nOptimal Results:")
        print("\tPlayer   {0:.2f}%".format(100.0 * ratio_optimal_win))
        print("\tOpponent {0:.2f}%".format(100.0 * ratio_optimal_loose))
        print("\tTie {0:.2f}%".format(100.0 * ratio_optimal_tie))

        # Ratio of win, loss diff between player and optimal
        # positive if the player beats opponent
        relative_result = ((ratio_player_win - ratio_opponent_win) /
                           (ratio_optimal_win - ratio_optimal_loose))

        print("\nResults Player Relative Optimal:")
        print("\tWins   {0:.2f}%".format(100.0 * ratio_player_win / ratio_optimal_win))
        print("\tLosses {0:.2f}%".format(100.0 * ratio_opponent_win / ratio_optimal_loose))
        print("\tScore {0:.2f}%".format(100.0 * relative_result))

        if self.last_test is not None:
            print("Diff from last test score is {0:.2f}%".format(100.0 * (relative_result - self.last_test)))
        self.last_test = relative_result

