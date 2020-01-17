import React from "react";
import styles from "./card.module.css";
import { Draggable } from "react-beautiful-dnd";

const Card = props => {
  const front_url = props.opponent
    ? `url(/cards/project_${props.cardId}.svg)`
    : `url(/cards/team_${props.cardId}.svg)`;

  return !props.front ? (
    <div
      className={props.sm ? styles.card + " " + styles.sm : styles.card}
      style={{
        backgroundImage: `url(/cards/mb_neocard_back_blue.svg)`
      }}
    ></div>
  ) : props.draggable ? (
    <Draggable draggableId={props.dragId} index={props.idx}>
      {provided => (
        <div
          className={props.sm ? styles.card + " " + styles.sm : styles.card}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          ref={provided.innerRef}
          style={{
            backgroundImage: front_url,
            ...provided.draggableProps.style
          }}
          onDoubleClick={() => {
            props.hand
              ? props.playerActionCards.length < 4 &&
                props.pickCard(props.dragId, props.idx)
              : props.unpickCard(
                  props.dragId,
                  6,
                  props.playerActionCards[2] &&
                    props.playerActionCards[2].id === props.dragId
                    ? "pickedCardFirst"
                    : "pickedCardSec"
                );
          }}
        ></div>
      )}
    </Draggable>
  ) : (
    <div
      className={props.sm ? styles.card + " " + styles.sm : styles.card}
      style={{
        backgroundImage: front_url
      }}
    ></div>
  );
};

export default Card;
