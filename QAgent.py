import pandas as pd
import numpy as np
from BaseAgent import BaseAgent


class QTableAgent(BaseAgent):

    def __init__(self, learning_rate=0.1, epsilon=0.9,
                 decay_rate=1e-5, unexplored=0,
                 discount_rate=0.95):

        self.Q = {}                # Q-table (Dict)
        self.learning_rate = learning_rate   # Learning rate
        self.discount_rate = discount_rate        # Discount rate

        # Exploration parameters
        self.epsilon = epsilon         # Starting exploration probability
        self.decay_rate = decay_rate
        self.unexplored = unexplored   # Default value of unexplored state
        # This can be used in on-policy learning to force exploration

    def _get_Q(self, state, action):
        if state in self.Q and action in self.Q[state]:
            return self.Q[state][action]
        else:
            return self.unexplored

    def _set_Q(self, state, action, value):
        if state in self.Q:
            self.Q[state][action] = value
        else:
            self.Q[state] = {action: value}

    def get_action(self, state, actions,
                   explore_exploit='none',
                   as_string=False):
        """ Implements an epsilon greedy algorithm for exploration/exploitation

        Args:
            state (list): String representation of the current game state
            actions (list): list of available actions
            explore_exploit: Options 'explore', 'exploit' or 'none'(default)
        Returns:
           string/list: String or list representation of the chosen action
        """
        # Convert lists to string representations
        actions_str = [''.join([str(x) for x in y]) for y in actions]
        state_str = ''.join([str(x) for x in state])
        exp_tradeoff = np.random.uniform(0, 1)

        if explore_exploit == 'explore':
            action = np.random.choice(actions_str,  1)[0]
        # If this number > greater than epsilon --> exploitation
        elif exp_tradeoff > self.epsilon or explore_exploit == 'exploit':
            _, action = max(map(lambda m: (self._get_Q(state_str, m), m),
                                actions_str),
                            key=lambda x: x[0])
        # Else doing a random choice --> exploration
        else:
            action = np.random.choice(actions_str,  1)[0]
        # Reduce epsilon (because we need less and less exploration)
        self.epsilon *= np.exp(-self.decay_rate)
        if as_string:
            return action
        else:
            return list(int(x) for x in action)

    def update_Q(self, state, action, reward):
        """Updates the Q-table values via the Q-learning algorithn
            Q[state, action] =
                 Q[state, action] +
                    learning_rate * (reward +
                                        discount_rate * MAX(Q[new_state]) -
                                            Q[state, action])
        Args:
            state (string):  String representation of the current game state
            action (string): String representation of the action performed
            reward (float): Direct reward of the action on the state

        Returns:
            self
        """
        # max_q = max(map(lambda a: self._get_Q(new_state, a), actions))
        # Since our actions doesn't influence the next step (randomly
        # drawn cards) the new state is not of importance
        max_q = 0
        new_value = self._get_Q(state, action) * (1 - self.learning_rate) + \
            self.learning_rate * (reward + max_q*self.discount_rate)

        self._set_Q(state, action, new_value)
        return self

    def learn(self, state, action, reward, new_state=None):
        """Performs the alorithms learning stage.

        Args:
            state (list): representation of game state
            action (list): representation of chosen action
            reward (int/float): Immediate reward
            new_state (list, optional): representation of
                                               new game state.
                                               Defaults to None.

        Returns:
            self
        """
        # Convert list to string representation
        action_str = ''.join([str(x) for x in action])
        state_str = ''.join([str(x) for x in state])

        # For Q-learning all that is needed is to update the table
        self.update_Q(state_str, action_str, reward)
        return self

    def get_QTable(self, as_dataframe=False):
        if as_dataframe:
            return pd.DataFrame.from_dict(self.Q)
        else:
            return self.Q

    def save(self, filename):
        self.get_QTable(as_dataframe=True).to_csv(filename)
        return self

    def load(self, filename):
        self.Q = pd.read_csv(filename,
                             dtype={0: str}
                             ).set_index('Unnamed: 0').to_dict()
        return self


class DeepQAgent(BaseAgent):
    pass


class GreedyAgent(BaseAgent):

    def __init__(self, value_func=None):
        self.value_func = value_func

    def get_action(self, state, actions, as_string=False):
        print('Greedy actions: ', actions)
        print('Greedy state: ', state)
        player_hand = np.array(state[:5])
        opponent_table = state[-2:]

        print(player_hand, opponent_table)
        # max_q = max(map(lambda a: self.get_Q(new_state, a), actions))

        possibles = [player_hand[a == 1] for a in actions]
        print('Possible action: ', possibles)
        # print(list(self.value_func(x, opponent_table) for x in possibles))
        print(list(
                map(
                    lambda a: (self.value_func(player_hand[a == 1], opponent_table), a),
                        actions)))
        # print(max(map(lambda a: (value_func(a, opponent_table), a),
        #                possibles)))
        action = actions[0]
        if as_string:
            return action
        else:
            return list(int(x) for x in action)
        return 0

    def learn(self, state, action, reward, new_state=None):
        # Static strategy, just return self
        return self
