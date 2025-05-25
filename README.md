Codex - AI-Powered Code Editor & Executor

Codex is an interactive code editor and executor designed to enhance coding productivity by providing real-time code editing, execution in multiple languages, terminal output viewing, and AI-powered assistance features such as code commenting and chat-based help.

---

About the Project

The project integrates frontend and backend components to offer a smooth development experience:

- Code Editor: Supports multiple programming languages with syntax highlighting and line tracking.
- Code Execution: Executes user-written code in Python, JavaScript, C, and C++ securely on the backend, returning output/errors.
- Terminal: Displays execution results in a collapsible terminal view.
- AI Bot & Prompt: Provides interactive chat-based code assistance, including explanations and code commenting using AI models.
- Custom ESLint Config: Ensures React-based frontend code quality with linting rules tailored for React 18.3.
- Responsive UI: Clean, modern interface built with React and styled using CSS.

---

Features

- Multi-language code execution (Python, JavaScript, C, C++)
- Real-time code editing with syntax highlighting
- Terminal to view output/errors from executed code
- AI-powered bot for code comments and explanations
- Clean React UI with language and code state management
- ESLint configuration customized for React projects

---

Technologies Used

- Frontend: React, JSX, CSS  
- Backend: Python, Flask, subprocess for code execution  
- AI Models: Hugging Face transformers (local model loading), custom Together API client for code generation  
- Code Linting: ESLint with plugins for React, React Hooks, and React Refresh  
- Tooling: Vite for frontend bundling  

---

Getting Started

### Clone the Repository

```bash
git clone https://github.com/yourusername/codex.git
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

Code Highlights

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
