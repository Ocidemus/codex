#  Codex - AI-Powered Code Assistant

**Codex** is a web-based developer tool that combines code execution, comment generation, explanation, and visual flowcharting in a seamless AI-powered interface. Built using React, Flask, and Hugging Face Transformers, it enhances the coding experience with interactive features.

---

##  Features

-  **AI Chat Assistant**: Generate or explain code with natural language prompts via LLaMA 2 (`meta-llama/Llama-Vision-Free`) and Together API.
-  **Comment Generator**: Automatically add meaningful comments using `phi-2` fine-tuned LLM.
-  **Code Flowchart Visualizer**: Convert Python code into dynamic flowcharts using AST parsing and Graphviz.
-  **Multi-language Code Runner**: Execute Python, C, C++, and JavaScript code securely in a sandboxed environment.
-  **Monaco Editor Integration**: Write and format code in a smooth, syntax-highlighted interface.
-  **Dockerized Backend**: One-command container deployment with support for model loading and local inference.

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
### Backend Setup

1. Create and activate a Python virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows use 'env\Scripts\activate'
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables:

- Add your API keys (e.g., TOGETHER_API_KEY) in a .env file.

4. Run the Flask backend:

```bash
python app.py
```

---

### Frontend Setup

1. Navigate to the frontend folder (if applicable):

```bash
cd frontend
```

2. Install Node dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

4. Open your browser to http://localhost:5173 (or the port specified).
## 🐳 Run with Docker
### Build and run:

```bash
docker build -t codex-backend .
docker run -p 5000:5000 --env-file .env codex-backend
```
Ensure that models like distilgpt2 or phi-2 are downloaded and placed in the ./distilgpt2_local and ./phi_2_local directories.

## 🧠 Model Training
Training code is available in train_model.py:

- Fine-tunes distilgpt2 on the code_search_net dataset for generating docstrings/code.

- Saved at ./distilgpt2-comment-gen after training.
  
  ---
  
Project Structure

- backend/: Python Flask server handling code execution and AI API integration  
- frontend/: React app with components:
  - App.jsx: Main app state and layout  
  - CodeEditor.jsx: Code editing UI with syntax highlighting  
  - Terminal.jsx: Output console for execution results  
  - Prompt.jsx & Bot.jsx: AI chat assistant UI  
  - Header.jsx, Footer.jsx: Navigation and status display  
- eslint.config.js: ESLint configuration for React linting rules  
- main.css: Global styling for UI

  ---

## Code Highlights

### Backend Code Execution (execute_code function)

- Writes user code to temporary files by language
- Compiles C/C++ code when needed
- Runs the code safely with timeouts
- Returns stdout or stderr to frontend

### AI Code Comment Generator (comment.py)

- Loads a local Hugging Face model for causal language modeling
- Takes a code snippet and generates commented version using AI

### Frontend App.jsx

- Manages app-wide states like code, language, output, loading
- Composes all UI components to create the code editor and terminal experience
- Controls chat bot visibility and interaction

### ESLint Configuration

- Supports React 18.3 features
- Includes recommended React and React Hooks linting rules
- Configured for JSX and modern ECMAScript syntax

---

Contributors

- Aryan Singh  
- Shivam Chaudhary  
- Abhinav Singh 

---

License

This project is licensed under the MIT License.

---

Acknowledgments

Special thanks to the open-source communities for React, Flask, Hugging Face, and ESLint for providing the powerful tools that made this project possible.
