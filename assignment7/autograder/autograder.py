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


def verify_output(
    test_case: str, *, expected: List[str] = [], hint: str = "", empty_hint: str = "", show_diff: bool = True
):
    hint = hint.strip()
    has_hint = bool(hint)
    if has_hint:
        hint += " "

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
        error = result.stderr.strip()
        if not error and empty_hint:
            raise RuntimeError(empty_hint)
        if has_hint:
            if error:
                raise RuntimeError(f"{hint}Got the following error message:\n\n{error}")
            raise RuntimeError(f"{hint}")
        raise RuntimeError(error)

    actual = result.stdout.strip()
    if not actual:
        actual = []
    else:
        actual = actual.split("\n")

    if actual != expected:
        nl = "\n\t"
        if show_diff:
            raise RuntimeError(
                f"Test output did not match expected. Expected: \n{nl}{nl.join(expected)}\n\nGot: \n{nl}{nl.join(actual)}\n\n{hint}"
            )
        raise RuntimeError(hint)


if __name__ == "__main__":
    grader = Autograder()
    grader.add_part(
        "Part 1: Destructor",
        lambda: verify_output("destructor", hint="Did you make sure to set the underlying pointer to `nullptr` in the `nullptr` version of the constructor? If you didn't, you might be trying to delete an arbitrary region of memory!"),
    )

    grader.add_part(
        "Part 1: Deleted copy constructor and assignment", lambda: verify_output("copy")
    )

    grader.add_part(
        "Part 1: Move constructor",
        lambda: verify_output(
            "move_constructor",
            expected=["400308000"],
            hint="Did you make sure to set the other unique_ptr to nullptr in the move constructor? It may help to review the lecture on move semantics!",
            show_diff=False,
        ),
    )

    grader.add_part(
        "Part 1: Move assignment",
        lambda: verify_output(
            "move_assignment",
            hint="Did you make sure to deallocate the existing data before assigning the private fields? It may help to review the lecture on move semantics!",
            show_diff=False,
        ),
    )

    grader.add_part(
        "Part 1: Move assignment (self-assignment)",
        lambda: verify_output(
            "move_self_assignment",
            hint="Did you make sure to check for self-assignment in the move assignment operator? You should have code that checks `if (this == &other) ...`. It may help to review the lecture on move semantics!",
            expected=["400308000"],
            show_diff=False,
        ),
    )

    grader.add_part(
        "Part 2: Linked List",
        lambda: verify_output(
            "linked_list",
            expected=[
                "Constructing node with value 'Sean'",
                "Constructing node with value 'Chris'",
                "Constructing node with value 'Keith'",
                "Constructing node with value 'Fabio'",
                "Constructing node with value 'Jacob'",
                "Jacob",
                "Fabio",
                "Keith",
                "Chris",
                "Sean",
                "Destructing node with value 'Jacob'",
                "Destructing node with value 'Fabio'",
                "Destructing node with value 'Keith'",
                "Destructing node with value 'Chris'",
                "Destructing node with value 'Sean'",
            ],
            empty_hint="Hmm... that didn't work. Make sure that you are passing all of the previous tests! You might have an issue with your `unique_ptr` implementation."
        ),
    )

    grader.run(),
