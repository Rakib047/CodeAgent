# CodeAgent

**CodeAgent** is an AI-powered developer assistant that analyzes, refactors, tests, and documents Python code from GitHub repositories. It helps improve code quality and developer productivity using LLMs (Large Language Models) like Groq's LLaMA models.

---

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) for the interactive web interface  
- **Backend / Logic**:
  - Python
  - LLM API (Groq `llama3-70b-8192`)
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

- **Code Diff Viewer**  
  Visualize side-by-side differences between the original and refactored code to track all changes.

- **Requirements Updater**  
  Automatically update the `requirements.txt` file with the latest compatible versions for your specified Python version.

- **GitHub Integration**  
  - Enter any public GitHub repo URL and branch  
  - Browse files and analyze directly from the UI  
  - Commit refactored code or updated dependencies to a specific branch (creates branch if it doesn't exist)  
  - Create pull requests with a custom title and description to merge your changes into the main branch

- **Runtime Validator**
  - Automatically creates a virtual environment for a specified Python version
  - Installs dependencies from requirements.txt
  - Executes the refactored Python script
  - Captures and returns execution output and installed packages
  - Helps validate if the updated code runs successfully in isolation

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
