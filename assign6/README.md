# Assignment 6: Explore Courses

Due Sunday, March 3rd at 11:59PM

## Overview

In this assignment you will be exercising your understanding of `std::optional`. We'll be making use of the same `courses.csv` from assignment 1. You are tasked to write one function for this assignment, which attempts to find the a `Course` in the `CourseDatabase` object, and return it.
You'll also explore the monadic operations that come with the `std::optional` class. Take a look at the code and review the `CourseDatabase` class to understand the interface.

## Running your code

To run your code, first you'll need to compile it. Open up a terminal (if you are using VSCode, hit <kbd>Ctrl+\`</kbd> or go to **Terminal > New Terminal** at the top). Then make sure that you are in the `assign6/` directory and run:

```sh
g++ -std=c++23 main.cpp -o main
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
> g++ -static-libstdc++ -std=c++23 main.cpp -o main
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

### Monadic Operations

There are three monadic operations: [`and_then`](https://en.cppreference.com/w/cpp/utility/optional/and_then), [`transform`](https://en.cppreference.com/w/cpp/utility/optional/transform), and [`or_else`](https://en.cppreference.com/w/cpp/utility/optional/or_else). Read the description of each of them in the lecture slides, and take a look at [the standard library documentation](https://en.cppreference.com/w/cpp/utility/optional). You will only need to use 2 of the mondadic operations.

Your code should end up looking something like this:

```cpp
std::string output = course
    ./* monadic function one */ (/* ... */)
    ./* monadic function two */ (/* ... */)
    .value();                                  // OR `.value_or(...)`, see below
```

It can help to **think about what the type of `output` is and work backwards from there**. Pay attention to what each of the monadic functions does, as described in the hint below.

> [!NOTE]  
> Recall what the role is of each of the monadic functions. The official C++ library doesn't do a good job explaining this, so we have included a short reference here. Suppose `T` and `U` are arbitrary types.
>
> ```cpp
> /** 
>  * tl;dr; 
>  * Calls a function to produce a new optional if there is a value; otherwise, returns nothing.
>  *
>  * The function passed to `and_then` takes a non-optional instance of type `T` and returns a `std::optional<U>`.
>  * If the optional has a value, `and_then` applies the function to its value and returns the result.
>  * If the optional doesn't have a value (i.e. it is `std::nullopt`), it returns `std::nullopt`.
>  */
> template <typename U>
> std::optional<U> std::optional<T>::and_then(std::function<std::optional<U>(T)> func);
> 
> /**
>  * tl;dr; 
>  * Applies a function to the stored value if present, wrapping the result in an optional, or returns nothing otherwise.
>  *
>  * The function passed to `transform` takes a non-optional instance of type `T` and returns a non-optional instance of type `U`.
>  * If the optional has a value, `transform` applies the function to its value and returns the result wrapped in an `std::optional<U>`.
>  * If the optional doesn't have a value (i.e. it is `std::nullopt`), it returns `std::nullopt`.
>  */
> template <typename U>
> std::optional<U> std::optional<T>::transform(std::function<U(T)> func);
> 
> /** 
>  * tl;dr; 
>  * Returns the optional itself if it has a value; otherwise, it calls a function to produce a new optional.
>  *
>  * The opposite of `and_then`.
>  * The function passed to `or_else` takes in no arguments and returns a `std::optional<U>`.
>  * If the optional has a value, `or_else` returns it.
>  * If the optional doesn't have a value (i.e. it is `std::nullopt`), `or_else invokes the function and returns the result.
>  */
> template <typename U>
> std::optional<U> std::optional<T>::or_else(std::function<std::optional<U>(T)> func);
> ```
>
> For example, given a `std::optional<T> opt` object, the monadic operations could be invoked as follows:
>
> ```cpp
> opt
>   .and_then([](T value) -> std::optional<U> { return /* ... */; })
>   .transform([](T value) -> U { return /* ... */; });
>   .or_else([]() -> std::optional<U> { return /* ... */; })
> ```
>
> <sup>Note that the `->` notation in the lambda function is a way of explicitly writing out the return type of the function!</sup>
>
> Notice that since each method returns an `std::optional`, you can chain them together. If you are certain that the optional will have a value at the end of the chain, you could call [`.value()`](https://en.cppreference.com/w/cpp/utility/optional/value) to get the value. Otherwise, you could call [`.value_or(fallback)`](https://en.cppreference.com/w/cpp/utility/optional/value_or) to get the result or some other `fallback` value if the optional doesn't have a value.



## 🚀 Submission Instructions

Before you submit the assignment, please fill out this [short feedback form](https://forms.gle/11LreWzsMa5U8VTT9). **Completion of the form is required to receive credit for the assignment.** After filling out the form, please upload the files to Paperless under the correct assignment heading.

Your deliverable should be:

- `main.cpp`

You may resubmit as many times as you'd like before the deadline.
