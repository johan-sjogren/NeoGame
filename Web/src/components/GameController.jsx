import React, { useState } from "react";
import GameTable from "./GameTable";
import axios from "axios";
import SettingsBox from "./SettingsBox";
import styles from "./gameController.module.css";
import Opponent from "./Opponent";
import Player from "./Player";
import Score from "./Score";

function GameController(props) {
  const [table, setTable] = useState({
    opponent_name: "No opponent",
    opponent_cards: [0, 0, 0, 0],
    player_cards: [0, 0, 0, 0],
    player_hand: [0, 0, 0, 0, 0],
    opponent_hand: [0, 0, 0, 0, 0],
    version: 0.0
  });
  const [opponent, setOpponent] = useState("Greedy");
  const [score, setScore] = useState([0, 0]);
  const [message, setMessage] = useState(
    "Press 'Deal Cards' to start a new round."
  );
  const [roundDone, setRoundDone] = useState(false);
  const [idxPicks, setIdxPicks] = useState([]);

  const getTable = () => {
    axios
      .post(
        `http://${window.location.hostname}:${window.location.port}/ai/game/v1.0`,
        {
          opponent_name: opponent
        }
      )
      .then(res => {
        const opponent_action = actionBoolToIndex(res.data.opponent_action);
        const opponentCards = res.data.opponent_table;
        opponentCards.push(res.data.opponent_hand[opponent_action[0]]);
        opponentCards.push(res.data.opponent_hand[opponent_action[1]]);
        const playerCards = res.data.player_table;

        setTable({
          opponent_name: res.data.opponent_name,
          opponent_cards: opponentCards,
          player_cards: playerCards,
          player_hand: res.data.player_hand,
          opponent_hand: res.data.opponent_hand,
          version: res.data.version
        });
        setRoundDone(false);
        setMessage("Pick two cards and press play!");
        const picks = [];
        setIdxPicks(picks);
      });
  };

  const actionBoolToIndex = action => {
    // Maps the boolean opponent action outputted from the model to normal indices
    let idxAction = [];
    action.forEach((val, idx) => {
      if (val) idxAction.push(idx);
    });
    return idxAction;
  };

  const cardWins = (x, y, max_cls = 4, min_cls = 0) => {
    // Returns true if x wins over y
    if (x === max_cls && y === min_cls) {
      return true;
    } else if (x + 1 === y) {
      return true;
    } else {
      return false;
    }
  };

  const getWinner = () => {
    //Retrieves the winner based on the current state
    const playerCards = table.player_cards;
    const opponentCards = table.opponent_cards;
    let ppoints = 0;
    let opoints = 0;

    for (let i = 0; i < 5; i++) {
      for (let j = 0; j < 5; j++) {
        if (cardWins(playerCards[i], opponentCards[j])) {
          ppoints += 1;
        }
        if (cardWins(opponentCards[i], playerCards[j])) {
          opoints += 1;
        }
      }
    }

    let winText = "";
    if (ppoints > opoints) {
      winText +=
        "\nPlayer Wins with " + ppoints + " points against " + opoints + "!";
      const new_score = [...score];
      new_score[0] += 1;
      setScore(new_score);
    } else if (ppoints === opoints) {
      winText += "\nRound is Draw!";
    } else {
      const new_score = [...score];
      new_score[1] += 1;
      setScore(new_score);
      winText +=
        "\nOpponent Wins with " + opoints + " points against " + ppoints + "!";
    }
    winText += "  -- Press 'Deal Cards' to start a new round.";
    setRoundDone(true);
    setMessage(winText);
  };

  const playCards = () => {
    //Plays a round if two cards are given by the player.
    if (idxPicks.length === 2) {
      getWinner();
      const picks = [];
      setIdxPicks(picks);
    } else {
      setMessage("Please pick two cards!");
    }
  };

  const pickCard = (card, idx) => {
    // Picks a card from the player hand
    if (table.player_cards.length < 4) {
      const newTable = { ...table };

      newTable.player_cards.push(card);
      setTable(newTable);

      const picks = [...idxPicks];
      picks.push(idx);
      setIdxPicks(picks);
    }
  };

  const unpickCard = (card, idx) => {
    //Unpicks a card
    const newTable = { ...table };

    const idxToRemove = newTable.player_cards.lastIndexOf(card);
    if (idxToRemove !== -1) newTable.player_cards.splice(idxToRemove, 1);
    setTable(newTable);

    const picks = [...idxPicks];
    const pickToRemove = picks.lastIndexOf(idx);
    if (pickToRemove !== -1) picks.splice(pickToRemove, 1);
    setIdxPicks(picks);
  };

  return (
    <>
      <div>
        <Opponent
          hand={table.opponent_hand}
          roundDone={roundDone}
          message={message}
        ></Opponent>
        <div className={styles.row}>
          <Score score={score[0]} player={true}></Score>
          <GameTable
            setOpponent={setOpponent}
            table={table}
            message={message}
            roundDone={roundDone}
          />
          <Score score={score[1]} player={false}></Score>
        </div>
        <Player
          dealCards={getTable}
          playCards={playCards}
          hand={table.player_hand}
          pickCard={pickCard}
          unpickCard={unpickCard}
          picks={idxPicks}
        ></Player>
        <SettingsBox
          setOpponent={setOpponent}
          dealCards={getTable}
          playCards={playCards}
          message={message}
        ></SettingsBox>
      </div>
    </>
  );
}
export default GameController;
