import pandas as pd
import numpy as np
from collections import defaultdict

from . import BaseAgent
from . import QTableAgent

class ActiveTable(QTableAgent.QTableAgent):
    """
    This Agent implements a form of active learning.
    The agent keeps track of how often a state has been visited and
    can make recommendations of states to revisist.
    Currently recommends the least visited state
    """

    def __init__(self, **args):
        super().__init__(**args)
        self.state_count = defaultdict(int)

    def recommend_state(self, as_string=False):
        minimum = min(self.state_count, key=self.state_count.get)
        if as_string:
            return minimum
        else:
            return list(int(x) for x in minimum)

    def seen_state(self, state):
        state_str = ''.join([str(x) for x in state])
        try:
            self.state_count[state_str]
            return True
        except:
            return False

    def learn(self, state, action, reward, new_state=None):
        """
        Calls the learn function of the standard QTable
        Counts the number of times a state is visited
        """

        super().learn(state, action, reward, new_state=None)
        state_str = ''.join([str(x) for x in state])
        self.state_count[state_str] += 1

        return self

    def save(self, filename):
        raise NotImplementedError

    def load(self, filename):
        raise NotImplementedError


