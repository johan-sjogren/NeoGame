import pandas as pd
import numpy as np
from . import BaseAgent


class DeepQAgent(BaseAgent.BaseAgent):
    """ Deep Q-learning Agent
    This implementation will take a state as input,
    estimate the Q value Q(s, a_x) for all actions a_x and
    select the action with the highest Q value if exploiting.
    """

    def __init__(self, actions=None):
        self.dnn_model = self.make_model()

    def make_model(self):
        pass

    def get_action(self, state, actions,
                   explore_exploit='none',
                   as_string=False):

        pass

    def learn(self, state, action, reward, new_state=None):
        pass
