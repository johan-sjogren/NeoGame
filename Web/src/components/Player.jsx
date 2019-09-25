import React from "react";
import styles from "./player.module.css";
function Player(props) {
  return (
    <div>
      <table className={styles.cardTable}>
        <tbody>
          <tr>
            {props.hand.map((card, idx) => {
              if (props.picks.includes(idx)) {
                return (
                  <td
                    key={idx}
                    className={styles.pickedCard}
                    onClick={() => {
                      props.unpickCard(card, idx);
                    }}
                  >
                    {card}
                  </td>
                );
              } else {
                return (
                  <td
                    key={idx}
                    className={styles.frontCard}
                    onClick={() => {
                      props.pickCard(card, idx);
                    }}
                  >
                    {card}
                  </td>
                );
              }
            })}
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Player;
