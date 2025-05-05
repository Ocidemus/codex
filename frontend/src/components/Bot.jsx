/* eslint-disable react/prop-types */
import style from "./bot.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRobot } from "@fortawesome/free-solid-svg-icons";

const Bot = ({ showBot, setShowBot }) => {
  const buttonStyle = showBot ? { right: "52%" } : { right: "2%" };

  return (
    <div
      className={style.button}
      onClick={() => setShowBot(!showBot)}
      style={buttonStyle}
    >
      <FontAwesomeIcon icon={faRobot} className={style.icon} />
    </div>
  );
};

export default Bot;
