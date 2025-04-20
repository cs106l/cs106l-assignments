from utils import Autograder

import base64
from colorama import Fore
import difflib
import pickle
import re
import os

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
AUTOGRADER_DIR = os.path.join(PATH, "autograder")

SOLN_NOT_OFFERED_BIN = os.path.join(AUTOGRADER_DIR, "courses_not_offered.bin")
SOLN_OFFERED_BIN = os.path.join(AUTOGRADER_DIR, "courses_offered.bin")
SOLN_OFFERED = os.path.join(AUTOGRADER_DIR, "courses_offered.csv")
SOLN_NOT_OFFERED = os.path.join(AUTOGRADER_DIR, "courses_not_offered.csv")


def binary_to_csv(binary_filename, csv_filename):
    with open(binary_filename, "rb") as pickle_file:
        encoded_data = pickle.load(pickle_file)
    decoded_data = base64.b64decode(encoded_data).decode("utf-8")
    with open(csv_filename, "w") as output_file:
        output_file.write(decoded_data)


def csv_to_binary(csv_filename, binary_filename):
    with open(csv_filename, "r") as file:
        lines = file.read()
    encoded_data = base64.b64encode(lines.encode("utf-8"))
    with open(binary_filename, "wb") as pickle_file:
        pickle.dump(encoded_data, pickle_file)


def check_files_equal(expected, actual):
    if not os.path.exists(expected):
        raise RuntimeError(
            f"Solution file '{os.path.relpath(expected, PATH)}' does not exist"
        )
    if not os.path.exists(actual):
        raise RuntimeError(
            f"Output file '{os.path.relpath(actual, PATH)}' does not exist"
        )

    with open(expected, "r") as f1, open(actual, "r") as f2:
        expected_lines = f1.readlines()
        actual_lines = f2.readlines()

    if expected_lines != actual_lines:
        diff = list(
            difflib.unified_diff(
                expected_lines, actual_lines, fromfile=expected, tofile=actual
            )
        )

        if len(diff) > 10:
            diff = diff[:10] + ["... (truncated, showing first 10 lines of diff) ...\n"]

        diff = [f"\t{l}" for l in diff]
        diff_output = "".join(diff)

        diff_output = re.sub(r"^\s*-+", lambda match: f"{Fore.RED}{match.group(0)}{Fore.RESET}", diff_output, flags=re.MULTILINE)
        diff_output = re.sub(r"^\s*\++", lambda match: f"{Fore.GREEN}{match.group(0)}{Fore.RESET}", diff_output, flags=re.MULTILINE)

        raise RuntimeError(
            f"Contents of '{os.path.relpath(actual, PATH)}' do not equal solution:\n{diff_output}"
        )


def setup():
    binary_to_csv(SOLN_NOT_OFFERED_BIN, SOLN_NOT_OFFERED)
    binary_to_csv(SOLN_OFFERED_BIN, SOLN_OFFERED)


def teardown():
    os.remove(SOLN_OFFERED)
    os.remove(SOLN_NOT_OFFERED)


def test_write_courses_offered():
    student = os.path.join(PATH, "student_output/courses_offered.csv")
    check_files_equal(SOLN_OFFERED, student)


def test_write_courses_not_offered():
    student = os.path.join(PATH, "student_output/courses_not_offered.csv")
    check_files_equal(SOLN_NOT_OFFERED, student)


if __name__ == "__main__":
    grader = Autograder()
    grader.add_part("write_course_offered", test_write_courses_offered)
    grader.add_part("write_course_not_offered", test_write_courses_not_offered)

    grader.setup = setup
    grader.teardown = teardown
    grader.run()
