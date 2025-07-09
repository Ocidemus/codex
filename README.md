# 🧠 Codex - AI-Powered Code Assistant

**Codex** is a web-based developer tool that combines code execution, comment generation, explanation, and visual flowcharting in a seamless AI-powered interface. Built using React, Flask, and Hugging Face Transformers, it enhances the coding experience with interactive features.

---

## 🚀 Features

- 🧠 **AI Chat Assistant**: Generate or explain code with natural language prompts via LLaMA 2 (`meta-llama/Llama-Vision-Free`) and Together API.
- 💬 **Comment Generator**: Automatically add meaningful comments using `phi-2` fine-tuned LLM.
- 🖼️ **Code Flowchart Visualizer**: Convert Python code into dynamic flowcharts using AST parsing and Graphviz.
- 💻 **Multi-language Code Runner**: Execute Python, C, C++, and JavaScript code securely in a sandboxed environment.
- 🎨 **Monaco Editor Integration**: Write and format code in a smooth, syntax-highlighted interface.
- 🐳 **Dockerized Backend**: One-command container deployment with support for model loading and local inference.

---

## ⚙️ Tech Stack

| Frontend          | Backend           | ML & NLP              | DevOps            |
|-------------------|-------------------|------------------------|-------------------|
| React + Vite      | Flask (Python)    | Hugging Face Transformers (`distilgpt2`, `phi-2`) | Docker            |
| Monaco Editor     | Together API      | Tokenization & CausalLM | ESLint + Vite     |
| Axios, FontAwesome| Flask-CORS        | Graphviz + AST         |                   |

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/codex.git
cd codex
```
