import React, { useState, useEffect } from "react";
import axios from "axios";
import styles from "./settingsBox.module.css";
function SettingsBox(props) {
  const [opponents, setOpponents] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:5000/ai/game/v1.0`).then(res => {
      setOpponents(res.data.opponents);
    });
  }, []);

  return (
    <div className={styles.settingsBox}>
      <select
        style={{ width: "80px" }}
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
      <br />
      <button
        onClick={() => {
          props.dealCards();
        }}
      >
        Deal Cards
      </button>
      <button
        onClick={() => {
          props.playCards();
        }}
      >
        Play Cards
      </button>
      <br />
      <textarea
        readOnly
        style={{ resize: "none", height: "80px" }}
        value={props.message}
      ></textarea>
    </div>
  );
}
export default SettingsBox;
