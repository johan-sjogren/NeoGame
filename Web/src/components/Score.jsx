import React, { useState, useEffect } from "react";
import styles from "./score.module.css";
function Score(props) {
  let style = props.width < 700 ? styles.board2 : styles.board;
  let text = props.width < 700 ? "absolute" : "static";
  const [easterClick, setEasterClick] = useState(0);
  useEffect(() => {
    if (easterClick === 15) {
      setEasterClick(0);
      alert("Well done!");
      props.setScore((score) => {
        const newScores = [...score];
        newScores[0] += 10;
        return newScores;
      });
    }
  }, [easterClick]);
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
      <div
        onClick={() => setEasterClick((v) => v + 1)}
        className={style + " " + styles.opponent}
      >
        {props.score}
      </div>
    </>
  );
}
export default Score;
