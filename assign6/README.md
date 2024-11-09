# Assignment 6: Explore Courses

Due Friday, November 15th at 11:59PM

## Overview

> [!IMPORTANT]
> To complete this assignment you'll need the content in the lecture on November 12th.
> We've scoped this assignment such that it should be reasonable to finish it by Friday, even though the lecture is on Tuesday.

In this assignment you will be exercising your understanding of `std::optional`. We'll be making use of the same `courses.csv` from assignment 1. You are tasked to write one function for this assignment, which attempts to find the a `Course` in the `CourseDatabase` object, and return it. Take a look at the code and review the `CourseDatabase` class to understand the interface.

## Running your code

To run your code, first you'll need to compile it. Open up a terminal (if you are using VSCode, hit <kbd>Ctrl+\`</kbd> or go to **Terminal > New Terminal** at the top). Then make sure that you are in the `assign6/` directory and run:

```sh
g++ -std=c++20 main.cpp -o main
```

Assuming that your code compiles without any compiler errors, you can now do:

```sh
./main
```

which will actually run the `main` function in `main.cpp`.

As you are following the instructions below, we recommend intermittently compiling/testing with the autograder as a way to make sure you're on the right track!

> [!NOTE]
>
> ### Note for Windows
>
> On Windows, you may need to compile your code using
>
> ```sh
> g++ -static-libstdc++ -std=c++20 main.cpp -o main
> ```
>
> in order to see output. Also, the output executable may be called `main.exe`, in which case you'll run your code with:
>
> ```sh
> ./main.exe
> ```

## Part 0: Include `<optional>`

At the top of the `main.cpp` include `<optional>`, we're going to make use of `std::optional` in this assignment!

## Part 1: Write the `find_course` function

This function takes in a string `course_title`, and the function should try to find the `course` inside of the private `courses` member of the `CourseDatabase` object. What should the return type be? (hint: there may or may not be a `Course` for the `course_title` passed in)

> [!NOTE]
> You need to change the type returned by `find_course` which is currenty `FillMeIn`.

## Part 2: Change the conditional in the `main` function

Notice that we call the `find_course` here in the `main` function:

```cpp
auto course = db.find_course(argv[1]);
```

Now, you need to change the conditional that prints out whether or not a course is found.
Currently the conditional is:

```cpp
if (false) {...}
```

Think about the type of `course`, and the interface of that type.

## 🚀 Submission Instructions

Before you submit the assignment, please fill out this [short feedback form](https://forms.gle/VWH3ADoSDfBgxiSG9). **Completion of the form is required to receive credit for the assignment.** After filling out the form, please upload the files to Paperless under the correct assignment heading.

Your deliverable should be:

- `main.cpp`

You may resubmit as many times as you'd like before the deadline.
