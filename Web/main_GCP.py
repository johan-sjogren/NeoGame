from itertools import permutations
from flask import escape, jsonify
import numpy as np
import random
from itertools import permutations


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
        random.shuffle(self.deque)
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


class RandomAgent(object):

    def get_action(self, state, actions, as_string=False):
        return random.choice(actions)


class GreedyAgent(object):
    
    def __init__(self, value_func=Game.calc_score):
        self.value_func = value_func

    def get_action(self, state, actions, as_string=False):
        player_hand = np.array(state[:5])
        opponent_table = np.array(state[-2:])

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
            return ''.join([str(x) for x in action])
        else:
            return action
        return 0


def NeoGameGCP(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object. 
    Returns:
        jsonifyed dict: 
            'agent_used': Which agent was used for selecting computer action
            'computer action': Which cards, as a binary mask, was chosen
            'opponent_hand': Cards in opponents/computers hand
            'opponent_table': Cards already on the table for the opponent
            'player_hand': Cards in players hand
            'player_table': Cards already on the table for the player
    """

    request_json = request.get_json(silent=True)
    # request_args = request.args

    return_dict = {}

    game = Game()
    actions = game.get_actions()
    agent = RandomAgent()

    if request_json and 'model' in request_json:
        if str(request_json['model']).lower() == 'greedy':
            return_dict['agent_used'] = 'Greedy'
            agent = GreedyAgent()
        else:
            return_dict['agent_used'] = 'Random'
            agent = RandomAgent()
    else:
        return_dict['agent_used'] = 'Random'
        agent = RandomAgent()
       
        
    return_dict['computer_action'] = agent.get_action(
                                                game.get_opponent_state(),
                                                actions).tolist()
                                         
    return_dict['player_hand'] = game.player_hand.tolist()
    return_dict['player_table'] = game.player_table.tolist()
    return_dict['opponent_hand'] = game.opponent_hand.tolist()
    return_dict['opponent_table'] = game.opponent_table.tolist()

    return jsonify(return_dict)
