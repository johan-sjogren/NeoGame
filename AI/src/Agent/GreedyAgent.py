import pandas as pd
import numpy as np
from . import BaseAgent


class GreedyAgent(BaseAgent.BaseAgent):

    def __init__(self, value_func=None):
        self.value_func = value_func

    def get_action(self, state, actions, as_string=False):
        player_hand = np.array(state[:5])
        opponent_table = state[-2:]

        possibles = [player_hand[a == 1] for a in actions]

        def diff_score(player, opponent):
            return (self.value_func(player, opponent) -
                    self.value_func(opponent, player))

        greedy_list = list(
                        map(
                            lambda a: (diff_score(
                                player_hand[a == 1], opponent_table), a),
                            actions))

        _, action = max(greedy_list, key=lambda x: x[0])

        if as_string:
            return action
        else:
            return list(int(x) for x in action)
        return 0

    def learn(self, state, action, reward, new_state=None):
        # Static strategy, just return self
        return self
