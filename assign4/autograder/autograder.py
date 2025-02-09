from utils import Autograder

from typing import Dict, Iterable, Union

from colorama import Fore, Style
import difflib
import os
import re
import subprocess
import shutil
import sys

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
AUTOGRADER_DIR = os.path.join(PATH, "autograder")
CODE_PATH = os.path.join(PATH, "spellcheck.cpp")
EXAMPLES_PATH = os.path.join(PATH, "examples")
EXAMPLES_GOLD_PATH = os.path.join(AUTOGRADER_DIR, "gold")

# =============================================================================
# Verifying source code
# =============================================================================


FUNCTION_MATCHERS: Dict[str, Iterable[Union[str, Iterable[str]]]] = {
    "tokenize": [
        "find_all",
        "std::transform",
        "std::inserter",
        "std::erase_if",
        "#noloops",
    ],
    "spellcheck": [
        ["std::ranges::views::filter", "rv::filter"],
        ["std::ranges::views::transform", "rv::transform"],
        "!std::copy_if",
        "!std::transform",
        "levenshtein",
        "#noloops",
    ],
}


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


def tokenize_source(input_code: str) -> Iterable[str]:
    tokens = []

    pattern_fqn = re.compile(r"^(::)?[a-zA-Z_][a-zA-Z0-9_]*(::[a-zA-Z_][a-zA-Z0-9_]*)*")
    pattern_non_word = re.compile(r"^\W+")

    while input_code:
        fqn_match = pattern_fqn.match(input_code)
        if fqn_match:
            tokens.append(fqn_match.group().strip())
            input_code = input_code[len(fqn_match.group()) :]
        else:
            non_word_match = pattern_non_word.match(input_code)
            if non_word_match:
                tokens.append(non_word_match.group().strip())
                input_code = input_code[len(non_word_match.group()) :]
            else:
                tokens.append(input_code[0])
                input_code = input_code[1:]

    return [t for t in tokens if t]


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
        methods[method_name] = tokenize_source(method_body)
        pos = end_idx

    return methods


def add_matcher_tests(grader: Autograder, file: str):
    student_methods = parse_methods(file)
    for method, matchers in FUNCTION_MATCHERS.items():

        def generate_test_method(method_copy, matchers_copy):
            def test():
                if method_copy not in student_methods:
                    raise RuntimeError(
                        f"Could not find a definition for required method '{method_copy}' in {file}"
                    )

                method_body = student_methods[method_copy]

                for matcher in matchers_copy:
                    if matcher == "#noloops":
                        for loop_type in ["for", "while", "goto"]:
                            if loop_type in method_body:
                                raise RuntimeError(
                                    f"Method {method_copy} may not contain any explicit for/while loops! You must use the STL instead! Found loop: {loop_type}"
                                )
                        print(f"🔎 {method_copy} has no for/while loops!")
                        continue

                    if isinstance(matcher, str):
                        matcher = [matcher]

                    for m in matcher:
                        if m.startswith("!"):
                            m = m[1:]
                            if m in method_body:
                                raise RuntimeError(f"Method '{method_copy}' is not allowed to call method: {m}")
                        elif m in method_body:
                            print(f"🔎 {method_copy} called method {m}")
                            break
                    else:
                        if not any(m.startswith("!") for m in matcher):
                            raise RuntimeError(
                                f"Method '{method_copy}' must call one of the following methods: {matcher}."
                            )

            return test

        grader.add_part(method, generate_test_method(method, matchers))

    # Ensure no helper function were used
    def test_no_helper_functions():
        present = set(student_methods.keys())
        expected = set(FUNCTION_MATCHERS.keys())
        extra = present - expected
        if extra:
            raise RuntimeError(
                f"You may not use any helper functions for this assignment. You must implement all your code in the following functions: {', '.join(expected)}. \n\nFound extra functions: {', '.join(extra)}"
            )

    grader.add_part(
        "Check submission has no helper functions", test_no_helper_functions
    )


def no_obvious_namespace_std():
    with open(CODE_PATH, "r") as file:
        content = file.read()
    content = remove_comments_strings(content)
    content = content.replace("\n", " ")
    using_namespace = re.compile(r"using\s+namespace\s+std\s*;")
    if using_namespace.search(content):
        raise RuntimeError(
            "You should not use 'using namespace std;' for this assignment. In general, this is considered bad practice as it can lead to naming conflicts, and will affect the autograder for this assignment."
        )


# =============================================================================
# Verifying program correctness
# =============================================================================


import os
import subprocess


def find_executable(containing_dir):
    # Search for the executable in the given directory
    for filename in ("main", "main.exe"):
        exe_path = os.path.join(containing_dir, filename)
        if os.path.isfile(exe_path) and os.access(exe_path, os.X_OK):
            return exe_path
    raise FileNotFoundError(
        f"No executable named 'main' or 'main.exe' found in '{containing_dir}'."
    )


def spellcheck(file_path):
    exe_path = find_executable(PATH)
    command = [exe_path, "--stdin", "--unstyled"]

    with open(file_path, "r", encoding="utf-8") as file:
        result = subprocess.run(
            command,
            stdin=file,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8"
        )

    return result.stdout


def generate_gold_dir():
    if os.path.exists(EXAMPLES_GOLD_PATH):
        shutil.rmtree(EXAMPLES_GOLD_PATH)
    os.makedirs(EXAMPLES_GOLD_PATH)

    for example_file in os.listdir(EXAMPLES_PATH):
        example_file_path = os.path.join(EXAMPLES_PATH, example_file)
        if not os.path.isfile(example_file_path):
            continue
        try:
            output = spellcheck(example_file_path)
            gold_file_path = os.path.join(EXAMPLES_GOLD_PATH, example_file)
            with open(gold_file_path, "w", encoding="utf-8") as gold_file:
                gold_file.write(output)

            print(f"Processed {example_file} -> {gold_file_path}")
        except Exception as e:
            print(f"Failed to process {example_file}: {e}")


def assert_contents_equal(expected, actual, filename):
    if expected != actual:
        expected_lines = expected.split("\n")
        actual_lines = actual.split("\n")

        diff = list(
            difflib.unified_diff(
                expected_lines,
                actual_lines,
                fromfile="Expected in solution, missing in your output",
                tofile="Present in your output, missing in solution",
            )
        )

        diff = [f"\t{l}" for l in diff]
        diff[0] = diff[0].rstrip()
        diff_output = "\n".join(diff)

        def matcher(fore):
            return (
                lambda match: f"{fore}{Style.BRIGHT}{match.group(0)}{Style.RESET_ALL}"
            )

        diff_output = re.sub(
            r"^\s*-+", matcher(Fore.RED), diff_output, flags=re.MULTILINE
        )
        diff_output = re.sub(
            r"^\s*\++", matcher(Fore.GREEN), diff_output, flags=re.MULTILINE
        )

        error_lines = [
            f"Contents do not match solution:",
            diff_output,
            "",
            f"\t{Fore.CYAN}To see the output of your submission on this file, run:",
            "",
            f'\t\t ./main --stdin < "examples/{filename}"',
            "",
            f'\tTo see the expected solution output, open "autograder/gold/{filename}"{Fore.RESET}',
        ]

        raise RuntimeError("\n".join(error_lines))


def test_spellcheck():
    for example_file in os.listdir(EXAMPLES_GOLD_PATH):
        gold_path = os.path.join(EXAMPLES_GOLD_PATH, example_file)
        input_path = os.path.join(EXAMPLES_PATH, example_file)

        if not os.path.isfile(input_path):
            raise RuntimeError(
                f"Could not find gold file for example '{example_file}'. Did you modify the examples/ directory?"
            )

        with open(gold_path, "r", encoding="utf-8") as f:
            gold_output = f.read()

        spellcheck_result = spellcheck(input_path)

        assert_contents_equal(gold_output, spellcheck_result, example_file)
        print(f"🔎 {example_file} spellcheck matched solution!")


# =============================================================================
# Autograder setup
# =============================================================================

if __name__ == "__main__":
    if "--gold" in sys.argv:
        generate_gold_dir()
        sys.exit(0)

    grader = Autograder()
    grader.setup = no_obvious_namespace_std
    add_matcher_tests(grader, CODE_PATH)
    grader.add_part("Spellcheck", test_spellcheck)
    grader.run()
