import random
import sys
# from .pyneogame.Agent import BaseAgent
import h5py


class CustomAgent:

    @classmethod
    def from_game(cls, game):
        return cls()

    @classmethod
    def from_game_and_h5(cls, game, h5file):
        with h5py.File(h5file, 'r') as f:
            print('H5')
            for key in f.keys():
                print(key)
        return cls()

    @classmethod
    def from_game_and_csv(cls, game, csvfile):
        with open(csvfile) as infile:
            print('CSV')
            print(infile.read())
        return cls()

    def __str__(self):
        return "Random Agent"

    def get_action(self, state, actions, explore_exploit='none'):

        action = random.choice(actions)

        if as_string:
            return ''.join([str(x) for x in action])
        else:
            return action
        return 0

    def learn(self, state, action, reward):
        # Static strategy, just return self
        return self
