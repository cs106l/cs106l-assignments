# Assignment 0: Enviornment Setup!

Due Friday, January 17th at 11:59PM

## Overview

Welcome to CS106L! This assignment will get you setup for the rest of the quarter so that hopefully setup for the rest of the assignments is simple and smooth.

## Part 1: Checking your Python installation and installing if necessary

### Part 1.1: Checking your Python installation

The autograder for CS106L uses Python and requires version 3.8 or higher. To check your Python version you can run the following in your terminal:

If you're on Linux or Mac:

```sh
python3 --version
```

If you're on Windows:

```sh
python --version
```

if you get a version that is 3.8 or higher, then you're good, **you can ignore Part 1.2**, otherwise please take a look at Part 1.2.

### Part 1.2: Installing Python (if you don't already have it installed)

#### Mac

<ol>
  <li>
    Check if you have Homebrew by running 
    <pre lang="sh">brew --version</pre>
    If you get something like
    <pre lang="sh">
brew --version
Homebrew 4.2.21</pre>
    then <b>skip step 2 and go to step 3.</b> If you get anything else that looks sus then proceed to step 2!
  </li>
  <li>
    Run this command:
    <pre lang="sh">/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"</pre>
    which is going to download Homebrew🍺 which is a package manager. Woot woot.
  </li>
  <li>
    Run the following command:
    <pre lang="sh">brew install python</pre>
    which is to install a recent-enough version of Python.
  <li>
    Restart your terminal and verify that everything worked by running the following command:
    <pre lang="sh">python3 --version</pre>
  </li>
</ol>

#### Windows

Please follow the instructions [here](https://learn.microsoft.com/
en-us/windows/python/beginners#install-python) under the "Install Python" section and this should suffice.

#### Linux

These instructions are for Debian-based distributions, like Ubuntu. Tested on Ubuntu 20.04 LTS.

<ol>
  <li>
    Update the Ubuntu package lists by running
    <pre lang=>"sh"sudo apt-get update </pre>
  </li>
  <li>
    Install python
    <pre lang="sh">sudo apt-get install python3</pre>
  </li>
  <li>
    Restart your terminal and verify that the installation worked by running the following command:
    <pre lang="sh">python3 --version</pre>
  </li>
</ol>

## Part 2: Setup VSCode

We recommend that you use VSCode to write C++ code for this class. Below are instructions to setup VSCode along withe the GCC compiler for your machine.

### Mac

#### Step One: Installing VSCode

Go to [this link](https://code.visualstudio.com/docs/setup/mac)
and download Visual Studio Code for Mac. Follow the instructions on this webpage under the
section **Installation**.

Inside VSCode, head to the extensions tab <img src="docs/vscode-extensions.png" display="inline" height="20px"></img> and search for **C/C++**. Click on the **C/C++** extension, and then click **Install**.

<b> 🥳 At this point you should successfully have VSCode on your Mac 👏 </b>

#### Step Two: Installing a C++ Compiler

<ol>
  <li>
    Run the following command (you should already have brew installed from Part 1!):
    <pre lang="sh">brew install gcc</pre>
    which is going to install the compiler (GCC).
  </li>
  <li>
    Make note of which GCC version Homebrew installs. In most cases, this will be <code>g++-14</code>. 
    By default, the <code>g++</code> command on Mac is an alias to the built-in <code>clang</code> compiler. We can fix this by running <pre lang="sh">echo 'alias g++="g++-14"' >> ~/.zshrc</pre> to make <code>g++</code> point to the version of GCC we just installed. Change <code>g++-14</code> in the above command to whichever version of GCC you installed.
  <li>
    Restart your terminal and verify that everything worked by running the following command:
    <pre lang="sh">g++ --version</pre>
  </li>
</ol>

### Windows

#### Step One: Installing VSCode

Go to [this link](https://code.visualstudio.com/docs/setup/windows)
and download Visual Studio Code for Windows. Follow the instructions on this webpage under the
section **Installation**.

Inside VSCode, head to the extensions tab <img src="docs/vscode-extensions.png" display="inline" height="20px"></img> and search for **C/C++**. Click on the **C/C++** extension, and then click **Install**.

<b> 🥳 At this point you should successfully have VSCode on your PC 👏 </b>

#### Step Two: Installing a C++ Compiler

1. Follow the instructions at [this link](https://code.visualstudio.com/docs/cpp/config-mingw) \* You should be doing the instructions under **Installing the
   MinGW-w64 toolchain.**

2. After fully following the instructions under **Installing the
   MinGW-w64 toolchain** you should now be able to verify
   everything worked by running the following command:

```sh
g++ --version
```

### Linux

These instructions are for Debian-based distributions, like Ubuntu. Tested on Ubuntu 20.04 LTS.

#### Step One: Installing VSCode

Go to [this link](https://code.visualstudio.com/docs/setup/linux)
and download Visual Studio Code for Linux. Follow the instructions on this webpage under the section **Installation**.

Inside VSCode, head to the extensions tab <img src="docs/vscode-extensions.png" display="inline" height="20px"></img> and search for **C/C++**. Click on the **C/C++** extension, and then click **Install**.

<b> 🥳 At this point you should successfully have VSCode on your Linux machine 👏 </b>

#### Step Two: Installing a C++ Compiler

<ol>
  <li>In a terminal, update the Ubuntu package lists by running <pre lang="sh">sudo apt-get update</pre></li>
  <li>Next install the G++ compiler: <pre lang="sh">sudo apt-get install g++-10</pre></li>
  <li>By default, the system version of G++ will be used. To change it to the version you just installed, you can configure Linux to use G++ version 10 or a higher version installed like so: <pre lang="sh">sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 10</pre></li>
  <li>Restart your terminal and verify that GCC was installed correctly. You must have a GCC version of 10 or higher: <pre lang="sh">g++ --version</pre></li>
</ol>

## Getting setup on Git + cloning the class code!

If you successfully installed VSCode, then you should already have this. You can check by running `git --version` in a terminal.

### Download the starter code

Open up a terminal (if you are using VSCode, hit <kbd>Ctrl+\`</kbd> or go to **Terminal > New Terminal** at the top) and run the following command:

```sh
git clone https://github.com/cs106l/cs106l-assignments.git
```

which will download the starter code into a folder `cs106l-assignments`. If you are using VSCode, you can then open up a VSCode workspace dedicated to CS106L:

```sh
cd cs106l-assignments && code .
```

and you are ready to go!

### Fetching assignments

As we update existing assignments and release new ones, we will push updates to this repository. To fetch a new assignment, open up a terminal to your `cs106l-assignments` directory and run

```sh
git pull origin main
```

You should now have the latest starter code!

# Testing your setup!

To run your code, first you'll need to compile it. Open up a terminal (if you are using VSCode, hit <kbd>Ctrl+\`</kbd> or go to **Terminal > New Terminal** at the top). Then make sure that you are in the `assign0/` directory and run:

```sh
g++ -std=c++20 main.cpp -o main
```

Assuming that your code compiles without any compiler errors, you can now do:

```sh
./main
```

which will actually run the `main` function in `main.cpp`. This will execute your code and then run an autograder that will check that your installation is correct.

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

## 🚀 Submission Instructions

After compiling and running, if your autograder looks like this:

![An image showing a terminal window where the autograder has run with all tests passing](docs/autograder.png)

then you have finished the assignment! Woot woot. To submit the assignment, please complete the feedback form [at this link](https://forms.gle/UfSDVYpbg472ZXkJ8). Once you submit the form, a link to the submission page will show up in the form submission confirmation.
