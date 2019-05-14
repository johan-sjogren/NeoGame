# %%
import numpy as np
from game_engine import Game
from tqdm import tqdm
from QAgent import QTableAgent

# %%
TRAIN_EPISODES = 1000000
TEST_EPISODES = 100000
game = Game()
player = QTableAgent(unexplored=4)
opponent = QTableAgent()

for i in tqdm(range(TRAIN_EPISODES)):
    game.dealCards().get_player_state()

    player_action = player.get_action(game.get_player_state(),
                                      game.get_actions(),
                                      explore_exploit='explore')

    opponent_action = opponent.get_action(game.get_opponent_state(),
                                          game.get_actions())

    player_score, opponent_score = (game.set_player_action(player_action)
                                    .set_opponent_action(opponent_action)

                                    .get_scores())
    player.learn(state=game.get_player_state(),
                 action=player_action,
                 reward=player_score-opponent_score)

print(player.get_QTable(as_dataframe=True))

saved_loaded = (player.save('test.csv')
                      .load('test.csv').get_QTable(as_dataframe=True)
                )
print(saved_loaded)
print(saved_loaded.columns)

player = QTableAgent().load('test.csv')
game = Game()
for _ in range(1):
    for i in tqdm(range(TEST_EPISODES)):
        game.dealCards().get_player_state()
        player_action = player.get_action(game.get_player_state(),
                                          game.get_actions(),
                                          explore_exploit='exploit')

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
