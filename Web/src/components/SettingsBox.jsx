import React, { useState, useEffect } from "react";
import axios from "axios";
import styles from "./settingsBox.module.css";
function SettingsBox(props) {
  return (
    <div className={styles.settingsBox}>
      <button
        className={styles.btn + " " + styles.stn}
        onClick={() => {
          props.playCards();
        }}
      >
        Play Cards
      </button>
    </div>
  );
}
export default SettingsBox;
