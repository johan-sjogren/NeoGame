import React from "react";
import styles from "./gameTable.module.css";

function GameTable(props) {
  const renderOpponentCards = () => {
    let cards = props.table.opponent_cards.map((card, idx) => {
      if (props.roundDone) {
        return (
          <div
            key={idx}
            className={styles.frontCard + " " + styles.card}
            style={{
              backgroundImage: `url(/cards/project_${card}.svg)`
            }}
          ></div>
        );
      } else if (idx < 2) {
        return (
          <div
            key={idx}
            className={styles.frontCard + " " + styles.card}
            style={{
              backgroundImage: `url(/cards/project_${card}.svg)`
            }}
          ></div>
        );
      } else {
        return (
          <div key={idx} className={styles.backCard + " " + styles.card}></div>
        );
      }
    });
    return cards;
  };
  const renderPlayerCards = () => {
    let cards = props.table.player_cards.map((card, idx) => {
      return (
        <div
          key={idx}
          className={styles.frontCard + " " + styles.card}
          style={{
            backgroundImage: `url(/cards/team_${card}.svg)`
          }}
        ></div>
      );
    });

    while (cards.length < 4) {
      cards.push(<div className={styles.frontCard + " " + styles.card}></div>);
    }
    return cards;
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
