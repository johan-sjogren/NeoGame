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
            class={styles.playerCards}
            ref={provided.innerRef}
            {...provided.droppableProps}
          >
            {props.handOrder.map((card, idx) =>
              props.hand[card] !== undefined ? (
                <Card
                  front
                  draggable
                  key={props.hand[card]["id"]}
                  dragId={props.hand[card]["id"]}
                  cardId={props.hand[card]["value"]}
                  idx={idx}
                />
              ) : (
                <Card></Card>
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
