import Modal from "react-bootstrap/Modal";
import React from "react";
import Card from "../Card";

function FinishModal(props) {
  const playerHand = Object.values(props.playerHand).map((object) => {
    return object.value;
  });

  const getCardPoints = (card, opponentCards) => {
    let points = 0;
    opponentCards.forEach((oCard) => {
      if (props.cardWins(card, oCard)) {
        points += 1;
      }
    });
    return points;
  };

  const playerActionCards = Object.values(props.playerActionCards).map(
    (object) => {
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
            {"Summary "}
          </Modal.Title>
        </Modal.Header>
        <Modal.Header>
          {props.pPoints > props.oPoints
            ? `Nicely done! You beat the opponent with ${props.pPoints} points against their ${props.oPoints}.`
            : props.pPoints === props.oPoints
            ? `You both got ${props.oPoints} points resulting in a tie. Keep going!`
            : `Opponent won with ${props.oPoints} against your ${props.pPoints}, try harder!`}
        </Modal.Header>
        <Modal.Body>
          <div
            className={"cardsContainer"}
            style={{ float: "left", width: "100%" }}
          >
            <div
              className={"CardRow"}
              style={{
                textAlign: "center",
                fontWeight: 600,
                display: "flex",
                width: "100%",
                justifyContent: "center",
              }}
            >
              {props.opponentHand.map((value, idx) => {
                return <Card sm front opponent cardId={value} key={idx}></Card>;
              })}
            </div>
            <br />
            <div
              className={"CardRow"}
              style={{
                textAlign: "center",
                fontWeight: 600,
                display: "flex",
                width: "100%",
                justifyContent: "center",
              }}
            >
              {props.opponentActionCards.map((value, idx) => {
                return (
                  <div>
                    {getCardPoints(
                      value,
                      props.playerActionCards.map((c) => c.value)
                    ) + " pts"}
                    <Card sm front opponent cardId={value} key={idx}></Card>
                  </div>
                );
              })}
              <div
                style={{ position: "absolute", left: "350px", top: "210px" }}
              ></div>
            </div>
            <div
              className={"CardRow"}
              style={{
                textAlign: "center",
                fontWeight: 600,
                display: "flex",
                width: "100%",
                justifyContent: "center",
              }}
            >
              {playerActionCards.map((value, idx) => {
                return (
                  <div>
                    {getCardPoints(value, props.opponentActionCards) + " pts"}
                    <Card sm front cardId={value} key={idx}></Card>
                  </div>
                );
              })}
              <div
                style={{ position: "absolute", left: "350px", top: "320px" }}
              ></div>
            </div>
            <br />
            <div
              className={"CardRow"}
              style={{
                textAlign: "center",
                fontWeight: 600,
                display: "flex",
                width: "100%",
                justifyContent: "center",
              }}
            >
              {playerHand.map((value, idx) => {
                return <Card sm front cardId={value} key={idx}></Card>;
              })}
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer style={{ justifyContent: "flex-start" }}>
          Tip: Try to think two steps ahead if you play against a greedy AI.{" "}
          {/* Generate random tip here */}
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default FinishModal;
