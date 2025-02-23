from utils import Autograder, ASSIGNMENT_DIR
from typing import List

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


def verify_output(courses: List[str], found: bool):
    main_path = get_main_exe_path()

    course_names = [course.split(",")[0] for course in courses]
    for course_name, course in zip(course_names, courses):
        result = subprocess.run(
            [main_path, course_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        actual = result.stdout.strip()

        expected = f"Found course: {course}" if found else "Course not found."

        if actual != expected:
            raise RuntimeError(
                f"For course {course_name}, expected output:\n\t{expected}\nbut got:\n\t{actual}"
            )


if __name__ == "__main__":
    grader = Autograder()
    grader.add_part(
        "Present Courses",
        lambda: verify_output(
            [
                "Introduction to Mobile Augmented Reality Design and Development,1,2023-2024 Spring",
                "Design for Play (SYMSYS 195G),4,2023-2024 Spring",
                "Practical Machine Learning,4,null",
                "Human-Centered AI,3,null",
                "Seminar in Artificial Intelligence in Healthcare,1,2023-2024 Autumn",
                "Introduction to Python Programming,1,2023-2024 Autumn",
                "Machine Learning for Discrete Optimization (MS&E 236),3,2023-2024 Spring",
                "AI for Social Good,2,2023-2024 Spring",
                "Software Project Experience with Corporate Partners,4,2023-2024 Winter",
                "The Future of Mechanical Engineering (ME 228),1,null",
            ],
            True,
        ),
    )

    grader.add_part(
        "Missing Courses",
        lambda: verify_output(
            [
                "Introduction to Quantum Mechanics for Engineers",
                "Fundamentals of Blockchain and Cryptography",
                "Applied Data Science for Social Impact",
                "Advanced Robotics and Autonomous Systems",
                "Neural Networks and Deep Learning Fundamentals",
                "Exploring the Future of Artificial General Intelligence",
                "Data Ethics and Privacy in the Digital Age",
                "Introduction to Cloud Computing with AWS",
                "Creative Coding for Interactive Media",
                "Virtual Reality and Augmented Reality for Healthcare",
            ],
            False,
        ),
    )

    grader.run(),
