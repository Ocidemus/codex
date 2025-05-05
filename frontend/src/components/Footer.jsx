/* eslint-disable react/prop-types */
import style from "./footer.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCode } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";

const Footer = ({
  terminal,
  setTerminal,
  lineCount,
  currentLine,
  code,
  setChatHistory,
  setShowBot,
  setOutputState,
  setImagePath,
  outputState,
  setCode,
}) => {
  const analyzeCode = async () => {
    setShowBot(true);
    setOutputState(true);
    const res = await axios.post("http://localhost:5000/analyze", {
      code: code,
    });
    const path = res.data.path;
    setImagePath(path);
    setChatHistory((prev) => [
      ...prev,
      {
        prompt: "Analyze Code",
        response: `![Flowchart](${path})`,
      },
    ]);
    setOutputState(false);
  };

  const explainCode = async () => {
    setShowBot(true);
    setOutputState(true);
    const response = await axios.post("http://localhost:5000/explain", {
      code: code,
    });
    setChatHistory((prev) => [
      ...prev,
      { prompt: "Explain Code", response: response.data.response },
    ]);
    setOutputState(false);
  };
  const commentCode = async () => {
    setOutputState(true);
    const response = await axios.post("http://localhost:5000/comment", {
      code: code,
    });
    setCode(response.data.response);
    setOutputState(false);
  };

  return (
    <div className={style.container}>
      <ul className={style.options}>
        <li>
          <FontAwesomeIcon icon={faCode} />
        </li>
        <li
          onClick={() => setTerminal(!terminal)}
          className={terminal ? style.color : null}
        >
          Terminal
        </li>
        <li>
          Line: {currentLine} / {lineCount}
        </li>
        <li
          onClick={analyzeCode}
          style={{
            pointerEvents: outputState ? "none" : "auto",
            opacity: outputState ? 0.5 : 1,
          }}
        >
          Analyze
        </li>
        <li
          onClick={explainCode}
          style={{
            pointerEvents: outputState ? "none" : "auto",
            opacity: outputState ? 0.5 : 1,
          }}
        >
          Explain
        </li>
        <li
          style={{
            pointerEvents: outputState ? "none" : "auto",
            opacity: outputState ? 0.5 : 1,
          }}
          onClick={()=> commentCode()}
        >
          Comment
        </li>
        <li
          style={{
            pointerEvents: outputState ? "none" : "auto",
            opacity: outputState ? 0.5 : 1,
          }}
        >
          Report
        </li>
      </ul>
    </div>
  );
};

export default Footer;
