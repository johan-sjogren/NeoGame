import React from "react";
import styles from "./gameTable.module.css";

function GameTable(props) {
  const renderOpponentCards = () => {
    let cards = props.table.opponent_cards.map((card, idx) => {
      if (props.roundDone) {
        return (
          <td id="card" key={idx} className={styles.frontCard}>
            {card}
          </td>
        );
      } else if (idx < 2) {
        return (
          <td id="card" key={idx} className={styles.frontCard}>
            {card}
          </td>
        );
      } else {
        return <td id="card" key={idx} className={styles.backCard}></td>;
      }
    });
    return cards;
  };
  const renderPlayerCards = () => {
    let cards = props.table.player_cards.map((card, idx) => {
      return (
        <td id="card" key={idx} className={styles.frontCard}>
          {card}
        </td>
      );
    });

    while (cards < 4) {
      cards.push(<td></td>);
    }
    return cards;
  };
  return (
    <div className={styles.theTable}>
      <table className={styles.cardTable}>
        <tbody>
          <tr>{renderOpponentCards()}</tr>
          <tr>{renderPlayerCards()}</tr>
        </tbody>
      </table>
    </div>
  );
}

export default GameTable;
