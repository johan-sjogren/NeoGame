import React from "react";
import styles from "./score.module.css";
function Score(props) {
  return props.player ? (
    <>
      <div style={{ color: "white" }}>Player</div>
      <div className={styles.board + " " + styles.player}>{props.score}</div>
    </>
  ) : (
    <>
      <div style={{ color: "white" }}>Opponent</div>
      <div className={styles.board + " " + styles.opponent}>{props.score}</div>
    </>
  );
}
export default Score;
