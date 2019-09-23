import React from "react";
import "./GameTable.css";

function GameTable(props) {
  return (
    <div>
      <table>
        <tbody>
          <tr>
            {props.table.opponent_cards.map((card, idx) => {
              if (props.roundDone) {
                return (
                  <td key={idx} className="frontCard">
                    {card}
                  </td>
                );
              } else if (idx < 2) {
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
          <tr>
            {props.table.player_cards.map((card, idx) => {
              return (
                <td key={idx} className="frontCard">
                  {card}
                </td>
              );
            })}
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default GameTable;
