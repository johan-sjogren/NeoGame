from random import shuffle
from itertools import permutations
from collections import deque
import numpy as np


class Game(object):

    def __init__(self,
                 n_classes=5,
                 card_per_class=5,
                 episodes=5,
                 memory_length=10000,
                 cards_in_hand=5,
                 cards_on_table=2,
                 cards_to_play=2):

        deck = []
        self.n_classes = n_classes
        for x in range(n_classes):
            deck += [x] * card_per_class
        self.deck = np.array(deck)
        self.player_score = deque(maxlen=memory_length)
        self.opponent_score = deque(maxlen=memory_length)
        self.n_cards_in_hand = cards_in_hand
        self.n_cards_to_play = cards_to_play
        self.n_cards_on_table = cards_on_table
        self.actions = None
        # Initial setup
        self.deal_cards()

    @staticmethod
    def calc_score(player1_final, player2_final):
        return sum(Game.wins(x, y)
                   for x in player1_final
                   for y in player2_final)

    @staticmethod
    def wins(x, y, max_cls=4, min_cls=0):
        if x + 1 == y:
            return 1
        elif x == max_cls and y == min_cls:
            return 1
        else:
            return 0

    def shuffle_deck(self):
        shuffle(self.deck)
        return self

    def deal_cards(self):
        """Randomly deal cards"""
        self.shuffle_deck()
        i = self.n_cards_on_table
        self.opponent_table = self.deck[:i].copy()
        j, i = i, i + self.n_cards_in_hand
        self.opponent_hand = self.deck[j:i].copy()
        j, i = i, i + self.n_cards_on_table
        self.player_table = self.deck[j:i].copy()
        j, i = i, i + self.n_cards_in_hand
        self.player_hand = self.deck[j:i].copy()
        return self

    def deal_from_recommendation(self, state):
        """ Deals cards according to agent recommendation.
        Arguments:
            state {[int]} -- Integer list describing the recommended state

        Returns:
            Game -- self
        """
        # First recreate the recommended state and assign to Game variables
        i = self.n_cards_in_hand
        self.player_hand = state[:i].copy()
        j, i = i, i + self.n_cards_on_table
        self.player_table = state[j:i].copy()
        j, i = i, i + self.n_cards_on_table
        self.opponent_table = state[j:i].copy()
        j, i = i, i + self.n_cards_in_hand

        # Use a temporary deck
        temp_deck = list(self.deck)
        # Remove all cards already used in the recommended state
        [temp_deck.remove(x) for x in state if x in temp_deck]
        # The randomly pick opponents hand
        shuffle(temp_deck)
        self.opponent_hand = np.array(temp_deck[j:i])
        return self

    def get_env(self):
        return ((self.opponent_hand, self.opponent_table),
                (self.player_hand, self.player_table))

    def get_actions(self):
        '''
        The actions are all possible ways that you can pick n_cards_to_play
        cards from hand. In this case represented by a boolean array for
        cards chosen
        '''

        if self.actions is None:
            n_ones = self.n_cards_to_play
            n_zeros = self.n_cards_in_hand-self.n_cards_to_play
            # Generate all permutations
            perms = permutations(n_ones*[1]+n_zeros * [0],
                                 self.n_cards_in_hand)
            # Remove duplicates
            perms = set(perms)
            # Convert to array
            self.actions = np.array(list(perms))
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
        self.player_action = action.astype(bool)
        return self

    def set_opponent_action(self, action):
        self.opponent_action = action.astype(bool)
        return self

    def get_scores(self):
        player_cards = np.concatenate(
            [self.player_table,
             self.player_hand[self.player_action]])
        opponent_cards = np.concatenate(
            [self.opponent_table,
             self.opponent_hand[self.opponent_action]])
        player_score = Game.calc_score(player_cards, opponent_cards)
        self.player_score.append(player_score)
        opp_score = Game.calc_score(opponent_cards, player_cards)
        self.opponent_score.append(opp_score)
        return player_score, opp_score

    def get_optimal_result(self):
        opponent_cards = np.concatenate(
            [self.opponent_table,
             self.opponent_hand[self.opponent_action]])
        possible_actions = self.get_actions()

        optimal_result = None
        for action in possible_actions:
            player_cards = np.concatenate(
                [self.player_table,
                self.player_hand[action.astype(bool)]])
            player_score = self.calc_score(player_cards, opponent_cards)
            opponent_score = self.calc_score(opponent_cards, player_cards)
            diff = player_score - opponent_score
            if optimal_result == None or diff >= optimal_result:
                optimal_result = diff
        return optimal_result

    def test_player(self, agent):
        """Routine to test agent behaviour
        Arguments:
            agent {BaseAgent} -- Agent class inheriting from BaseAgent
        """

        self.deal_cards()
        agent_action = agent.get_action(self.get_player_state(),
                                        actions=self.get_actions())

        # Check that action recieved is a numpy array
        assert isinstance(agent_action, np.ndarray)

        # Check that the player action produces the required number of cards
        # Also checks that action can be convertet to boolean array
        try:
            assert len(self.player_hand[agent_action.astype(
                bool)]) == self.n_cards_to_play
        except:
            print('Test failed for ', str(agent))
            print('Expected number of cards:', self.n_cards_to_play)
            print('Got: ', len(self.player_hand[agent_action]))


def test():
    """
    Checking basic functionality of the Game class
    """
    game = Game()
    print('Running Engine tests')

    # Make sure that deal_cards function actually randomizes
    for _ in range(10):
        setup_1, setup_2 = game.get_env(), game.deal_cards().get_env()
        com_arrs = [np.array_equal(a, b) for x, y in zip(
            setup_1, setup_2) for a, b in zip(x, y)]
        # There is a chance that arrays will be similar just by chance
        try:
            assert sum(com_arrs) < 3
        except AssertionError:
            print(com_arrs)
            print(setup_1)
            print(setup_2)

    # Test that the scoring function returns expected values
    assert game.calc_score([1, 1, 1, 1, 1], [2, 3, 4, 0, 0]) == 5
    assert game.calc_score([2, 3, 4, 0, 0], [1, 1, 1, 1, 1]) == 10
    assert Game.calc_score([2, 3, 4, 0, 0], [1, 1, 1, 1, 1]) == 10
    assert Game.calc_score([1, 1, 1, 1, 1], [2, 3, 4, 0, 0]) == 5

    # Check that scoring never exceeds the highest possible score
    for _ in range(500):
        arr1 = np.random.randint(0, 5, 4)
        arr2 = np.random.randint(0, 5, 4)
        try:
            max_score = (game.n_cards_on_table + game.n_cards_to_play)**2
            assert Game.calc_score(arr1, arr2) <= max_score
        except AssertionError:
            print(arr1)
            print(arr2)

    # Scoring should be insensitive to permutations
    for _ in range(4):
        arr1 = [1, 1, 4, 4, 2]
        shuffle(arr1)
        arr2 = [2, 3, 4, 0, 0]
        shuffle(arr2)
        assert Game.calc_score(arr1, arr2) == 7
        assert Game.calc_score(arr2, arr1) == 6

    # The list of actions should be equal for all game instances
    for _ in range(10):
        game1 = Game()
        game2 = Game()
        assert (game1.get_actions() == game2.get_actions()).all()

    print('Engine tests completed')


def main():
    test()


if __name__ == "__main__":
    main()
