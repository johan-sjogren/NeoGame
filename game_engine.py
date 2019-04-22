from random import shuffle, sample
from itertools import permutations, combinations
import numpy as np


def calc_score(player1, player2):
    return sum(wins(x, y) for x in player1 for y in player2)


def wins(x, y, max=4, min=0):
    if x + 1 == y:
        return 1
    elif x == max and y == min:
        return 1
    else:
        return 0


# TODO: put in real test file
assert calc_score([1, 1, 1, 1, 1], [2, 3, 4, 0, 0]) == 5
assert calc_score([2, 3, 4, 0, 0], [1, 1, 1, 1, 1]) == 10

# TODO: Remove this garbage
'''
test = [1, 2, 3]
print(''.join(str(x) for x in test))
test2 = ''.join(str(x) for x in test)
test3 = [int(x) for x in list(test2)]
print(test3)

print(list(combinations(range(5), 3)))  #
test = list(combinations(range(5), 3))
print(test)
print([''.join([str(x) for x in y]) for y in test])
'''


class Game(object):

    def __init__(self, n_classes=5, card_per_class=5, episodes=5):
        deque = []
        self.n_classes = n_classes
        for x in range(n_classes):
            deque += [x] * card_per_class
        self.deque = deque  # np.array(deque)
        self.player_score = 0
        self.opponent_score = 0
        self.n_cards_in_hand = 5
        self.n_cards_to_play = 3
        self.n_cards_on_table = 2

        self.actions = None
        self.actions = self.shuffleDeck().dealCards().get_actions()

    def shuffleDeck(self):
        shuffle(self.deque)
        return self

    def dealCards(self):
        i = self.n_cards_on_table
        self.opponent_table = np.sort(self.deque[:i])
        j, i = i, i + self.n_cards_in_hand
        self.opponent_hand = np.sort(self.deque[j:i])
        j, i = i, i + self.n_cards_on_table
        self.player_table = np.sort(self.deque[j:i])
        j, i = i, i + self.n_cards_in_hand
        self.player_hand = np.sort(self.deque[j:i])
        return self

    def getEnv(self):
        return ((self.opponent_hand, self.opponent_table),
                (self.player_hand, self.player_table))

    def get_actions(self):
        '''
        The actions are possible ways that you can pick n_cards_to_play cards
        from hand by index
        '''
        if self.actions:
            return self.actions

        return list(combinations(range(self.n_classes), self.n_cards_to_play))

    def get_actions_string(self):
        return [''.join([str(x) for x in y]) for y in self.get_actions()]

    def get_player_state(self):
        return np.concatenate([self.player_hand,
                               self.player_table,
                               self.opponent_table])

    def get_player_state_string(self):
        return ''.join(str(x) for x in self.get_player_state())

    def get_opponent_state(self):
        return np.concatenate([self.opponent_hand,
                               self.opponent_table,
                               self.player_table])

    def get_opponent_state_string(self):
        return ''.join(str(x) for x in self.get_opponent_state())

    def player_action(self, cards_choosen):
        self.player_cards_chosen = cards_choosen
        return self

    def opponent_action(self, cards_choosen):
        self.opponent_cards_chosen = cards_choosen
        return self

    def score_player(self):
        player_cards = np.concatenate(
            [self.player_table, self.player_cards_chosen])
        opponent_cards = np.concatenate(
            [self.opponent_table, self.opponent_cards_chosen])
        score = calc_score(player_cards, opponent_cards)
        self.player_score += score
        return score

    def score_opponent(self):
        player_cards = np.concatenate(
            [self.player_table, self.player_cards_chosen])
        opponent_cards = np.concatenate(
            [self.opponent_table, self.opponent_cards_chosen])
        score = calc_score(opponent_cards, player_cards)
        self.opponent_score += score
        return score

    def get_scores(self):
        return self.score_player(), self.score_opponent()


def main():
    game = Game()
    print(game.getEnv())
    opponent, player = game.getEnv()
    print(opponent)
    print(player)

    opponent_play = np.concatenate(
        [opponent[1], np.random.choice(opponent[0], 3)])
    player_play = np.concatenate([player[1], np.random.choice(player[0], 3)])

    print(calc_score(player_play, opponent_play))
#    print(score_basic(player_play, opponent_play))
    # opponent, player =
    _ = game.shuffleDeck()  # .getEnv()
    print(opponent)
    print(player)


main()

if __name__ == "__main__":
    main()
