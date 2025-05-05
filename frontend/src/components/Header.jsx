/* eslint-disable react/prop-types */
import style from "./header.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// eslint-disable-next-line no-unused-vars
import { faCode, faPlay } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";

const Header = ({
  language,
  setLanguage,
  code,
  setOutput,
  setLoading,
  loading,
}) => {
  const handleRunCode = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/run", {
        language,
        code,
      });
      setOutput(response.data.output);
    } catch (error) {
      setOutput("Error: " + error.message);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className={style.main}>
      <div className={style.logo}>
        <div className={style.logo_img}>
          <img src="/code-solid.svg" alt="Code icon" />
        </div>
        <div className={style.logo_text}>codex</div>
      </div>
      <div className={style.options}>
        <div>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            <option value="Python">Python</option>
            <option value="Javascript">JavaScript</option>
            <option value="C">C</option>
            <option value="cpp">C++</option>
          </select>
        </div>
        <div
          className={style.run}
          onClick={!loading ? handleRunCode : null}
          style={{
            pointerEvents: loading ? "none" : "auto",
            opacity: loading ? 0.5 : 1,
          }}
        >
          <span className={style.run_text}>{language}</span>{" "}
          <span className={style.run_icon}>
            <FontAwesomeIcon icon={faPlay} title="Execute" />
          </span>
        </div>
      </div>
    </div>
  );
};

export default Header;
