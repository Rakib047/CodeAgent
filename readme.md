# CodeAgent

**CodeAgent** is an AI-powered developer assistant that analyzes, refactors, tests, and documents Python code from GitHub repositories. It helps improve code quality and developer productivity using LLMs (Large Language Models) like Groq's LLaMA models.

---

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) for the interactive web interface  
- **Backend / Logic**:
  - Python
  - LLM API (Groq LLaMA 3.1 8B Instant)
  - GitHub API (for file access)
- **Project Structure**:
  - `src/utils/`: GitHub + token handling utilities
  - `src/llm/`: Logic for code analysis, refactoring, test case generation, and documentation

---

## Features

- **Code Analyzer**  
  Analyze GitHub-hosted Python files for:
  - Outdated syntax
  - Hard-coded values
  - Code smells
  - Anti-patterns
  - Maintainability issues

- **Code Refactorer**  
  Refactor legacy or modern Python code to a specified version (e.g., `python3.10`) using clean, idiomatic best practices.

- **Test Case Generator**  
  Automatically generate `pytest`-compatible unit tests for refactored code using LLMs.

- **Documentation Generator**  
  Generate professional Python documentation (docstrings, module overviews) based on the refactored code and version.

- **GitHub Integration**  
  - Enter any public GitHub repo URL and branch
  - Browse files and analyze directly from the UI

---

## How to Run Locally

### 1. Clone the Repository

```bash
git clone "https://github.com/Rakib047/CodeAgent.git"
cd CodeAgent
```
### 2. Set Up a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate 
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Set Environment Variables (Optional)
Create a `.env` file:
```
GROQ_API_KEY = your_groq_api_key
```
### 5. Run the Streamlit App
```bash
cd .\notebooks\
streamlit run streamlite_app.py
```
