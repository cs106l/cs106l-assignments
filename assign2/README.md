<p align="center">
  <img src="docs/marriage_pact.png" alt="Marriage Pact Logo" />
</p>

# Assignment 2: Marriage Pact

Due Friday, January 31st at 11:59PM

## Overview

Happy assignment 2! This is meant to be a very short and sweet bit of practice to get you started working with the STL’s containers and pointers.

These are the files you need to care about:

- `main.cpp`: All your code goes here 😀!
- `short_answer.txt`: Short answer responses go here 📝!

To download the starter code for this assignment, please see the instructions for [**Getting Started**](../README.md#getting-started) on the course assignments repository.

## Running your code

To run your code, first you'll need to compile it. Open up a terminal (if you are using VSCode, hit <kbd>Ctrl+\`</kbd> or go to **Terminal > New Terminal** at the top). Then make sure that you are in the `assign2/` directory and run:

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

## Part 0: Setup

Welcome to the Marriage Pact! Before you begin, we'll need to know your name. Please change the constant `kYourName` at the top of `main.cpp` from `"STUDENT TODO"` to your full name (with a space between first and last).

## Part 1: Get all applicants

You’ve been waiting for days to get your Marriage Pact initials this year, and they’ve finally arrived in your inbox! This year, they’re implementing a new rule: your match MUST share your own initials to be eligible. However, even after talking about it for hours with your friends, you have no idea who your match could be! There are thousands of students on campus, and you can’t just go through the whole roster by hand to draft up a list of your potential soulmates. Fortunately enough for you, you’re in CS106L, and you remember that C++ has a pretty quick method of going through collected, similar information – containers!

We’ve included a `.txt` file of all of the (fictional) students who signed up for The Marriage Pact this year (`students.txt`). Each line includes the first and last name of the student. You will first write the function `get_applicants`:

> [!IMPORTANT]
>
> ### `get_applicants`
>
> From the `.txt` file, parse all of the names into a set. Each line contained in the file named `filename` is a single applicant's name. In your implementation, you are free to choose between an ordered (`std::set`) and unordered set (`std::unordered_set`) as you wish! If you do choose to use an unordered set, please change the relevant function definitions!

Additionally, please answer the following short answer question in `short_answer.txt`:

> [!IMPORTANT]
>
> ### `short_answer.txt`
>
> **Q1:** It is your choice to use either an ordered or unordered set. In a few sentences, what are some of the tradeoffs between the two? Additionally, please give an example (that has not been shown in lecture) of a valid hash function that could be used to hash student names for an unordered set.

> [!NOTE]
> All names appearing in this assignment are fictitious. Any resemblance to real persons, living or dead, is purely coincidental.

## Part 2: Find matches

Great detective work! Now that you’ve narrowed down your list of potential soulmates, it’s time to put it to the test. After a long day of acapella and consulting club meetings, you return to your dorm to learn from your roommate that there is a mixer for Marriage Pact matches at Main Quad that night! Your best chance of finding true love is imminent — if only you can get out of your Ultimate Frisbee practice. Quickly, you decide to interview everyone who shares your initials at the mixer, and you get to work coding up a function that will compile the order for you automatically.

For this section, you will write the functions `find_matches` and `get_match`:

> [!IMPORTANT]
>
> ### `find_matches`
>
> From the set `students` (generated in the previous part), take all names that share initials with the parameter `name` and place pointers to them in a new `std::queue`.
>
> - If you’re having trouble figuring out how to iterate through a set, it could be helpful to look back over [Thursday’s lecture on iterators and pointers](https://office365stanford-my.sharepoint.com/:p:/g/personal/jtrb_stanford_edu/EbOKUV784rBHrO3JIhUSAUgBvuIGn5rSU8h3xbq-Q1JFfQ?e=BlZwa7).
> - You will need to be familiar with the operations of a `std::queue` for this part. Take a look at cppreference's documentation [here](https://en.cppreference.com/w/cpp/container/queue).
> - Hint: It might help to define a helper function that computes the initials of some student's name. Then you can use that helper function to compare the initials of `name` with the initials of each name in `students`.

From here please implement the function `get_match` to find your “one true match.”:

> [!IMPORTANT]
>
> ### `get_match`
>
> Gets your “one true match” from the queue of all possible matches. This can be determined as you see fit; choose some method of acquiring one student from the queue, ideally something with a bit more thought than a single `pop()`, but it doesn’t have to be particularly complicated! Consider random values or other methods of selection.
>
> If your initials have no matches in the dataset, print `“NO MATCHES FOUND.”` Better luck next year 😢

Afterwards, answer the following question in `short_answer.txt`:

> [!IMPORTANT]
>
> ### `short_answer.txt`
>
> **Q2:** Note that we are saving pointers to names in the queue, not names themselves. Why might this be desired in this problem? What happens if the original set where the names are stored goes out of scope and the pointers are referenced?

## 🚀 Submission Instructions

Before you submit the assignment, please fill out this [short feedback form](https://forms.gle/8sPwrAsMKMspPShc8). **Completion of the form is required to receive credit for the assignment.** After filling out the form, please upload the files to Paperless under the correct assignment heading.

Your deliverable should be:

- `main.cpp`
- `short_answer.txt`

You may resubmit as many times as you'd like before the deadline.
