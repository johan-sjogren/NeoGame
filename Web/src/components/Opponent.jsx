import React from "react";
import styles from "./opponent.module.css";
function Opponent(props) {
  const renderCards = () => {
    let cards = props.hand.map((card, idx) => {
      if (props.roundDone) {
        return (
          <div
            key={idx}
            className={
              styles.opponent + " " + styles.frontCard + " " + styles.card
            }
            style={{
              backgroundImage: `url(/cards/project_${card}.svg)`
            }}
          ></div>
        );
      } else {
        return (
          <div
            key={idx}
            className={
              styles.opponent + " " + styles.backCard + " " + styles.card
            }
          ></div>
        );
      }
    });
    return cards;
  };

  return <div className={styles.opponentContainer}>{renderCards()}</div>;
}
export default Opponent;
