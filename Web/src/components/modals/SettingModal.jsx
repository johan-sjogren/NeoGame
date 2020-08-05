import Modal from "react-bootstrap/Modal";
import React, { useState, useEffect } from "react";
import axios from "axios";

function SettingModal(props) {
  const [opponents, setOpponents] = useState([]);
  const { setOpponent, dealCards } = props;
  const [changedOpp, setchangedOpp] = useState(false);
  const [footerText, setFooterText] = useState(
    "The random opponent picks cards completely random and uses no logic whatsoever."
  );
  useEffect(() => {
    axios
      .get(`http://${window.location.hostname}:5000/ai/game/v1.0`)
      .then((res) => {
        setOpponents(res.data.opponents);
        setOpponent(res.data.opponents[0]);
        dealCards();
      });
  }, [setOpponent]);

  return (
    <Modal
      size="lg"
      show={props.showSettings}
      onHide={() => {
        props.setShowSettings(false);
        if (changedOpp) {
          dealCards();
          props.setScore([0, 0]);
          setchangedOpp(false);
        }
        props.setShowSettings(false);
      }}
      aria-labelledby="example-modal-sizes-title-lg"
    >
      <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
          {"Settings"}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div>
          Choose an opponent
          <br />
          <select
            onChange={(event) => {
              props.setOpponent(event.target.value);
              setchangedOpp(true);

              setFooterText(
                event.target.value === "Random"
                  ? "The random opponent picks cards completely random and uses no logic whatsoever."
                  : event.target.value === "Greedy"
                  ? "The greedy opponent will always try to use the current state to beat you."
                  : event.target.value === "DeepQ"
                  ? "DeepQ uses reinforcement learning agent trained to beat the Greedy agent."
                  : ""
              );
            }}
            value={props.opponent}
          >
            {opponents.map((opponent) => {
              return (
                <option key={opponent} value={opponent}>
                  {opponent}
                </option>
              );
            })}
          </select>
        </div>
      </Modal.Body>
      <Modal.Footer>{footerText}</Modal.Footer>
    </Modal>
  );
}

export default SettingModal;
