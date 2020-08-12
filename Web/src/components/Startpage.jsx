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
  {
    idx: 0,
    title: "Bugs",
    desc:
      "A software bug is an error, flaw or fault in a computer program or system that causes it to produce an incorrect or unexpected result, or to behave in unintended ways",
  },
  {
    idx: 1,
    title: "Requirements",
    desc:
      "Software requirements describes the features and functionalities of the system. Requirements adheres to the expectations of the client.",
  },
  {
    idx: 2,
    title: "Process",
    desc:
      "A software process is a set of related activities that leads to the production of the software. These activities may involve the development of the software from the scratch, or, modifying an existing system.",
  },
  {
    idx: 3,
    title: "Design",
    desc:
      "Design is the process of visual communication and problem-solving through the use of typography, photography, iconography and illustration.",
  },
  {
    idx: 4,
    title: "Code",
    desc:
      "Code is most often human-readable instructions of text which is inputed to the machine to execute some actions.",
  },
];

const playerCards = [
  {
    idx: 0,
    title: "Product Owner",
    desc:
      "The Product Owner serves as the bridge between the customer and the team to ensure that the requirements are met.",
  },
  {
    idx: 1,
    title: "Scrum Master",
    desc:
      "Works as a coach for the team. Ensures compliance with the process, synchronizes between actors and removes obstacles for the developer group. Is not a direct leadership role.",
  },
  {
    idx: 2,
    title: "Architect",
    desc:
      "A systems architect models the architecture of a system in order to fulfill the requirements. Defining the architecture could mean breaking down the system into smaller parts and deciding on the technologies to be used.",
  },
  {
    idx: 3,
    title: "Developer",
    desc:
      "A developer writes computer code to implement the features of the system.",
  },
  {
    idx: 4,
    title: "Tester",
    desc:
      "Testers focus is to ensure good quality around the software system. They could conduct manual or automated tests to make sure that everything works smoothly and fits the purposed requirements. They are experienced in finding bugs and try to make sure that they are gone before deployment.",
  },
];

const Startpage = ({ setGameStarted }) => {
  const [index, setIndex] = useState(0);

  const handleSelect = (selectedIndex, e) => {
    setIndex(selectedIndex);
  };

  return (
    <div className={styles.StartpageBckg}>
      <div style={{ flex: "0 1 auto" }}>
        <img className={styles.logo} src={logo} alt="Neodev" />
      </div>

      <Carousel
        style={{ flex: "1 1 auto" }}
        controls={false}
        activeIndex={index}
        onSelect={handleSelect}
        interval={false}
      >
        <Carousel.Item className={clsx(styles.frontCardRbs, "text-center")}>
          <CardRbs.Body>
            <CardRbs.Title>The game</CardRbs.Title>
            <CardRbs.Text style={{ margin: "1rem 3rem" }}>
              NeoGame is a web based card game, where you take the role of the
              development team and the computer opponent will play as the
              dreaded IT-project. Your job is to throw in the right team members
              to overcome the different project obstacles.
            </CardRbs.Text>
            <img src={meeting} style={{ width: "27rem" }} alt="meeting"></img>
          </CardRbs.Body>
        </Carousel.Item>
        <Carousel.Item className={clsx(styles.contentCardRbs, "text-center")}>
          <CardRbs.Body>
            <CardRbs.Title>The project</CardRbs.Title>
            <CardRbs.Text style={{ margin: "2rem 3rem" }}>
              A Software Project is the process of gathering requirements,
              modeling, implementing, maintenance and testing using well known
              methodologies to eventually end up with a product or a service.
            </CardRbs.Text>
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
          </CardRbs.Body>
        </Carousel.Item>
        <Carousel.Item className={clsx(styles.contentCardRbs, "text-center")}>
          <CardRbs.Body>
            <CardRbs.Title>The team</CardRbs.Title>
            <CardRbs.Text style={{ margin: "2rem 3rem" }}>
              A software team is a group of people who develop or maintain
              computer software. They are commonly divided into the following
              roles.
            </CardRbs.Text>
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
          </CardRbs.Body>
        </Carousel.Item>
      </Carousel>
      <div className={styles.startPageControl}>
        <div
          className={styles.carouselControlPrevIcon}
          onClick={() => setIndex((i) => (i == 0 ? 2 : i - 1))}
        />
        <div
          className={styles.startButton}
          onClick={() => setGameStarted(true)}
        >
          Start
        </div>
        <div
          className={styles.carouselControlNextIcon}
          onClick={() => setIndex((i) => (i == 2 ? 0 : i + 1))}
        />
      </div>
    </div>
  );
};

export default Startpage;
