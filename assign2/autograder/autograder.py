from utils import Autograder

import base64
from colorama import Fore
import difflib
import pickle
import re
import os

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
AUTOGRADER_DIR = os.path.join(PATH, "autograder")

def setup():
    '''
    Write to the file using student's code
    '''
    pass

def teardown():
    '''
    Clean up the file here
    '''
    pass

def test_applicants_set():    
    pass

def test_match():
    pass    
    
if __name__ == "__main__":
    grader = Autograder()
    grader.add_part("test_applicants_set", test_applicants_set)
    grader.add_part("test_match", test_match)

    grader.setup = setup
    grader.teardown = teardown
    grader.run()
