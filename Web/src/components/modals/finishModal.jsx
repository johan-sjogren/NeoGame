import Modal from "react-bootstrap/Modal";
import React from "react";
import Card from "../Card";

function FinishModal(props) {
  const playerHand = Object.values(props.playerHand).map(object => {
    return object.value;
  });

  const playerActionCards = Object.values(props.playerActionCards).map(
    object => {
      return object.value;
    }
  );
  return (
    <>
      <Modal
        size="lg"
        show={props.finishShow}
        onHide={() => {
          props.setFinishShow(false);
          props.dealCards();
          props.setRoundDone(false);
        }}
        aria-labelledby="example-modal-sizes-title-sm"
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-modal-sizes-title-sm">
            {"Round Finished"}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className={"cardsContainer"} style={{ float: "left" }}>
            <div
              className={"CardRow"}
              style={{ display: "flex", width: "100%" }}
            >
              {props.opponentHand.map(value => {
                return <Card sm front opponent cardId={value}></Card>;
              })}
            </div>
            <br />
            <div
              className={"CardRow"}
              style={{ display: "flex", width: "100%" }}
            >
              {props.opponentActionCards.map(value => {
                return <Card sm front opponent cardId={value}></Card>;
              })}
              {props.oPoints + " points"}
            </div>
            <div
              className={"CardRow"}
              style={{ display: "flex", width: "100%" }}
            >
              {playerActionCards.map(value => {
                return <Card sm front cardId={value}></Card>;
              })}
              {props.pPoints + " points"}
            </div>
            <br />
            <div
              className={"CardRow"}
              style={{ display: "flex", width: "100%" }}
            >
              {playerHand.map(value => {
                return <Card sm front cardId={value}></Card>;
              })}
            </div>
          </div>
          <div style={{ float: "right" }}>
            Some text...Some text... Some text...Some text...Some text...Some
            text...Some text...Some text...Some text...Some text...Some
            text...Some text...Some text...Some text...Some text...Some
            text...Some text...Some text...
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}

export default FinishModal;
