import Modal from "react-bootstrap/Modal";
import React from "react";

function HelpModal(props) {
  return (
    <>
      <Modal
        size="lg"
        aria-labelledby="example-modal-sizes-title-sm"
        show={props.showHelp}
        onHide={() => {
          props.setShowHelp(false);
        }}
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-modal-sizes-title-sm">
            {"Instructions"}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div>
            <span style={{ whiteSpace: "pre-wrap" }}>
              NeoGame is a 2 player card game, where one player takes the role
              of the development team and the other will play as the dreaded
              IT-project.{"\n"}
              {"\n"}The deck is shuffled for each round, then each player
              receives two cards lying face-up and a hand of five cards. The
              players selects two cards from their hand and places them on the
              table.
              {"\n"}
              {"\n"}The players score is calculated as follows: For each card,
              points are rewarded for everyone of the opponent's card that it
              beats. Cards beat each other according to a circle chain where
              level one cards (Bug/Product owner) beats level two cards (Scrum
              master/Specifications) and so on.
              <div
                style={{
                  content: `url(/cards/circle2.svg)`,
                  width: "80%",
                  position: "relative",
                  margin: "auto",
                  marginLeft: "auto",
                  marginRight: "auto",
                }}
              ></div>
            </span>
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}

export default HelpModal;
