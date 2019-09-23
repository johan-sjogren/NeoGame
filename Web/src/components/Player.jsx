import React, { useState } from "react";

function Player(props) {
  return (
    <>
      <table>
        <tbody>
          <tr>
            {props.hand.map((card, idx) => {
              if (props.picks.includes(idx)) {
                return (
                  <td key={idx} className="pickedCard">
                    {card}
                  </td>
                );
              } else {
                return (
                  <td
                    key={idx}
                    className="frontCard"
                    onClick={() => {
                      props.pickCard(card, idx);
                    }}
                  >
                    {card}
                  </td>
                );
              }
            })}
          </tr>
        </tbody>
      </table>
    </>
  );
}

export default Player;
