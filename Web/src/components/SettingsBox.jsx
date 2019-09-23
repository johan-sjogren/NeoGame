import React from "react";

function SettingsBox(props) {
  //TODO: Get opponent list from flask api
  return (
    <>
      <select
        onChange={event => {
          props.setOpponent(event.target.value);
        }}
      >
        <option value="Greedy">Greedy</option>
        <option value="Random">Random</option>
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
