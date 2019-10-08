import React, { useState, useEffect } from "react";
import axios from "axios";
import styles from "./settingsBox.module.css";
import host from "../../../config.json";
function SettingsBox(props) {
  const [opponents, setOpponents] = useState([]);
  const { setOpponent } = props;
  useEffect(() => {
    axios.get(`http://${host}:${port}/ai/game/v1.0`).then(res => {
      setOpponents(res.data.opponents);
      setOpponent(res.data.opponents[0]);
    });
  }, [setOpponent]);

  return (
    <div className={styles.settingsBox}>
      <select
        className={styles.selectOpponent + " " + styles.stn}
        onChange={event => {
          props.setOpponent(event.target.value);
        }}
      >
        {opponents.map(opponent => {
          return (
            <option key={opponent} value={opponent}>
              {opponent}
            </option>
          );
        })}
      </select>
      <button
        className={styles.btn + " " + styles.stn}
        onClick={() => {
          props.dealCards();
        }}
      >
        Deal Cards
      </button>
      <button
        className={styles.btn + " " + styles.stn}
        onClick={() => {
          props.playCards();
        }}
      >
        Play Cards
      </button>
      <textarea
        readOnly
        className={styles.textBox + " " + styles.stn}
        value={props.message}
      ></textarea>
    </div>
  );
}
export default SettingsBox;
