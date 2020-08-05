import React, { useState } from "react";
import "./App.css";
import GameController from "./components/GameController";
import "bootstrap/dist/css/bootstrap.min.css";
import Startpage from "./components/Startpage";

function App() {
  const [gameStarted, setGameStarted] = useState(false);
  return (
    <div className="App" style={{ height: "100%" }}>
      {!gameStarted ? (
        <Startpage setGameStarted={setGameStarted} />
      ) : (
        <GameController />
      )}
    </div>
  );
}

export default App;
