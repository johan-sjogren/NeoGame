import React from "react";

function Opponent(props) {
  return (
    <>
      <table>
        <tbody>
          <tr>
            {props.hand.map((card, idx) => {
              if (props.roundDone) {
                return (
                  <td key={idx} className="frontCard">
                    {card}
                  </td>
                );
              } else {
                return (
                  <td key={idx} className="backCard">
                    x
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

export default Opponent;
