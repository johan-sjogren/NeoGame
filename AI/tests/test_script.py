from random import shuffle
import unittest

import numpy as np

from pyneogame.Engine import Game
from pyneogame.Agent.QTableAgent import QTableAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.ActiveTable import ActiveTable
from pyneogame.Agent.DeepQAgent import DeepQAgent
from pyneogame.Agent.RandomAgent import RandomAgent
from pyneogame.Agent.PolicyGradient import ReInforce, ReInforce_v2


class test(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_random(self):
        print("Running routine agent test for Random Agent")
        self.game.test_player(RandomAgent())

    def test_QTable(self):
        print("Running routine agent test for Q Table")
        self.game.test_player(QTableAgent())

    def test_DeepQAgent(self):
        print("Running routine agent test for Deep Q Agent")
        self.game.test_player(
            DeepQAgent(state_size=len(self.game.get_player_state()),
                       actions=self.game.get_actions()))

    def test_ReInforce(self):
        print("Running routine agent test for ReInforce")
        self.game.test_player(
            ReInforce(state_size=len(self.game.get_player_state()),
                      actions=self.game.get_actions()))

    def test_ReInforce_v2(self):
        print("Running routine agent test for ReInforce v2")
        self.game.test_player(
            ReInforce_v2(state_size=len(self.game.get_player_state()),
                         actions=self.game.get_actions()))

    def test_greedy(self):
        """
        Checking basic functionality of the greedy agent class
        """
        print("Running 3 tests on the greedy agent + routine agent test")
        self.game.test_player(GreedyAgent())

        actions = self.game.get_actions()
        agent = GreedyAgent(value_func=self.game.calc_score)

        state_1 = [1, 2, 3, 4, 4, 0, 0, 1, 3]
        action_1 = agent.get_action(state_1, actions).tolist()
        # There are three equally good solutions here...
        self.assertTrue(action_1 == [1, 1, 0, 0, 0] or
                        action_1 == [1, 0, 1, 0, 0] or
                        action_1 == [0, 1, 1, 0, 0])

        state_2 = [2, 3, 3, 4, 4, 0, 4, 1, 4]
        action_2 = agent.get_action(state_2, actions).tolist()
        self.assertTrue(action_2 == [0, 1, 1, 0, 0])

        state_3 = [0, 2, 2, 4, 4, 1, 2, 0, 3]
        action_3 = agent.get_action(state_3, actions).tolist()
        self.assertTrue(action_3 == [0, 1, 1, 0, 0])
        print("Greedy agent passed all tests")

    def test_engine(self):
        """
        Checking basic functionality of the Game class
        """
        print('Running Engine tests')

        # Make sure that deal_cards function actually randomizes
        for _ in range(10):
            setup_1 = self.game.get_env()
            setup_2 = self.game.deal_cards().get_env()
            com_arrs = [np.array_equal(a, b) for x, y in zip(
                setup_1, setup_2) for a, b in zip(x, y)]
            # There is a chance that arrays will be similar just by chance
            self.assertTrue(sum(com_arrs) < 3,
                            msg=[com_arrs, setup_1, setup_2])

        # Test that the scoring function returns expected values
        self.assertTrue(self.game.calc_score([1, 1, 1, 1, 1], [2, 3, 4, 0, 0]) == 5)
        self.assertTrue(self.game.calc_score([2, 3, 4, 0, 0], [1, 1, 1, 1, 1]) == 10)
        self.assertTrue(self.game.calc_score([2, 3, 4, 0, 0], [1, 1, 1, 1, 1]) == 10)
        self.assertTrue(self.game.calc_score([1, 1, 1, 1, 1], [2, 3, 4, 0, 0]) == 5)

        # Check that scoring never exceeds the highest possible score
        for _ in range(500):
            np.random.seed(_)
            arr1 = np.random.randint(0, 5, 4)
            np.random.seed(500+_)
            arr2 = np.random.randint(0, 5, 4)

            max_score = (self.game.n_cards_on_table + self.game.n_cards_to_play)**2
            self.assertTrue(self.game.calc_score(arr1, arr2) <= max_score,
                            msg=[arr1, arr2, _, 500+_])

        # Scoring should be insensitive to permutations
        for _ in range(4):
            arr1 = [1, 1, 4, 4, 2]
            shuffle(arr1)
            arr2 = [2, 3, 4, 0, 0]
            shuffle(arr2)
            self.assertTrue(self.game.calc_score(arr1, arr2) == 7)
            self.assertTrue(self.game.calc_score(arr2, arr1) == 6)

        # The list of actions should be equal for all game instances
        for _ in range(10):
            game1 = Game()
            game2 = Game()
            self.assertTrue((game1.get_actions() == game2.get_actions()).all())

        print('Engine tests completed')


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
