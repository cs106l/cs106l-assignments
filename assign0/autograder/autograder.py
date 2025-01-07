from utils import Autograder

import base64
from colorama import Fore
import difflib
import pickle
import re
import os
import subprocess
import getpass

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
AUTOGRADER_DIR = os.path.join(PATH, "autograder")

def test_python_installed():
    """Check that Python is installed."""
    try:
        result = subprocess.run(["python3", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert result.returncode == 0, "Python 3 is not installed or not in PATH."
    except FileNotFoundError:
        raise AssertionError("Python 3 is not installed or not in PATH.")


def test_vscode_installed():
    """Check that VSCode is installed."""
    try:
        result = subprocess.run(["code", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert result.returncode == 0, "VSCode is not installed or not in PATH."
    except FileNotFoundError:
        raise AssertionError("VSCode is not installed or not in PATH.")


def test_cpp_compiler():
    """Check that a C++ compiler is installed."""
    try:
        result = subprocess.run(["g++", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert result.returncode == 0, "C++ compiler (g++) not found or not working."
    except FileNotFoundError:
        raise AssertionError("C++ compiler (g++) not installed or not in PATH.")


def test_git_installed():
    """Check that Git is installed."""
    try:
        result = subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert result.returncode == 0, "Git is not installed or not in PATH."
    except FileNotFoundError:
        raise AssertionError("Git is not installed or not in PATH.")


def test_environment_setup():
    """Verify all setup steps."""
    # Get the logged-in user's name
    user = getpass.getuser()
    print(f"Hey {user}, you have set up correctly! Woot woot! 🙂")

def setup():
    pass    


def teardown():
    pass

if __name__ == "__main__":
    grader = Autograder()
    grader.setup = None
    grader.teardown = None
    grader.add_part("Check C++ Compiler", test_cpp_compiler)
    grader.add_part("Check VSCode Installation", test_vscode_installed)
    grader.add_part("Check Git Installation", test_git_installed)
    grader.add_part("Check Python Installation", test_python_installed)
    grader.add_part("Environment Setup Success Message", test_environment_setup)
    grader.run()