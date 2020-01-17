import React from "react";
import styles from "./card.module.css";
import { Draggable } from "react-beautiful-dnd";

const Card = props => {
  const front_url = props.opponent
    ? `url(/cards/project_${props.cardId}.svg)`
    : `url(/cards/team_${props.cardId}.svg)`;

  return !props.front ? (
    <div
      class={props.sm ? styles.card + " " + styles.sm : styles.card}
      style={{
        backgroundImage: `url(/cards/mb_neocard_back_blue.svg)`
      }}
    ></div>
  ) : props.draggable ? (
    <Draggable draggableId={props.dragId} index={props.idx}>
      {provided => (
        <div
          class={props.sm ? styles.card + " " + styles.sm : styles.card}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          ref={provided.innerRef}
          style={{
            backgroundImage: front_url,
            ...provided.draggableProps.style
          }}
          onDoubleClick={() => {
            console.log("propsincard", props);
            props.setClick({ clicked: true, id: props.dragId, idx: props.idx });
          }}
        ></div>
      )}
    </Draggable>
  ) : (
    <div
      class={props.sm ? styles.card + " " + styles.sm : styles.card}
      style={{
        backgroundImage: front_url
      }}
    ></div>
  );
};

export default Card;
