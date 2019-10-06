import React from 'react';
import styles from './card.module.css';


const Card = (props) => {
  const pickCardHandler = (picked, id, idx) => {
    return picked ? props.unpickCard(id, idx) : props.pickCard(id, idx);
  }

  return (
    <div
      className={`${styles.card} ${props.picked ? styles.pickedCard : styles.frontCard}`}
      onClick={pickCardHandler.bind(this, props.picked, props.cardId, props.idx)}
    >
      {props.cardId}
    </div>
  )
}

export default Card;