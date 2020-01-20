import Modal from "react-bootstrap/Modal";
import React from "react";

function MessageModal(props) {
  return (
    <>
      <Modal
        size="sm"
        show={props.smShow}
        onHide={() => {
          props.setSmShow(false);
          props.dealCards();
        }}
        aria-labelledby="example-modal-sizes-title-sm"
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-modal-sizes-title-sm">
            {props.title}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body> {props.message}</Modal.Body>
      </Modal>

      <Modal
        size="lg"
        show={props.lgShow}
        onHide={() => {
          props.setLgShow(false);
          props.dealCards();
        }}
        aria-labelledby="example-modal-sizes-title-lg"
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-modal-sizes-title-lg">
            {props.title}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body> {props.message}</Modal.Body>
      </Modal>
    </>
  );
}

export default MessageModal;
