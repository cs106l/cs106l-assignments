import functools
from typing import List
from utils import Autograder, ASSIGNMENT_DIR

import os
import subprocess


def get_main_exe_path() -> os.PathLike:
    main_path = os.path.join(ASSIGNMENT_DIR, "main")
    if not os.path.isfile(main_path):
        main_path = os.path.join(ASSIGNMENT_DIR, "main.exe")
    if not os.path.isfile(main_path):
        raise RuntimeError(
            "Could not find a main executable. Did you compile your code with the command in the README?"
        )
    return main_path


@functools.lru_cache
def get_memory_leak_exit_code() -> int:
    main_path = get_main_exe_path()
    result = subprocess.check_output([main_path, "memory_leak_exit_code"], text=True)
    return int(result.strip())


def verify_output(test_case: str, expected: List[str]):
    main_path = get_main_exe_path()
    result = subprocess.run(
        [main_path, test_case],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode == get_memory_leak_exit_code():
        raise RuntimeError(f"💧Memory leak detected: {result.stderr}")

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    actual = result.stdout.strip()
    if not actual:
        actual = []
    else:
        actual = actual.split("\n")

    if actual != expected:
        nl = "\n\t"
        raise RuntimeError(
            f"Test output did not match expected. Expected: \n{nl}{nl.join(expected)}\n\nGot: \n{nl}{nl.join(actual)}"
        )


if __name__ == "__main__":
    grader = Autograder()
    grader.add_part(
        "Part 1: operator<<",
        lambda: verify_output(
            "insertion_operator",
            [
                "User(name=Alice, friends=[])",
                "User(name=Bob, friends=[Alice])",
                "User(name=Charlie, friends=[Alice, Bob])",
            ],
        ),
    )

    grader.add_part("Part 2: Destructor", lambda: verify_output("destructor", []))

    grader.add_part(
        "Part 2: Copy Constructor",
        lambda: verify_output(
            "copy_constructor",
            [
                "User(name=Alice, friends=[F, F, F, F, F, F, F, F, F])",
                "User(name=Alice, friends=[Bob, Alice, Charlie, F, F, F, F, F, F])",
            ],
        ),
    )

    grader.add_part(
        "Part 2: Copy Assignment Operator",
        lambda: verify_output(
            "copy_assignment",
            [
                "User(name=Bob, friends=[BF, BF, BF, BF, BF, BF, BF, BF, BF])",
                "User(name=Bob, friends=[BF, BF, BF, BF, BF, BF, BF, BF, BF])",
            ],
        ),
    )

    grader.add_part(
        "Part 2: Move Constructor", lambda: verify_output("move_constructor", [])
    )
    grader.add_part(
        "Part 2: Move Assignment Operator", lambda: verify_output("move_assignment", [])
    )

    grader.add_part(
        "Part 3: operator+=",
        lambda: verify_output(
            "compound_assignment",
            ["User(name=Alice, friends=[Bob])", "User(name=Bob, friends=[Alice])"],
        ),
    )

    grader.add_part(
        "Part 3: operator<",
        lambda: verify_output(
            "comparable",
            [
                "A < B is true",
                "B < A is false",
                "B < C is true",
                "C < B is false",
                "C < A is false",
                "A < C is true",
            ],
        ),
    )

    grader.run(),
