import React from "react";
import styles from "./player.module.css";
import Card from './Card';
function Player(props) {

return(
  <div className={styles.playerContainer}>
    <div className={styles.playerCards}>
      {props.hand.map((id, idx) =>
        <Card
          key={idx}
          cardId={id}
          idx={idx}
          pickCard={props.pickCard}
          unpickCard={props.unpickCard}
          picked = {props.picks.includes(idx)}
        />
      )}
    </div>
  </div>
  );
}

export default Player;
