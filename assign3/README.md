<p align="center">
  <img src="docs/bjarne.jpg" alt="Bjarne Stroustrup writing the declaration of a class on a whiteboard" />
</p>

# Assignment 3: Make a Class

Due Friday, February 7th at 11:59PM

## Overview

<pre>
(\_/)
(•x•) <b>Howdy</b>
(<☕)
</pre>

Now that we've learned about classes, it’s time for you to make your own! Have fun with this, let the creative juices flow. Your class can represent anything, and feel free to make more than one if you'd like. There are some requirements though. As long as you meet these requirements, you’ll get credit for this assignment! 🙂

There are four files you'll work with for this assignment:

* `class.h` - This is the header file for your class, where the class **declaration** will go.
* `class.cpp` - This is the `.cpp` file for your class, where the class **definition** will go.
* `sandbox.cpp` - You'll construct an instance of your class here.
* `short_answer.txt` - You'll answer a few short answer questions here.

To download the starter code for this assignment, please see the instructions for [**Getting Started**](../README.md#getting-started) on the course assignments repository.

## Running your code

To run your code, first you'll need to compile it. Open up a terminal (if you are using VSCode, hit <kbd>Ctrl+\`</kbd> or go to **Terminal > New Terminal** at the top). Then make sure that you are in the `assign3/` directory and run:

```sh
g++ -std=c++20 main.cpp class.cpp -o main
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
> g++ -static-libstdc++ -std=c++20 main.cpp class.cpp -o main
> ```
>
> in order to see output. Also, the output executable may be called `main.exe`, in which case you'll run your code with:
>
> ```sh
> ./main.exe
> ```

## Part 1: Making your class

Let your creative juices flow! Fill in `class.h` and `class.cpp` to create your own custom class. Please refer to the relevant slides from Tuesday's lecture on classes for more information. Your class can represent pretty much anything you want, as long as it meets the following requirements.

> [!IMPORTANT]
> ### Class Requirements
>
> Your class must:
> 1. Have a custom constructor taking **one or more** parameters.
> 2. Have a default (parameterless) constructor (i.e. constructor overloading).
> 3. Have one or more private member fields (i.e. variables).
> 4. Have one or more private member functions.
>     - Remember, private functions are like what happens underneath the hood of your car! They are a necessary part of the implementation of a class, but shouldn't be exposed in the public interface. Try to think of a private member function that logically makes sense in the context of your class.
> 5. Have **at least one** public getter function for one of the private fields.
>     - E.g. if `int data` is the field, you must have a function called `get_data` or `getData` with the signature <pre lang="cpp">int getData();</pre>
>     - The getter function should also be marked `const`. Refer to Thursday's lecture on `const` correctness if you are unfamiliar!
> 6. Have at least one public setter function for one of the private fields.
>     - E.g. if `int data` is the field, you must have a function called `set_data` or `setData` with the signature <pre lang="cpp">void setData(int value);</pre>

Note that this is the bare minimum to get credit for the assignment. Please feel free to go above and beyond these requirements or create more than one class if you want extra practice!

> [!NOTE]
> For brownie points, you can choose to create a class template instead of a regular class using the `template <typename T>` notation discussed on Thursday's lecture. This is totally optional!
>
> Note that if you do decide to create a class template, you **must remove class.cpp
> from the compilation command.** For example, on Mac/Linux, the compilation
> command will be:
>
> ```sh
> g++ -std=c++20 main.cpp -o main
> ```
> 
> Remember to also swap the includes so that the `.h` file includes the `.cpp`
> file at the end of the file, as discussed in Thursday's lecture.

Now that you've created your class, let's actually use it. **Inside of the `sandbox` function in `sandbox.cpp`, construct an instance of your class!** You can do so however you like (call default constructor, use uniform initialization, etc.).

To see if you did everything correctly, compile and run your code! The autograder will give you feedback on your class and check if it meets the specifications above.

## Part 2: Short answer questions

Please answer the following questions inside `short_answer.txt`. We expect about 2-3 sentences per question.

> [!IMPORTANT]
> `short_answer.txt`
> - **Q1:** What’s const-correctness and why is it important?
> - **Q2:** Is your class const-correct? How do you know?

## 🚀 Submission Instructions

Before you submit the assignment, please fill out this [short feedback form](https://forms.gle/GpYLMocRHsgCfL6k8). **Completion of the form is required to receive credit for the assignment.** After filling out the form, please upload the files to Paperless under the correct assignment heading.

Your deliverable should be:

* `class.h`
* `class.cpp`
* `sandbox.cpp`
* `short_answer.txt`

You may resubmit as many times as you'd like before the deadline.
