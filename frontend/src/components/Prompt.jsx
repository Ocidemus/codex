import React, { useState, useRef, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPaperPlane,
  faCopy,
  faPaperclip,
} from "@fortawesome/free-solid-svg-icons";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { tomorrow } from "react-syntax-highlighter/dist/esm/styles/prism";
import axios from "axios";
import PropTypes from "prop-types";
import { unified } from "unified";
import remarkParse from "remark-parse";
import style from "./prompt.module.css";

const Prompt = ({
  showBot,
  chatHistory,
  setChatHistory,
  outputState,
  setOutputState,
}) => {
  const [inputValue, setInputValue] = useState("");
  const [copiedCodeIndex, setCopiedCodeIndex] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  const handleCopy = (text, idx) => {
    navigator.clipboard.writeText(text);
    setCopiedCodeIndex(idx);
    setTimeout(() => setCopiedCodeIndex(null), 1000);
  };

  const handleSend = async () => {
    if (!inputValue.trim() || outputState) return;
    setOutputState(true);
    try {
      const { data } = await axios.post("http://localhost:5000/generate", {
        prompt: inputValue,
      });
      setChatHistory((prev) => [
        ...prev,
        { prompt: inputValue, response: data.response },
      ]);
    } catch (err) {
      console.error(err);
    }
    setInputValue("");
    setOutputState(false);
  };

  // Recursively render MDAST nodes
  const renderNode = (node, i) => {
    switch (node.type) {
      case "root":
        return node.children.map(renderNode);

      case "heading": {
        const Tag = `h${node.depth}`;
        return (
          <Tag key={i} className={style.output_heading}>
            {node.children.map(renderNode)}
          </Tag>
        );
      }

      case "paragraph":
        return (
          <p key={i} className={style.paragraph}>
            {node.children.map(renderNode)}
          </p>
        );

      case "list":
        return (
          <ul key={i} className={style.list}>
            {node.children.map(renderNode)}
          </ul>
        );

      case "listItem":
        return (
          <li key={i} className={style.list_item}>
            {node.children.map(renderNode)}
          </li>
        );

      case "code":
        return (
          <div className={style.output_box} key={i}>
            <div className={style.code_header}>
              <div
                className={style.copy}
                onClick={() => handleCopy(node.value, i)}
                style={{
                  pointerEvents: copiedCodeIndex === i ? "none" : "auto",
                  opacity: copiedCodeIndex === i ? 0.5 : 1,
                }}
              >
                <FontAwesomeIcon icon={faCopy} className={style.icon} />
                {copiedCodeIndex === i ? "Copied" : "Copy"}
              </div>
            </div>
            <div className={style.text}>
              <SyntaxHighlighter
                language={node.lang || "plaintext"}
                style={tomorrow}
                customStyle={{
                  background: "#2d2d2d",
                  borderRadius: "8px",
                  fontSize: "14px",
                  whiteSpace: "pre-wrap",
                  wordBreak: "break-word",
                }}
                wrapLongLines
              >
                {node.value}
              </SyntaxHighlighter>
            </div>
          </div>
        );

      case "text":
        return <span key={i}>{node.value}</span>;

      case "strong":
        return <strong key={i}>{node.children.map(renderNode)}</strong>;

      case "emphasis":
        return <em key={i}>{node.children.map(renderNode)}</em>;

      case "inlineCode":
        return (
          <code key={i} className={style.inline_code}>
            {node.value}
          </code>
        );

      case "blockquote":
        return <blockquote key={i}>{node.children.map(renderNode)}</blockquote>;

      case "thematicBreak":
        return <hr key={i} className={style.hr} />;

      case "image":
        // Markdown image syntax ![alt](url)
        return (
          <img
            key={i}
            src={node.url}
            alt={node.alt || ""}
            className={style.image}
          />
        );

      default:
        return null;
    }
  };

  // Parse markdown to MDAST
  const parseMarkdownToTree = (md) => unified().use(remarkParse).parse(md);

  if (!showBot) return null;
  return (
    <div className={`${style.prompt_dialog_box} ${style.show}`}>
      <div className={style.output}>
        {chatHistory.map((chat, idx) => (
          <React.Fragment key={idx}>
            <div className={style.prompt}>{chat.prompt}</div>
            <div className={style.response}>
              {renderNode(parseMarkdownToTree(chat.response))}
            </div>
          </React.Fragment>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className={style.prompt_container}>
        <div className={style.prompt_send}>
          <FontAwesomeIcon icon={faPaperclip} />
        </div>
        <textarea
          className={style.prompt_box}
          rows={3}
          placeholder="Ask Anything..."
          value={inputValue}
          disabled={outputState}
          onChange={(e) => !outputState && setInputValue(e.target.value)}
          onKeyDown={(e) => {
            if (!outputState && e.key === "Enter") handleSend();
          }}
        />
        <div
          className={style.prompt_send}
          onClick={handleSend}
          style={{
            pointerEvents: outputState ? "none" : "auto",
            opacity: outputState ? 0.5 : 1,
          }}
        >
          <FontAwesomeIcon icon={faPaperPlane} />
        </div>
      </div>
    </div>
  );
};

Prompt.propTypes = {
  showBot: PropTypes.bool.isRequired,
  chatHistory: PropTypes.array.isRequired,
  setChatHistory: PropTypes.func.isRequired,
  outputState: PropTypes.bool.isRequired,
  setOutputState: PropTypes.func.isRequired,
};

export default Prompt;
