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
            {"The game"}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>{"Write text here"}</Modal.Body>
      </Modal>
    </>
  );
}

export default HelpModal;
