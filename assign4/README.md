<p align="center">
  <img src="docs/theweatherchannel.png" alt="A logo of the weather channel" />
</p>

# Assignment 4: Weather Forcast

Due Friday, November 1st at 11:59PM

## Overview

<pre>
(\_/)
(•x•) <b>Howdy</b>
(<☕)
</pre>

Now that we've learned about classes, it’s time for you to make your own! Have fun with this, let the creative juices flow. Your class can represent anything, and feel free to make more than one if you'd like. There are some requirements though. As long as you meet these requirements, you’ll get credit for this assignment! 🙂

There is one file you'll work with for this assignment:

- `main.cpp` - You'll write the functions for this assignment here.

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
> g++ -static-libstdc++ -std=c++20 main.cpp class.cpp -o main
> ```
>
> in order to see output. Also, the output executable may be called `main.exe`, in which case you'll run your code with:
>
> ```sh
> ./main.exe
> ```

<!-- Assignment Starts here -->

## Part 1: Making a `Forecast` Struct!

We need a way to keep track of the weather forcasts we're going to make at the daily granularity. Define a `struct` that contains
information like `min`, `average`, and `max` temperature.

It should look something like this:

```cpp
struct Forecast {
  double min_temp;
  double max_temp;
  double avg_temp;
};
```

## Part 2: Implement `Forecast compute_forecast(const std::vector<double>& dailyWeather) {}`

Given a `std::vector<double> dailyWeather` that has the temperature values recorded for a single day, create a `Forecast` object for the day and return it.

> [!NOTE]
>
> We need to get the `min`, `average`, and `max`, please make use of the
> standard library functions:
>
> ```cpp
> std::min_element( ForwardIt first, ForwardIt last );
> ```
>
> ```cpp
> std::accumulate(InputIt first, InputIt last, T init)
> ```
>
> ```cpp
> std::max_element( ForwardIt first, ForwardIt last );
> ```
>
> Think about what the accumulate functionn does, you can read more about it [here](https://en.cppreference.com/w/cpp/algorithm/accumulate)

Once you find the right information construct a `Forecast` struct and then return it!

Make sure to keep in mind the types that the above standard library functions return!

## Part 3: Implement `std::vector<Forecast> get_forecasts(const std::vector<std::vector<double> >& weatherData)`!

Now you have have the ability to get the `Forecast` for daily weather, get the `Forecast`s for the multiple days represented by `weatherData`

> [!NOTE]
>
> ```cpp
> std::vector<std::vector<double>> weatherData
> ```
>
> Is a vector of vectors. Where each of the vectors contained within `weatherData` contain the recorded temperature for a day.

Think about what you've already done! How can you leverage that?

## Part 4: implement `std::vector<Forceast> get_filtered_data(const std::vector<Forcast>& forecastData)`!

The weather channel is doing some statistical analysis on the data you've compiled, they are interested only in the days with a **maximum of `kMinTempRequirement` degrees Farenheit**, and an **average temperature of `uAvgTempRequirement`**. These values are predefined in the `main.cpp` file, so you don't need to worry about the nominal values of `kMinTempRequirement` and `uAvgTempRequirement`, you just need to use them to filter out your forcasts!

TODO: Continue writing

## 🚀 Submission Instructions

Before you submit the assignment, please fill out this [short feedback form](TODO: INSERT LINK). **Completion of the form is required to receive credit for the assignment.** After filling out the form, please upload the files to Paperless under the correct assignment heading.

Your deliverable should be:

- `main.cpp`

You may resubmit as many times as you'd like before the deadline.
