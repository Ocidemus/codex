/* eslint-disable react/prop-types */
import { useEffect } from "react";
import style from "./output.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faXmark } from "@fortawesome/free-solid-svg-icons";

const Terminal = ({ output, terminal, setTerminal}) => {
  useEffect(() => {
    if (!terminal) return;

    const resizer = document.querySelector("." + style.resizer);
    const container = document.querySelector("." + style.container);

    let isResizing = false;

    const handleMouseDown = () => {
      isResizing = true;
      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
    };

    const handleMouseMove = (e) => {
      if (!isResizing) return;
      const newHeight = window.innerHeight - e.clientY;
      container.style.height = `${newHeight}px`;
    };

    const handleMouseUp = () => {
      isResizing = false;
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };

    resizer.addEventListener("mousedown", handleMouseDown);

    return () => {
      resizer.removeEventListener("mousedown", handleMouseDown);
    };
  }, [terminal]);
  useEffect(() => {
    if (output) {
      setTerminal(true);
    }
  }, [output, setTerminal]);

  return (
    <>
      {terminal && (
        <div className={style.container}>
          <div className={style.resizer}></div>
          <div className={style.header}>
            <div className={style.exit} onClick={() => setTerminal(false)}>
              <FontAwesomeIcon icon={faXmark} />
            </div>
          </div>
          <pre className={style.output}>{">>"} {output}</pre>
        </div>
      )}
    </>
  );
};

export default Terminal;
