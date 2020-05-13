import React from "react";
import styles from "./gameTable.module.css";
import Score from "./Score";
import { Droppable } from "react-beautiful-dnd";
import Card from "./Card";

function GameTable(props) {
  const renderOpponentCards = () => {
    let cards = props.opponentActionCards.map((card, idx) => {
      if (props.roundDone) {
        return (
          <Card
            hand={false}
            front
            opponent
            key={idx}
            idx={idx}
            className={styles.opponent}
            cardId={card}
            unpickCard={props.unpickCard}
          ></Card>
        );
      } else if (idx < 2) {
        return (
          <Card
            hand={false}
            front
            opponent
            key={idx}
            idx={idx}
            className={styles.opponent}
            cardId={card}
            unpickCard={props.unpickCard}
          ></Card>
        );
      } else {
        return (
          <Card
            hand={false}
            key={idx}
            idx={idx}
            className={styles.opponent}
            unpickCard={props.unpickCard}
          ></Card>
        );
      }
    });
    return cards;
  };
  const renderPlayerCards = () => {
    let playerCards = props.playerActionCards;
    //console.log(Object.values(playerCards)[2]);

    return playerCards.length !== 0 ? (
      <>
        <Card
          hand={false}
          front
          cardId={playerCards[0].value}
          unpickCard={props.unpickCard}
          playerActionCards={props.playerActionCards}
        ></Card>
        <Card
          hand={false}
          front
          cardId={playerCards[1].value}
          unpickCard={props.unpickCard}
          playerActionCards={props.playerActionCards}
        ></Card>
        <Droppable droppableId="pickedCardFirst">
          {(provided) => (
            <div
              className={styles.frontCard + " " + styles.card}
              ref={provided.innerRef}
              {...provided.droppableProps}
            >
              {playerCards.length > 2 ? (
                <Card
                  hand={false}
                  key={playerCards[2].id}
                  draggable
                  front
                  dragId={playerCards[2].id}
                  cardId={playerCards[2].value}
                  idx={0}
                  unpickCard={props.unpickCard}
                  playerActionCards={props.playerActionCards}
                ></Card>
              ) : (
                provided.placeholder
              )}
            </div>
          )}
        </Droppable>
        <Droppable droppableId="pickedCardSecond">
          {(provided) => (
            <div
              className={styles.frontCard + " " + styles.card}
              ref={provided.innerRef}
              {...provided.droppableProps}
            >
              {playerCards.length > 3 ? (
                <Card
                  hand={false}
                  key={playerCards[3].id}
                  draggable
                  front
                  dragId={playerCards[3].id}
                  cardId={playerCards[3].value}
                  idx={1}
                  unpickCard={props.unpickCard}
                  playerActionCards={props.playerActionCards}
                ></Card>
              ) : (
                provided.placeholder
              )}
            </div>
          )}
        </Droppable>
      </>
    ) : null;
  };
  return (
    <div className={styles.theTable}>
      {props.screenWidth < 700 && (
        <div className={styles.scores}>
          <Score
            setScore={props.setScore}
            score={props.score[1]}
            player={false}
            width={props.screenWidth}
          ></Score>
          <Score
            score={props.score[0]}
            player={true}
            width={props.screenWidth}
          ></Score>
        </div>
      )}
      <div className={styles.cardContainer}>
        <div className={styles.cardRow}>{renderOpponentCards()}</div>
        <div className={styles.cardRow}>{renderPlayerCards()}</div>
      </div>
      {props.screenWidth < 700 && (
        <button
          className={styles.playButton2}
          onClick={() => props.playCards()}
        >
          Play cards
        </button>
      )}
    </div>
  );
}

export default GameTable;
