import React from "react";
import styles from "./gameTable.module.css";
import { Droppable } from "react-beautiful-dnd";
import Card from "./Card";

function GameTable(props) {
  const renderOpponentCards = () => {
    let cards = props.opponentActionCards.map((card, idx) => {
      if (props.roundDone) {
        return (
          <Card
            front
            opponent
            key={idx}
            className={styles.opponent}
            cardId={card}
            setClick={props.setClick}
          ></Card>
        );
      } else if (idx < 2) {
        return (
          <Card
            front
            opponent
            key={idx}
            className={styles.opponent}
            cardId={card}
            setClick={props.setClick}
          ></Card>
        );
      } else {
        return <Card key={idx} className={styles.opponent}></Card>;
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
          front
          cardId={playerCards[0].value}
          setClick={props.setClick}
        ></Card>
        <Card
          front
          cardId={playerCards[1].value}
          setClick={props.setClick}
        ></Card>
        <Droppable droppableId="pickedCardFirst">
          {provided => (
            <div
              className={styles.frontCard + " " + styles.card}
              ref={provided.innerRef}
              {...provided.droppableProps}
            >
              {playerCards.length > 2 ? (
                <Card
                  key={playerCards[2].id}
                  draggable
                  front
                  dragId={playerCards[2].id}
                  cardId={playerCards[2].value}
                  setClick={props.setClick}
                ></Card>
              ) : (
                provided.placeholder
              )}
            </div>
          )}
        </Droppable>
        <Droppable droppableId="pickedCardSecond">
          {provided => (
            <div
              className={styles.frontCard + " " + styles.card}
              ref={provided.innerRef}
              {...provided.droppableProps}
            >
              {playerCards.length > 3 ? (
                <Card
                  key={playerCards[3].id}
                  draggable
                  front
                  dragId={playerCards[3].id}
                  cardId={playerCards[3].value}
                  setClick={props.setClick}
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
      <div className={styles.cardContainer}>
        <div className={styles.cardRow}>{renderOpponentCards()}</div>
        <div className={styles.cardRow}>{renderPlayerCards()}</div>
      </div>
    </div>
  );
}

export default GameTable;
