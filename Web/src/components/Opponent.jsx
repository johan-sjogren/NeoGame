import React from "react";
import styles from "./opponent.module.css";
function Opponent(props) {
  return (
    <div className={styles.theTable}>
      <table className={styles.cardTable}>
        <tbody>
          <tr>
            {props.hand.map((card, idx) => {
              if (props.roundDone) {
                return (
                  <td key={idx} id="card" className={styles.frontCard}>
                    {card}
                  </td>
                );
              } else {
                return (
                  <td key={idx} id="card" className={styles.backCard}></td>
                );
              }
            })}
          </tr>
        </tbody>
      </table>
    </div>
  );
}
export default Opponent;
