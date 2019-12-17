import React, { useState } from "react";
import GameTable from "./GameTable";
import axios from "axios";
import styles from "./gameController.module.css";
import Player from "./Player";
import Score from "./Score";
import MessageModal from "./modals/MessageModal";
import SettingModal from "./modals/SettingModal";
import FinishModal from "./modals/finishModal";
import { DragDropContext } from "react-beautiful-dnd";

function GameController(props) {
  const [opponent, setOpponent] = useState("Greedy");
  const [opponentHand, setOpponentHand] = useState([0, 0, 0, 0, 0]);
  const [opponentActionCards, setOpponentActionCards] = useState([0, 0, 0, 0]);

  const [playerHand, setPlayerHand] = useState({
    card_2: { id: "card_2", value: 0 },
    card_3: { id: "card_3", value: 0 },
    card_4: { id: "card_4", value: 0 },
    card_5: { id: "card_5", value: 0 },
    card_6: { id: "card_6", value: 0 }
  });
  const [playerActionCards, setPlayerActionCards] = useState([
    { id: "card_0", value: 0 },
    { id: "card_1", value: 0 }
  ]);
  const [handOrder, setHandOrder] = useState([
    "card_2",
    "card_3",
    "card_4",
    "card_5",
    "card_6"
  ]);

  const [score, setScore] = useState([0, 0]);
  const [oPoints, setOPoints] = useState(0);
  const [pPoints, setPPoints] = useState(0);

  const [message, setMessage] = useState("");
  const [messageTitle, setMessageTitle] = useState("");
  const [showSettings, setShowSettings] = useState(true);
  const [smShow, setSmShow] = useState(false);
  const [lgShow, setLgShow] = useState(false);
  const [finishShow, setFinishShow] = useState(false);
  const [roundDone, setRoundDone] = useState(false);

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
        const opponent_hand = Array.from(res.data.opponent_hand);
        opponent_hand.splice(opponent_action[0], 1);
        opponent_hand.splice(opponent_action[1] - 1, 1);

        opponentCards.push(res.data.opponent_hand[opponent_action[0]]);
        opponentCards.push(res.data.opponent_hand[opponent_action[1]]);

        const playerCards = res.data.player_table;
        setHandOrder(["card_2", "card_3", "card_4", "card_5", "card_6"]);
        setOpponent(res.data.opponent_name);
        setOpponentHand(opponent_hand);
        setOpponentActionCards(opponentCards);
        setPlayerHand({
          card_2: { id: "card_2", value: res.data.player_hand[0] },
          card_3: { id: "card_3", value: res.data.player_hand[1] },
          card_4: { id: "card_4", value: res.data.player_hand[2] },
          card_5: { id: "card_5", value: res.data.player_hand[3] },
          card_6: { id: "card_6", value: res.data.player_hand[4] }
        });
        setPlayerActionCards([
          { id: "card_0", value: playerCards[0] },
          { id: "card_1", value: playerCards[1] }
        ]);
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
    //convert playercards card values to array, ugly solution but good enough for now
    const playerCards = Object.values(playerActionCards).map(object => {
      return object.value;
    });
    const opponentCards = opponentActionCards;

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
    setPPoints(ppoints);
    setOPoints(opoints);
    if (ppoints > opoints) {
      console.log(
        "\nThe player won with " + ppoints + " points against " + opoints + "!"
      );
      const new_score = [...score];
      new_score[0] += 1;
      setScore(new_score);
    } else if (ppoints === opoints) {
      console.log("\nRound is Draw!");
    } else {
      const new_score = [...score];
      new_score[1] += 1;
      setScore(new_score);
      console.log(
        "\nThe opponent won with " +
          opoints +
          " points against " +
          ppoints +
          "!"
      );
    }
    setRoundDone(true);
    setFinishShow(true);
  };

  const playCards = () => {
    //Plays a round if two cards are given by the player.
    if (playerActionCards.length === 4) {
      getWinner();
    }
  };

  const pickCard = (card_id, index, box) => {
    const action_idx = box === "pickedCardFirst" ? 2 : 3;
    // Picks a card from the player hand
    const newCardOrder = Array.from(handOrder);
    newCardOrder.splice(index, 1);
    setHandOrder(newCardOrder);

    const newPlayerActionCards = [...playerActionCards];
    newPlayerActionCards.splice(action_idx, 0, { ...playerHand[card_id] });
    setPlayerActionCards(newPlayerActionCards);

    const newPlayerHand = { ...playerHand };
    delete newPlayerHand[card_id];
    setPlayerHand(newPlayerHand);
  };
  const unpickCard = (card_id, index, box) => {
    const action_idx = box === "pickedCardFirst" ? 2 : 3;

    // Picks a card from the player hand
    const newCardOrder = Array.from(handOrder);
    newCardOrder.splice(index, 0, card_id);
    setHandOrder(newCardOrder);

    const newPlayerHand = { ...playerHand };
    newPlayerHand[playerActionCards[action_idx].id] = {
      ...playerActionCards[action_idx]
    };
    setPlayerHand(newPlayerHand);

    const newPlayerActionCards = [...playerActionCards];
    newPlayerActionCards.splice(action_idx, 1);
    setPlayerActionCards(newPlayerActionCards);
  };
  const replaceCard = (card_h, index, box) => {
    const action_idx = box === "pickedCardFirst" ? 2 : 3;

    //Hand order
    const newHandOrder = Array.from(handOrder);
    newHandOrder.splice(index, 1, playerActionCards[action_idx].id); //From cardOrder, remove chosen card, and add the card from the droppableId box.
    setHandOrder(newHandOrder);

    //Player action cards
    const newPlayerActionCards = [...playerActionCards];
    newPlayerActionCards.splice(action_idx, 1);
    newPlayerActionCards.splice(action_idx, 0, { ...playerHand[card_h] });
    setPlayerActionCards(newPlayerActionCards);

    //Player hand
    const newPlayerHand = { ...playerHand }; // We need to modify the player hand to add the unpicked card
    newPlayerHand[playerActionCards[action_idx].id] = {
      ...playerActionCards[action_idx]
    };
    delete newPlayerHand[card_h];
    setPlayerHand(newPlayerHand);
  };

  const onDragEnd = result => {
    console.log(result);
    const { destination, source, draggableId } = result;
    if (!destination) {
      return;
    }
    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) {
      return;
    }

    if (
      source.droppableId === "playerCards" &&
      destination.droppableId === "pickedCardFirst"
    ) {
      if (playerActionCards.length <= 4) {
        //if not a card has been picked to this slot, add the card
        if (playerActionCards.length === 2) {
          pickCard(draggableId, source.index);
        } else {
          replaceCard(draggableId, source.index, destination.droppableId);
        }
      }
      return;
    }
    if (
      source.droppableId === "playerCards" &&
      destination.droppableId === "pickedCardSecond"
    ) {
      if (playerActionCards.length < 4) {
        pickCard(draggableId, source.index, destination.droppableId);
      } else {
        replaceCard(draggableId, source.index, destination.droppableId);
      }
      return;
    }
    if (
      source.droppableId === "pickedCardFirst" &&
      destination.droppableId === "playerCards"
    ) {
      unpickCard(draggableId, destination.index, source.droppableId);
      return;
    }
    if (
      source.droppableId === "pickedCardSecond" &&
      destination.droppableId === "playerCards"
    ) {
      unpickCard(draggableId, destination.index, source.droppableId);
      return;
    }

    if (
      source.droppableId === "playerCards" &&
      destination.droppableId === "playerCards"
    ) {
      const newCardOrder = Array.from(handOrder);
      const [removed] = newCardOrder.splice(source.index, 1);
      newCardOrder.splice(destination.index, 0, removed);
      setHandOrder(newCardOrder);
    }
  };

  return (
    <>
      {console.log("render")}
      <div>
        <SettingModal
          dealCards={getTable}
          showSettings={showSettings}
          setShowSettings={setShowSettings}
          setOpponent={setOpponent}
        ></SettingModal>
        <MessageModal
          title={messageTitle}
          message={message}
          smShow={smShow}
          setSmShow={setSmShow}
          lgShow={lgShow}
          setLgShow={setLgShow}
        ></MessageModal>
        <FinishModal
          dealCards={getTable}
          setFinishShow={setFinishShow}
          finishShow={finishShow}
          opponentHand={opponentHand}
          opponentActionCards={opponentActionCards}
          playerActionCards={playerActionCards}
          playerHand={playerHand}
          oPoints={oPoints}
          pPoints={pPoints}
          setRoundDone={setRoundDone}
        ></FinishModal>

        <DragDropContext onDragEnd={onDragEnd.bind(this)}>
          <div className={styles.row}>
            <div className={styles.scores}>
              <Score score={score[1]} player={false}></Score>
              <Score score={score[0]} player={true}></Score>
            </div>

            <GameTable
              setOpponent={setOpponent}
              playerActionCards={playerActionCards}
              opponentActionCards={opponentActionCards}
              message={message}
              roundDone={roundDone}
              playCards={playCards}
            ></GameTable>
            <button
              onClick={() => {
                playCards();
              }}
              className={styles.playButton}
            >
              Play
            </button>
          </div>

          <Player hand={playerHand} handOrder={handOrder}></Player>
        </DragDropContext>
      </div>
    </>
  );
}
export default GameController;
