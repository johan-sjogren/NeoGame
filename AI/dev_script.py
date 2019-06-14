# %%
import numpy as np
from pyneogame.Engine import Game
from tqdm import tqdm
from pyneogame.Agent.QTableAgent import QTableAgent
from pyneogame.Agent.GreedyAgent import GreedyAgent
from pyneogame.Agent.ActiveTable import ActiveTable

# %%
game = Game()
player = GreedyAgent(value_func=Game.calc_score)
player = ActiveTable()
nn = QTableAgent()

game.get_actions()

# %%
game.get_player_state()
game.dealCards().get_player_state()

# %%
player_action = player.get_action(game.get_player_state(),
                                  game.get_actions()
                                  )
print(player_action)
# opponent_action = nn.get_action(game.get_nn_state(),
#                                       game.get_actions())
# print(nn_action)


TEST_EPISODES = 1000

for _ in range(1):
    # for i in tqdm(range(TEST_EPISODES)):
    for i in range(TEST_EPISODES):
        game.dealCards()
        player_action = player.get_action(game.get_player_state(),
                                          game.get_actions(),
                                          )

        opponent_action = opponent.get_action(game.get_opponent_state(),
                                              game.get_actions())

        player_score, opponent_score = (game.set_player_action(player_action)
                                        .set_opponent_action(opponent_action)
                                        .get_scores())

        player.learn(state=game.get_player_state(),
                     action=player_action,
                     reward=player_score-opponent_score)

print(list(zip(game.opponent_score[-10:], game.player_score[-10:])))

# %%
player_wins = sum(
    list(play > opp for opp, play in
         zip(game.opponent_score[-TEST_EPISODES:],
             game.player_score[-TEST_EPISODES:])
         ))

opponent_wins = sum(
    list(play < opp for opp, play in
         zip(game.opponent_score[-TEST_EPISODES:],
             game.player_score[-TEST_EPISODES:])
         ))

print(player_wins)
print(opponent_wins)


print(game.dealCards().getEnv())
if isinstance(player, ActiveTable):
    print('Recommended state')
    state = player.recommend_state()
    print(state)
    print(game.dealFromRecommendation(state).getEnv())

print(game.get_actions())
