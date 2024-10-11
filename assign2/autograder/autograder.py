from utils import Autograder
import os

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
AUTOGRADER_DIR = os.path.join(PATH, "autograder")
TEST_FILE_PATH = os.path.join(PATH, "students.txt")


def get_initials(name):
    parts = name.split()
    if len(parts) == 2:
        return parts[0][0] + parts[1][0]
    return None


def read_students_file(filename):
    with open(filename, "r") as file:
        return {line.strip() for line in file.readlines()}


def test_applicants_set():
    expected_possible_matches = read_students_file(TEST_FILE_PATH)

    student_output_set_path = os.path.join(AUTOGRADER_DIR, "student_output/set.txt")

    with open(student_output_set_path, "r") as possible_matches_file:
        possible_matches = {line.strip() for line in possible_matches_file.readlines()}

    if possible_matches != expected_possible_matches:
        raise RuntimeError(
            f"❌ Output does not match expected set of possible matches. Diff: {possible_matches ^ expected_possible_matches}"
        )


def test_match():
    all_students = read_students_file(TEST_FILE_PATH)

    student_output_match_path = os.path.join(AUTOGRADER_DIR, "student_output/match.txt")

    with open(student_output_match_path, "r") as student_file:
        lines = [line.strip() for line in student_file.readlines()]

    if len(lines) < 2:
        raise RuntimeError("❌ Student name and match not found in match.txt file")

    student_name = lines[0]
    student_match = lines[1]

    if student_name == "STUDENT TODO":
        raise RuntimeError("❌ You must replace kYourName in main.cpp with your name!")

    student_initials = get_initials(student_name)
    if not student_initials:
        raise RuntimeError(f"❌ Invalid student name format: {student_name}")

    expected_matches = {
        name for name in all_students if get_initials(name) == student_initials
    }

    match = student_match.split("Your match is: ")[1].strip()

    if match != "NO MATCHES FOUND.":
        if match not in expected_matches:
            raise RuntimeError(
                f"Matched student '{match}' is not in the expected set of matches: {expected_matches}"
            )
    print(f"✅ Matched student '{match}'")


if __name__ == "__main__":
    grader = Autograder()
    grader.add_part("test_applicants_set", test_applicants_set)
    grader.add_part("test_match", test_match)

    grader.setup = None
    grader.teardown = None
    grader.run()
