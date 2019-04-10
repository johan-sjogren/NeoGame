from random import shuffle, sample


def score_basic(player1, player2):
    score = 0
    for x in player1:
        for y in player2:
            if wins(x, y):
                score += 1
    return score


def wins(x, y, max=4, min=0):
    if x + 1 == y:
        return 1
    elif x == 4 and y == 0:
        return 1
    else:
        return 0


def score(player1, player2):
    return sum(wins(x, y) for x in player1 for y in player2)


class Game(object):

    deque = []
    for x in range(5):
        deque += [x]*5

    def __init__(self):
        self.shuffleDeck().dealCards()

    def shuffleDeck(self):
        shuffle(self.deque)
        return self

    def dealCards(self):
        self.opponent_table = self.deque[:2]
        self.opponent_hand = self.deque[2:7]
        self.player_table = self.deque[7:9]
        self.player_hand = self.deque[9:14]
        return self

    def getEnv(self):
        return (self.opponent_hand, self.opponent_table), (self.player_hand, self.player_table)


if __name__ == "__main__":
    game = Game()
    print(game.getEnv())
    opponent, player = game.getEnv()
    print(opponent)
    print(player)
    opponent_play = opponent[1] + sample(opponent[0], 3)
    player_play = player[1] + sample(player[0], 3)
    assert score(opponent_play, player_play) == score_basic(opponent_play, player_play)
    assert score(player_play, opponent_play) == score_basic(player_play, opponent_play)
    print(score(player_play, opponent_play))
    print(score_basic(player_play, opponent_play))
