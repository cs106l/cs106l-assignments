# Assignment 1: SimpleEnroll

Due Monday, January 27th, at 11:59PM

## Overview

It’s that time of the quarter again; time to use SimpleEnroll 🤗 Wootwoot.
One thing everyone realizes in their Stanford career at one point is that they
have to eventually graduate — and so enrolling in classes becomes a strategic
endeavor to maximize the XP towards graduation, while also being able to sleep
more than 4 hours a night!

In this hopefully short assignment, we’re going to use data from the
ExploreCourses API to figure out which CS classes on ExploreCourses are
offered this year, and which are not! We’ll be taking advantage of streams, while also exercising initialization and references in C++. Lets jump in ʕ•́ᴥ•̀ʔっ

There are only two files you should need to care about:

* `main.cpp`: All your code goes here 😀!
* `utils.cpp`: Contains some utility functions. You'll use functions defined in this file, but you don't otherwise need to modify it.

## Running your code

To run your code, first you'll need to compile it. Open up a terminal (if you are using VSCode, hit <kbd>Ctrl+\`</kbd> or go to **Terminal > New Terminal** at the top). Then make sure that you are in the `assign1/` directory and run:

```sh
g++ -std=c++20 main.cpp -o main
```

Assuming that your code compiles without any compiler errors, you can now do:

```sh
./main
```

which will actually run the `main` function in `main.cpp`. This will execute your code and then run an autograder that will check that your code is correct.

As you are following the instructions below, we recommend intermittently compiling/testing with the autograder as a way to make sure you're on the right track!

> [!NOTE]  
> ### Note for Windows
> On Windows, you may need to compile your code using
> ```sh
> g++ -static-libstdc++ -std=c++20 main.cpp -o main
> ```
> in order to see output. Also, the output executable may be called `main.exe`, in which case you'll run your code with:
> ```sh
> ./main.exe
> ```

## Part 0: Read the code and fill in the `Course` struct

1. In this assignment, we'll be using the `Course` struct to represent records pulled from ExploreCourses in C++. Take a look at the (incomplete) definition of the `Course` struct in `main.cpp` and fill in the field definitions. Ultimately, we'll be using streams to generate `Course`s ---  remember what types streams deal with?

2. Take a look at the `main` function in `main.cpp`, and take special notice of how `courses` is passed into `parse_csv`, `write_courses_offered`,
and `write_courses_not_offered`. Think about what these functions are doing. Do you need to change anything in the function definition? Spoiler, you do.

## Part 1: `parse_csv`

Check out `courses.csv`, it is a CSV file, with three columns: Title, Number of
Units, and Quarter. Implement `parse_csv` so that, for each line in the csv file, it creates a struct `Course` containing the Title, Number of Units, and Quarter for that line.

A couple of things you need to think about:
1. How are you going to read in `courses.csv`? Muahahaha, perhaps a
stream 😏?
2. How will you get each line in the file?

### Hints

1. Take a look at the `split` function we provide in `utils.cpp`. It may come in handy!
    * Feel free to check out the implementation of `split` and ask us any questions about it – you
should be able to reason about it since it’s using a `stringstream`.
2. Each **line** is a record! *This is important, so we're saying it again :>)*
3. In CSV files (and specifically in `courses.csv`), the first line is usually a row that defines the column names (a column header row). This line doesn't actually correspond to a `Course`, so you'll need to skip it somehow!

## Part 2: `write_courses_offered`

Ok. Now you have a populated `courses` vector which has all of the records
of the `courses.csv` file neatly stored in a `Course` struct! You find yourself
interested in only the courses that are offered, right? **A course is considered offered if its Quarter field is not the string `“null”`.** In this function, write out to `“student_output/courses_offered.csv”` all the courses that don’t have
`“null”` in the quarter field.

> [!IMPORTANT]  
> When writing out to the CSV file, please follow this format:
> ```
> <Title>,<Number of Units>,<Quarter>
> ```
> Note that there are **no spaces** between the commas! The autograder will not be happy if this format is not followed!
>
> Also, **make sure to write out the column header row** as the first line in the output. This is the same line you had to skip in `courses.csv` for the previous step!

Once `write_courses_offered` has been called, we expect that all of the offered courses (and consequently all the courses you wrote to the output file) will be removed from the `all_courses` vector. **This means that after this
function runs, `all_courses` should ONLY contain courses that are
not offered!** 

One way to do this is to keep track of the courses that are offered perhaps with another vector and delete them from `all_courses`. Just like in Python and many other languages, it is a bad idea to remove elements from a data structure while you are iterating over it, so you'll probably want to do this *after* you have written all offered courses to file.

## Part 3: `write_courses_not_offered`

So you’re curious about courses that aren’t offered... In the
`write_courses_not_offered` function, write out to
`“student_output/courses_not_offered.csv”` the courses in
`unlisted_courses`. Remember since you deleted the courses that are
offered in the previous step, `unlisted_courses` trivially contains ONLY courses that are not offered – lucky you. So this step should look really similar to Part 2 except shorter and a *tiny* bit simpler.

## 🚀 Submission Instructions

After compiling and running, if your autograder looks like this:

![An image showing a terminal window where the autograder has run with all tests passing](docs/autograder.png)

then you have finished the assignment! Woot woot. To submit the assignment, please complete the feedback form [at this link](https://forms.gle/SW3AgM6dKa5Ea2ow6). Once you submit the form, a link to the submission page will show up in the form submission confirmation.

Your deliverable should be:

- `main.cpp`
