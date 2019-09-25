import React from "react";
import styles from "./gameTable.module.css";

function GameTable(props) {
  return (
    <div className={styles.theTable}>
      <table className={styles.cardTable}>
        <tbody>
          <tr>
            {props.table.opponent_cards.map((card, idx) => {
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
                return (
                  <td id="card" key={idx} className={styles.backCard}></td>
                );
              }
            })}
          </tr>
          <tr>
            {props.table.player_cards.map((card, idx) => {
              return (
                <td id="card" key={idx} className={styles.frontCard}>
                  {card}
                </td>
              );
            })}

            {() => {
              while (props.table.player_cards.length() < 4) return <td />;
            }}
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default GameTable;
