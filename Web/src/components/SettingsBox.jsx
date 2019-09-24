import React, { useState, useEffect } from "react";
import axios from "axios";

function SettingsBox(props) {
  const [opponents, setOpponents] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:5000/ai/game/v1.0`).then(res => {
      setOpponents(res.data.opponents);
    });
  }, []);

  return (
    <>
      <select
        onChange={event => {
          props.setOpponent(event.target.value);
        }}
      >
        {opponents.map(opponent => {
          return <option value={opponent}>{opponent}</option>;
        })}
      </select>
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
      <button
        onClick={() => {
          props.undoPick();
        }}
      >
        Undo Pick
      </button>
      <br />
      <textarea
        readOnly
        style={{ resize: "none", height: "80px" }}
        value={props.message}
      ></textarea>
    </>
  );
}

export default SettingsBox;
