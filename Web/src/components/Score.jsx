import React from "react";
import styles from "./score.module.css";
function Score(props) {
  return props.player ? (
    <>
      {"Player"}
      <div className={styles.board + " " + styles.player}>{props.score}</div>
    </>
  ) : (
    <>
      {"Opponent"}
      <div className={styles.board + " " + styles.opponent}>{props.score}</div>
    </>
  );
}
export default Score;
