import React, { useState, useEffect } from "react";
import styles from "./card.module.css";
import { Draggable } from "react-beautiful-dnd";
import clsx from "clsx";
const Card = (props) => {
  const [surprised, setSurprised] = useState(false);
  const happy = props.isDragging && props.isDragging.id === props.dragId;

  useEffect(() => {
    if (happy) {
      setSurprised(false);
    }
  }, [happy]);
  const front_url = props.opponent
    ? `/cards/project_${props.cardId}.svg`
    : surprised
    ? `/cards/team_surprised_${props.cardId}.svg`
    : happy
    ? `/cards/team_happy_${props.cardId}.svg`
    : `/cards/team_${props.cardId}.svg`;

  return !props.front ? (
    <img
      className={props.sm ? clsx(styles.card, styles.sm) : styles.card}
      src={"/cards/mb_neocard_back_blue.svg"}
      alt=""
    />
  ) : props.draggable ? (
    <Draggable draggableId={props.dragId} index={props.idx}>
      {(provided) => (
        <div
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          ref={provided.innerRef}
          style={{
            ...provided.draggableProps.style,
          }}
        >
          <img
            className={props.sm ? clsx(styles.card, styles.sm) : styles.card}
            alt="Neogame back card"
            onMouseDown={() => setSurprised(true)}
            onDragStart={() => setSurprised(true)}
            onDragExit={() => setSurprised(false)}
            onDragLeave={() => setSurprised(false)}
            onDragOver={() => setSurprised(false)}
            onMouseUp={() => setSurprised(false)}
            src={front_url}
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
          />
        </div>
      )}
    </Draggable>
  ) : (
    <img
      className={props.sm ? clsx(styles.card, styles.sm) : styles.card}
      src={front_url}
      alt="Neogame Card"
    />
  );
};

export default Card;
