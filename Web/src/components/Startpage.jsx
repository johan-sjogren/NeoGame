import React, { useState } from "react";
import Card from "./Card";
import CardRbs from "react-bootstrap/Card";
import Popover from "react-bootstrap/Popover";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import logo from "../neodevlogo.png";
import meeting from "../meeting_01.svg";
import Carousel from "react-bootstrap/Carousel";
import styles from "./Startpage.module.css";
import clsx from "clsx";

const opponentCards = [
  { idx: 0, title: "Bugs", desc: "This is a bug" },
  { idx: 1, title: "Requirements", desc: "" },
  { idx: 2, title: "Process", desc: "" },
  { idx: 3, title: "Design", desc: "" },
  { idx: 4, title: "Code", desc: "" },
];

const playerCards = [
  { idx: 0, title: "Product Owner", desc: "" },
  { idx: 1, title: "Scrum Master", desc: "" },
  { idx: 2, title: "Architect", desc: "" },
  { idx: 3, title: "Developer", desc: "" },
  { idx: 4, title: "Tester", desc: "" },
];

const Startpage = ({ setGameStarted }) => {
  const [index, setIndex] = useState(0);

  const handleSelect = (selectedIndex, e) => {
    setIndex(selectedIndex);
  };

  return (
    <div className="StartpageBckg">
      <div style={{ flex: "0 1 auto" }}>
        <img className={styles.logo} src={logo} alt="Neodev" />
      </div>

      <Carousel
        style={{ flex: "1 1 auto" }}
        activeIndex={index}
        onSelect={handleSelect}
        interval={false}
      >
        <Carousel.Item id="test" style={{ height: "100%" }}>
          <CardRbs className={clsx(styles.frontCardRbs, "text-center")}>
            <CardRbs.Body>
              <CardRbs.Title>The game</CardRbs.Title>
              <CardRbs.Text>
                NeoGame is a web based 2 player card game, where one player
                takes the role of the development team and the other will play
                as the dreaded IT-project.
              </CardRbs.Text>
              <img src={meeting} style={{ width: "27rem" }} alt="meeting"></img>
              <div
                className={styles.startButton}
                onClick={() => setGameStarted(true)}
              >
                Start
              </div>
            </CardRbs.Body>
          </CardRbs>
        </Carousel.Item>
        <Carousel.Item>
          <CardRbs className="text-center" style={{ height: "700px" }}>
            <CardRbs.Body>
              <CardRbs.Title>The project</CardRbs.Title>
              <CardRbs.Text>Subtext</CardRbs.Text>
              <div className={styles.cardHold}>
                {opponentCards.map((card, idx) => {
                  return (
                    <OverlayTrigger
                      key={idx}
                      delay={{ show: 125, hide: 125 }}
                      placement="bottom"
                      overlay={
                        <Popover id="popover-basic">
                          <Popover.Title as="h3">{card.title}</Popover.Title>
                          <Popover.Content>{card.desc}</Popover.Content>
                        </Popover>
                      }
                    >
                      <div>
                        <Card front opponent cardId={card.idx} />
                      </div>
                    </OverlayTrigger>
                  );
                })}
              </div>
              <div
                className={styles.startButton}
                onClick={() => setGameStarted(true)}
              >
                Start
              </div>
            </CardRbs.Body>
          </CardRbs>
        </Carousel.Item>
        <Carousel.Item>
          <CardRbs className="text-center" style={{ height: "700px" }}>
            <CardRbs.Body>
              <CardRbs.Title>The team</CardRbs.Title>
              <CardRbs.Text>Subtext</CardRbs.Text>
              <div className={styles.cardHold}>
                {playerCards.map((card, idx) => {
                  return (
                    <OverlayTrigger
                      key={idx}
                      delay={{ show: 125, hide: 125 }}
                      placement="bottom"
                      overlay={
                        <Popover id="popover-basic">
                          <Popover.Title as="h3">{card.title}</Popover.Title>
                          <Popover.Content>{card.desc}</Popover.Content>
                        </Popover>
                      }
                    >
                      <div>
                        <Card front cardId={card.idx} />
                      </div>
                    </OverlayTrigger>
                  );
                })}
              </div>
              <div
                className={styles.startButton}
                onClick={() => setGameStarted(true)}
              >
                Start
              </div>
            </CardRbs.Body>
          </CardRbs>
        </Carousel.Item>
      </Carousel>
    </div>
  );
};

export default Startpage;
