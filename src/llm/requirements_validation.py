import subprocess
import tempfile
import os
import sys
import shutil

def validate_requirements_and_run_code(requirements_text: str, python_code_file: str, python_version: str = None):
    if python_version:
        python_executable = shutil.which(f"python{python_version}")
        if not python_executable:
            print(f"Python {python_version} not found. Falling back to current Python: {sys.executable}")
            python_executable = sys.executable
    else:
        python_executable = sys.executable

    with tempfile.TemporaryDirectory() as temp_dir:
        venv_dir = os.path.join(temp_dir, "venv")
        requirements_file = os.path.join(temp_dir, "requirements.txt")
        test_script_file = os.path.join(temp_dir, "test_script.py")

        # Write the requirements.txt
        with open(requirements_file, "w") as f:
            f.write(requirements_text)

        # Copy the provided script to the temp directory
        try:
            shutil.copy(python_code_file, test_script_file)
        except Exception as e:
            return False, f"Failed to copy script: {str(e)}", []

        # Step 1: Create virtual environment
        try:
            subprocess.run([python_executable, "-m", "venv", venv_dir], check=True)
        except subprocess.CalledProcessError:
            return False, "Failed to create virtual environment.", []

        pip_path = os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip.exe")
        python_path = os.path.join(venv_dir, "bin", "python") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "python.exe")

        # Step 2: Install dependencies
        try:
            # subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
            subprocess.run([pip_path, "install", "-r", requirements_file], check=True)
        except subprocess.CalledProcessError:
            return False, "Failed to install one or more packages.", []

        # Step 3: Run the Python script inside the virtual environment
        try:
            result = subprocess.run([python_path, test_script_file], check=True, capture_output=True, text=True)
            script_output = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, f"Script execution failed:\n{e.stderr.strip()}", []

        # Step 4: List installed packages
        try:
            result = subprocess.run([pip_path, "list"], stdout=subprocess.PIPE, check=True, text=True)
            installed_packages = result.stdout.strip().splitlines()[2:]  # Skip headers
        except subprocess.CalledProcessError:
            installed_packages = []

        return True, f"All good. Script ran successfully.\n\nOutput:\n{script_output}", installed_packages
