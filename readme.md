# Legacy Demo Project

A demo legacy Python 2.x codebase with multiple modules.  
**Note:** This project is for legacy reference and is not recommended for new development.

## Table of Contents

- [Files](#files)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Files

- `legacy_code.py`: Main entry point.
- `utils.py`: Utility functions.
- `data_processing.py`: Data loading and processing.
- `math_ops.py`: Math operations.
- `file_handler.py`: File reading.
- `config.py`: Configuration variables.
- `logger.py`: Simple logger.
- `legacy_api.py`: Mock API calls.
- `tests.py`: Basic tests.

## Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone <repo-url>
    cd legacy_repo
    ```

2. **Create Python 2.7 virtual environment:**
    ```bash
    virtualenv -p python2.7 venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the main application:
```bash
python legacy_code.py
```

You can modify configuration options in `config.py` as needed.

## Testing

To run the basic tests:
```bash
python tests.py
```

## Project Structure

```
legacy_repo/
├── legacy_code.py
├── utils.py
├── data_processing.py
├── math_ops.py
├── file_handler.py
├── config.py
├── logger.py
├── legacy_api.py
├── tests.py
├── requirements.txt
└── README.md
```


