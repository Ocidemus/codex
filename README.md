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
### 2. Setup Python Backend
   ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate
    pip install -r requirements.txt
```
## Add a .env file:

```env
TOGETHER_API_KEY=your_together_api_key
```
## Start the Flask server:
```bash
python app.py
```
### 3. Setup React Frontend
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

### 🐳 Run with Docker
## Build and run:

```bash
docker build -t codex-backend .
docker run -p 5000:5000 --env-file .env codex-backend
```
Ensure that models like distilgpt2 or phi-2 are downloaded and placed in the ./distilgpt2_local and ./phi_2_local directories.

### 🧠 Model Training
Training code is available in train_model.py:

Fine-tunes distilgpt2 on the code_search_net dataset for generating docstrings/code.
Saved at ./distilgpt2-comment-gen after training.

### 🛠 Requirements

Install with:

```bash
pip install -r requirements.txt
```

### 📜 License
MIT License.

### 🙌 Credits
Hugging Face Transformers

Together API

Graphviz

CodeSearchNet dataset

LLaMA community
