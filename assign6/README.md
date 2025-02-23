# Assignment 6: Explore Courses

Due Sunday, March 3rd at 11:59PM

## Overview

In this assignment you will be exercising your understanding of `std::optional`. We'll be making use of the same `courses.csv` from assignment 1. You are tasked to write one function for this assignment, which attempts to find the a `Course` in the `CourseDatabase` object, and return it.
You'll also explore the monadic operations that come with the `std::optional` class. Take a look at the code and review the `CourseDatabase` class to understand the interface.

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

## Part 2: Modifying the `main` function

Notice that we call the `find_course` here in the `main` function:

```cpp
auto course = db.find_course(argv[1]);
```

Now, you need to make use of the [monadic operations](https://en.cppreference.com/w/cpp/utility/optional) to populate the `output` string properly. Let's walk through how to do this.

Here's the behavior that you want to recreate, **without using any conditionals** like `if` statements:
```cpp
if (course.has_value()) {
    std::cout << "Found course: " << course->title << ","
            << course->number_of_units << "," << course->quarter << "\n";
} else {
    std::cout << "Course not found.\n";
}
```

Very simply, if there is a course then the line at the bottom of `main` 

```cpp
std::cout << output << std::end;
```

Should produce:
```bash
Found course: <title>,<number_of_units>,<quarter>
```

if there is no course then

```cpp
std::cout << output << std::end;
```

Should produce:
```bash
Course not found.
```

### Hints:
There are three monadic operations `and_then`, `transform`, and `or_else`. Read the description of each of them in the lecture slides, and take a look at [here](https://en.cppreference.com/w/cpp/utility/optional). Namely, you only need 2 of the mondadic operations.

Your code should end up looking something like this:

```cpp
    std::string output = course.<MONADIC_FN1>(<SOME LAMBDA FN>)
    .<MONADIC_FN2>(...);
```

Notice the lambda function being passed into the first monadic function. This should be a hint! **Think about what type output is** and what you're monadic opertaions therefore need to return/produce.


## 🚀 Submission Instructions

Before you submit the assignment, please fill out this [short feedback form](https://forms.gle/11LreWzsMa5U8VTT9). **Completion of the form is required to receive credit for the assignment.** After filling out the form, please upload the files to Paperless under the correct assignment heading.

Your deliverable should be:

- `main.cpp`

You may resubmit as many times as you'd like before the deadline.
