
# %%
import numpy as numpy
from game_engine import Game
from QAgent import QAgent

# %%
game = Game()
player = QTableAgent()
opponent = QTableAgent()

game.get_actions_string()
# %%
# %%
game.get_player_state_string()
game.shuffleDeck().dealCards().get_player_state_string()

# %%
player_action = player.get_action(
    game.get_player_state_string(), game.get_actions_string())
opponent_action = opponent.get_action(
    game.get_opponent_state_string(), game.get_actions_string())
print("Action taken " + player_action[0])
print("Action taken " + opponent_action[0])

player_score, opponent_score = (game.player_action([int(x) for x in player_action[0]])
                                    .opponent_action([int(x) for x in opponent_action[0]])
                                    .get_scores())

print(player_score, opponent_score)
# %%

# %%
numpy.random.choice(game.get_actions_string(), 2)

# %%
