import React, { useState, useEffect } from "react";
import styles from "./score.module.css";
function Score({ setScore, score, player, width }) {
  let style = width < 700 ? styles.board2 : styles.board;
  //let text = props.width < 700 ? "absolute" : "static";
  const [easterClick, setEasterClick] = useState(0);
  useEffect(() => {
    if (easterClick === 15) {
      setEasterClick(0);
      alert("Well done!");
      setScore((score) => {
        const newScores = [...score];
        newScores[0] += 10;
        return newScores;
      });
    }
  }, [easterClick, setScore]);
  return player ? (
    <div className={style + " " + styles.player}>{score}</div>
  ) : (
    <div
      onClick={() => setEasterClick((v) => v + 1)}
      className={style + " " + styles.opponent}
    >
      {score}
    </div>
  );
}
export default Score;
