from utils import Autograder

from typing import Dict, Iterable, List, Tuple, Union

import os
import re

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
AUTOGRADER_DIR = os.path.join(PATH, "autograder")
MAIN_CPP_PATH = os.path.join(PATH, "main.cpp")

kRangeThreshold = 5
kAvgTempThreshold = 60

FUNCTION_MATCHERS: Dict[str, Iterable[Union[str, Iterable[str]]]] = {
    "compute_forecast": ["std::min_element", "std::max_element", "std::accumulate"],
    "get_forecasts": ["compute_forecast", "std::transform"],
    "get_filtered_data": ["std::remove_if"],
    "get_shuffled_data": ["std::shuffle"],
    "run_weather_pipeline": ["get_filtered_data", "get_forecasts", "get_shuffled_data"],
}


def fix_datum(datum: Tuple[float, float, float]) -> str:
    return f"min = {datum[0]:.4f} average = {datum[1]:.4f} max = {datum[2]:.4f}"


def get_gold(file: os.PathLike) -> List[str]:
    records = []
    with open(file, "r") as f:
        for line in f:
            data = [float(x) for x in line.strip().split()]
            m = min(data)
            M = max(data)
            a = sum(data) / len(data)
            if M - m < kRangeThreshold:
                continue
            if a < kAvgTempThreshold:
                continue
            records.append(fix_datum((m, M, a)))
    return records


def get_student(file: os.PathLike) -> List[str]:
    data = []
    with open(file, "r") as f:
        for line in f:
            data.append(fix_datum(tuple(float(x) for x in line.strip().split())))
    return data


def test_valid_shuffle():
    STUDENT_FILE = os.path.join(AUTOGRADER_DIR, "student.txt")
    SOURCE_FILE = os.path.join(AUTOGRADER_DIR, "data.txt")

    student_raw = get_student(STUDENT_FILE)
    gold_raw = get_gold(SOURCE_FILE)

    student = sorted(student_raw)
    gold = sorted(gold_raw)
    
    if student_raw == gold:
        raise RuntimeError(
            "Student output appears unshuffled. Are you sure you shuffled your forecasts?"
        )

    if student != gold:
        extra = set(student) - set(gold)
        missing = set(gold) - set(student)

        if extra:
            extra_str = "\n\t - ".join([""] + list(extra))
            print(f" - Extra: {extra_str}\n")
        if missing:
            missing_str = "\n\t -".join([""] + list(missing))
            print(f" - Missing: {missing_str}\n")

        raise RuntimeError("Shuffled forecasts do not match.")


def remove_comments_strings(content):
    comment_pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    comment_regex = re.compile(comment_pattern, re.MULTILINE | re.DOTALL)
    string_pattern = r"\".*?\""
    string_regex = re.compile(string_pattern, re.MULTILINE | re.DOTALL)

    content = comment_regex.sub(
        lambda match: "" if match.group(2) is not None else match.group(1), content
    )
    content = string_regex.sub("", content)

    return content


def parse_methods(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    content = remove_comments_strings(content)

    method_pattern = re.compile(r"\b(\w+)\s*\([^)]*\)\s*\{")
    methods = {}
    pos = 0

    while True:
        match = method_pattern.search(content, pos)
        if not match:
            break

        method_name = match.group(1)
        if method_name in methods:
            raise RuntimeError(
                f"Duplicate method definition of '{method_name}'. Have you tried recompiling your code?"
            )

        start_idx = match.end() - 1
        brace_stack = 1
        end_idx = start_idx + 1

        while brace_stack > 0:
            if end_idx >= len(content):
                raise RuntimeError(
                    f"Unmatched braces in method definition of '{method_name}'. Have you tried recompiling your code?"
                )
            if content[end_idx] == "{":
                brace_stack += 1
            elif content[end_idx] == "}":
                brace_stack -= 1
            end_idx += 1

        method_body = content[start_idx + 1 : end_idx - 1].strip()
        methods[method_name] = method_body
        pos = end_idx

    return methods


def add_matcher_tests(grader: Autograder):
    student_methods = parse_methods(MAIN_CPP_PATH)
    for method, matchers in FUNCTION_MATCHERS.items():

        def generate_test_method(method_copy, matchers_copy):
            def test():
                if method_copy not in student_methods:
                    raise RuntimeError(
                        f"Could not find a definition for required method '{method_copy}' in main.cpp"
                    )
                for matcher in matchers_copy:
                    if isinstance(matcher, str):
                        matcher = [matcher]

                    for m in matcher:
                        if m in student_methods[method_copy]:
                            print(f"🔎 {method_copy} called method {m}")
                            break
                    else:
                        raise RuntimeError(
                            f"Method '{method_copy}' must call one of the following methods: {matcher}."
                        )

            return test

        grader.add_part(method, generate_test_method(method, matchers))


def setup():
    with open(MAIN_CPP_PATH, "r") as file:
        content = file.read()
    content = remove_comments_strings(content)
    content = content.replace("\n", " ")
    using_namespace = re.compile(r"using\s+namespace\s+std\s*;")
    if using_namespace.search(content):
        raise RuntimeError(
            "You should not use 'using namespace std;' for this assignment. In general, this is considered bad practice as it can lead to naming conflicts, and will affect the autograder for this assignment."
        )


if __name__ == "__main__":
    grader = Autograder()
    grader.setup = setup
    grader.add_part("Valid Shuffle", test_valid_shuffle)
    add_matcher_tests(grader)
    grader.run()
