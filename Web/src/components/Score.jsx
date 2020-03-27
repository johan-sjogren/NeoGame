import React from "react";
import styles from "./score.module.css";
function Score(props) {
  let style = props.width < 700 ? styles.board2 : styles.board;
  let text = props.width < 700 ? "absolute" : "static";
  return props.player ? (
    <>
      <div style={{ color: "white", position: text, top: "5px", left: "35%" }}>
        Player
      </div>
      <div className={style + " " + styles.player}>{props.score}</div>
    </>
  ) : (
    <>
      <div style={{ color: "white", position: text, top: "5px", left: "55%" }}>
        Opponent
      </div>
      <div className={style + " " + styles.opponent}>{props.score}</div>
    </>
  );
}
export default Score;
