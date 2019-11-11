import pandas as pd
import numpy as np

from . import BaseAgent
from ..Engine import Game

class GreedyAgent(BaseAgent.BaseAgent):

    def __init__(self, value_func=Game.calc_score):
        self.value_func = value_func

    def __str__(self):
        return "Greedy Agent"

    def get_action(self, state, actions, as_string=False):
        player_hand = np.array(state[:5])
        opponent_table = np.array(state[-2:])

        # possibles = [player_hand[a == 1] for a in actions]

        def diff_score(player, opponent):
            return (self.value_func(player, opponent) -
                    self.value_func(opponent, player))

        greedy_list = list(
                        map(
                            lambda a: (diff_score(
                                player_hand[a == 1], opponent_table), a),
                            actions))

        # print(sorted(greedy_list, key=lambda x: x[0])[::-1])
        _, action = max(greedy_list, key=lambda x: x[0])

        if as_string:
            return ''.join([str(x) for x in action])
        else:
            return action
        return 0

    def learn(self, state, action, reward, new_state=None):
        # Static strategy, just return self
        return self

    def save(self, filename):
        raise NotImplementedError

    def load(self, filename):
        raise NotImplementedError