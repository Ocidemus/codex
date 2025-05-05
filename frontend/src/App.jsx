import { useState } from "react";

import CodeEditor from "./components/CodeEditor";
import Header from "./components/Header";
import Terminal from "./components/Terminal";
import Footer from "./components/Footer";
import Prompt from "./components/Prompt";
import Bot from "./components/Bot";
import "./main.css";

function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("Python");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [terminal, setTerminal] = useState(false);
  const [lineCount, setLineCount] = useState(0);
  const [currentLine, setCurrentLine] = useState(0);
  const [showBot, setShowBot] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [outputState, setOutputState] = useState(false);
  const [imagePath, setImagePath] = useState("");
  // const handleExplain = async () => {
  //   const response = await axios.post("http://localhost:5000/analyze", {
  //     code,
  //   });
  //   setExplanation(response.data.message);
  // };

  return (
    <div>
      <Header
        language={language}
        setLanguage={setLanguage}
        code={code}
        setOutput={setOutput}
        setLoading={setLoading}
        loading={loading}
      />
      <CodeEditor
        code={code}
        setCode={setCode}
        language={language}
        loading={loading}
        setLineCount={setLineCount}
        setCurrentLine={setCurrentLine}
      />
      <Terminal output={output} terminal={terminal} setTerminal={setTerminal}/>
      <Prompt
        showBot={showBot}
        chatHistory={chatHistory}
        setChatHistory={setChatHistory}
        outputState={outputState}
        setOutputState={setOutputState}
        imagePath={imagePath}
      />
      <Bot showBot={showBot} setShowBot={setShowBot} />
      <Footer
        terminal={terminal}
        setTerminal={setTerminal}
        lineCount={lineCount}
        currentLine={currentLine}
        code={code}
        setCode={setCode}
        setChatHistory={setChatHistory}
        setShowBot={setShowBot}
        setOutputState={setOutputState}
        setImagePath={setImagePath}
        outputState={outputState}
      />
    </div>
  );
}

export default App;
