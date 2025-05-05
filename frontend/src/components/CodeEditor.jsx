/* eslint-disable react/prop-types */
import { Editor } from "@monaco-editor/react";
import style from "./editor.module.css";
import { useRef } from "react";

const CodeEditor = ({ code, setCode, language, setLineCount, setCurrentLine }) => {
  const editorRef = useRef(null);

  const handleEditorDidMount = (editor) => {
    editorRef.current = editor;
    setLineCount(editor.getModel().getLineCount());
    setCurrentLine(editor.getPosition().lineNumber);

    editor.onDidChangeModelContent(() => {
      setLineCount(editor.getModel().getLineCount());
    });

    editor.onDidChangeCursorPosition(() => {
      setCurrentLine(editor.getPosition().lineNumber);
    });
  };

  return (
    <div className={style.container}>
      <Editor
        height="95vh"
        className={style.editor}
        theme="vs-dark"
        language={language}
        value={code}
        onChange={(newValue) => setCode(newValue)}
        onMount={handleEditorDidMount}
      />
    </div>
  );
};

export default CodeEditor;
