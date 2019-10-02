import React from "react";
import styles from "./player.module.css";
function Player(props) {
  const renderCards = () => {
    let cards = props.hand.map((card, idx) => {
      if (props.picks.includes(idx)) {
        return (
          <div
            key={idx}
            className={styles.pickedCard + " " + styles.card}
            onClick={() => {
              props.unpickCard(card, idx);
            }}
          >
            {card}
          </div>
        );
      } else {
        return (
          <div
            key={idx}
            className={styles.frontCard + " " + styles.card}
            onClick={() => {
              props.pickCard(card, idx);
            }}
          >
            {card}
          </div>
        );
      }
    });
    return cards;
  };

  return <div className={styles.playerContainer}>{renderCards()}</div>;
}

export default Player;
