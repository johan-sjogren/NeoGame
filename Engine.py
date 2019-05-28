from random import shuffle
from itertools import combinations, permutations
import numpy as np


# TODO: Use player class to store hand/table info?
class Player(object):

    def __init__(self, score=0, hand=None, table=None, played=None):
        self.score = score
        self.hand = hand
        self.table = table
        self.played = played  # Card(s) played this round i.e. chosen actions


# TODO: Export as json
# TODO: Export only as list and json
# TODO: Generalize to multiplayer
class Game(object):

    def __init__(self, n_classes=5, card_per_class=5, episodes=5):
        deque = []
        self.n_classes = n_classes
        for x in range(n_classes):
            deque += [x] * card_per_class
        self.deque = np.array(deque)
        self.player_score = []
        self.opponent_score = []
        self.n_cards_in_hand = 5
        self.n_cards_to_play = 2
        self.n_cards_on_table = 2

        self.actions = None
        # Initial setup
        self.dealCards()

    @staticmethod
    def calc_score(player1_final, player2_final):
        return sum(Game.wins(x, y)
                   for x in player1_final
                   for y in player2_final)

    @staticmethod
    def wins(x, y, max=4, min=0):
        if x + 1 == y:
            return 1
        elif x == max and y == min:
            return 1
        else:
            return 0

    def shuffleDeck(self):
        shuffle(self.deque)
        return self

    def dealCards(self):
        """Randomly deal cards
        Returns:
            self
        """
        self.shuffleDeck()
        i = self.n_cards_on_table
        self.opponent_table = np.sort(self.deque[:i])
        j, i = i, i + self.n_cards_in_hand
        self.opponent_hand = np.sort(self.deque[j:i])
        j, i = i, i + self.n_cards_on_table
        self.player_table = np.sort(self.deque[j:i])
        j, i = i, i + self.n_cards_in_hand
        self.player_hand = np.sort(self.deque[j:i])
        return self

    def dealFromRecommendation(self, state):
        """
        Deals cards according to agent recommendation
        Returns:
            self
        """
        i = self.n_cards_in_hand
        self.player_hand = np.sort(state[:i])
        j, i = i, i + self.n_cards_on_table
        self.player_table = np.sort(state[j:i])
        j, i = i, i + self.n_cards_on_table
        self.opponent_table = np.sort(state[j:i])
        j, i = i, i + self.n_cards_in_hand

        temp_deque = list(self.deque)
        [temp_deque.remove(x) for x in state if x in temp_deque]
        shuffle(temp_deque)
        self.opponent_hand = np.sort(np.array(temp_deque[j:i]))

        return self

    def getEnv(self):
        return ((self.opponent_hand, self.opponent_table),
                (self.player_hand, self.player_table))

    def get_actions(self):
        '''
        The actions are possible ways that you can pick n_cards_to_play cards
        from hand. In this case represented by a boolean array for cards chosen
        '''

        if self.actions is None:
            n_ones = self.n_cards_to_play
            n_zeros = self.n_cards_in_hand-self.n_cards_to_play
            self.actions = np.array(list(set(
                            permutations(n_ones*[1]+n_zeros * [0],
                                         self.n_cards_in_hand))))

        return self.actions

    def get_player_state(self):
        state = np.concatenate([self.player_hand,
                                self.player_table,
                                self.opponent_table])
        return state

    def get_opponent_state(self):
        state = np.concatenate([self.opponent_hand,
                                self.opponent_table,
                                self.player_table])
        return state

    def set_player_action(self, action):
        # TODO: This should change the table and hand list
        self.player_action = action
        return self

    def set_opponent_action(self, action):
        # TODO: This should change the table and hand list
        self.opponent_action = action
        return self

    def score_player(self):
        player_cards = np.concatenate(
            [self.player_table,
             self.player_hand[self.player_action]])
        opponent_cards = np.concatenate(
            [self.opponent_table,
             self.opponent_hand[self.opponent_action]])
        score = Game.calc_score(player_cards, opponent_cards)
        self.player_score.append(score)
        return score

    def score_opponent(self):
        player_cards = np.concatenate(
            [self.player_table,
             self.player_hand[self.player_action]])
        opponent_cards = np.concatenate(
            [self.opponent_table,
             self.opponent_hand[self.opponent_action]])
        score = Game.calc_score(opponent_cards, player_cards)
        self.opponent_score.append(score)
        return score

    def get_scores(self):
        return self.score_player(), self.score_opponent()


def main():
    game = Game()

    # TODO: put in real test file
    for _ in range(10):
        setup_1, setup_2 = game.getEnv(), game.dealCards().getEnv()
        com_arrs = [np.array_equal(a, b) for x, y in zip(
            setup_1, setup_2) for a, b in zip(x, y)]
        # There is a chance that arrays will be similar just by chance
        assert sum(com_arrs) < 3
    assert game.calc_score([1, 1, 1, 1, 1], [2, 3, 4, 0, 0]) == 5
    assert game.calc_score([2, 3, 4, 0, 0], [1, 1, 1, 1, 1]) == 10
    assert Game.calc_score([2, 3, 4, 0, 0], [1, 1, 1, 1, 1]) == 10
    assert Game.calc_score([1, 1, 1, 1, 1], [2, 3, 4, 0, 0]) == 5

    for _ in range(4):
        arr1 = [1, 1, 4, 4, 2]
        shuffle(arr1)
        arr2 = [2, 3, 4, 0, 0]
        shuffle(arr2)
        assert Game.calc_score(arr1, arr2) == 7
        assert Game.calc_score(arr2, arr1) == 6


if __name__ == "__main__":
    main()
