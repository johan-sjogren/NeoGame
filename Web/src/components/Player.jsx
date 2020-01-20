import React from "react";
import styles from "./player.module.css";
import Card from "./Card";
import { Droppable } from "react-beautiful-dnd";

function Player(props) {
  return (
    <div className={styles.playerContainer}>
      <Droppable droppableId="playerCards" direction="horizontal">
        {provided => (
          <div
            className={styles.playerCards}
            ref={provided.innerRef}
            {...provided.droppableProps}
          >
            {props.handOrder.map((card, idx) =>
              props.hand[card] !== undefined ? (
                <Card
                  hand={true}
                  front
                  draggable
                  key={props.hand[card]["id"]}
                  dragId={props.hand[card]["id"]}
                  cardId={props.hand[card]["value"]}
                  idx={idx}
                  pickCard={props.pickCard}
                  playerActionCards={props.playerActionCards}
                />
              ) : (
                <Card
                  pickCard={props.pickCard}
                  playerActionCards={props.playerActionCards}
                ></Card>
              )
            )}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </div>
  );
}

export default Player;
