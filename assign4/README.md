<p align="center">
  <img src="docs/theweatherchannel.png" alt="A logo of The Weather Channel" style="width: 200px; height: auto;" />
</p>

# Assignment 4: Weather Forcast

Due Saturday, November 2nd at 11:59PM

## Overview

<pre>
(\_/)
(•x•) <b>Howdy</b>
(<☕)
</pre>

The Weather Channel learned about your knowledge of functions and lamdas and has requested your help in filtering out weather data! In this assignment you'll make use of standard library algorithms and lambdas to compute statistics on weather data, and filter out weather data based on these statistics.

There is one file you'll work with for this assignment:

- `main.cpp` - You'll write the functions for this assignment here.

To download the starter code for this assignment, please see the instructions for [**Getting Started**](../README.md#getting-started) on the course assignments repository.

## Running your code

To run your code, first you'll need to compile it. Open up a terminal (if you are using VSCode, hit <kbd>Ctrl+\`</kbd> or go to **Terminal > New Terminal** at the top). Then make sure that you are in the `assign4/` directory and run:

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

<!-- Assignment Starts here -->

## Part 1: Implement `Forecast compute_forecast(const std::vector<double>& dailyWeather) {}`

Given a `std::vector<double> dailyWeather` that has the temperature values recorded for a single day, create a `Forecast` object for the day and return it.

We've provided the struct which looks like:

```cpp
struct Forecast {
  double min_temp;
  double max_temp;
  double avg_temp;
};
```

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

## Part 2: Implement `std::vector<Forecast> get_forecasts(const std::vector<std::vector<double> >& weatherData)`!

Now you have have the ability to get the `Forecast` for daily weather, get the `Forecast`s for the multiple days represented by `weatherData`

> [!NOTE]
>
> ```cpp
> std::vector<std::vector<double>> weatherData
> ```
>
> Is a vector of vectors. Where each of the vectors contained within `weatherData` contain the recorded temperature for a day.
> What we really want to do is apply a **transformation** to weatherData. Use standard library method:
>
> ```cpp
> std::transform( InputIt first1, InputIt last1, OutputIt d_first, UnaryOp unary_op )
> ```
>
> Think about what you've already done! How can you leverage that while using `std::transform`?

## Part 3: implement `std::vector<Forecast> get_filtered_data(const std::vector<Forecast>& forecastData)`!

The Weather Channel is doing some statistical analysis on the data you've compiled, and they are interested only in the days where $$(\text{max temperature} - \text{min temperature})$$ > `kMaxTempRequirement` egrees Fahrenheit and an average temperature of **at least** `uAvgTempRequirement`. These values are predefined in the `main.cpp` file, so you don’t need to worry about the nominal values of `kMaxTempRequirement` and `uAvgTempRequirement`, you just need to use them to filter out your forecasts!

> [!NOTE]
>
> We need to **filter** out certain forecasts to meet the requirements of the Weather Channel. Make use of:
>
> ```cpp
> std::remove_if(ForwardIt first, ForwardIt last, UnaryPred p);
> ```
>
> and the **remove-erase idiom**:
>
> ```cpp
> result.erase(std::remove_if(result.begin(), result.end(), filter), result.end());
> ```
>
> ### Understanding the Remove-Erase Idiom
>
> In C++, `std::remove_if` doesn’t directly remove elements from a `std::vector`. Instead, it **rearranges the elements** so that those matching the filter condition are moved to the end of the vector. It then returns an iterator pointing to the "new end" of the container, right after the last element to keep.
>
> `std::erase` is then required to actually **delete** these unwanted elements and resize the vector accordingly. By calling `std::erase` with the iterator returned by `std::remove_if`, we finalize the filtering and ensure only the desired elements remain.
>
> Without using `std::erase`, the unwanted elements remain in the vector (just moved to the end and ignored). Using `std::erase` with the iterator from `std::remove_if` completes the removal, ensuring that only forecasts meeting `kMaxTempRequirement` and `uAvgTempRequirement` remain.
>
> For more on how `std::remove_if` works, you can read about it [here](https://en.cppreference.com/w/cpp/algorithm/remove).

You should return a `std::vector<Forecast>` containing only the `Forecast` structs where the maximum temperature range of the day exceeds `kMaxTempRequirement` and the average is `uAvgTempRequirement`.

To do this, define a lambda function(s) to perform this filtering, and pass it into `std::remove_if`.

## Part 4: implement `std::vector<double> get_shuffled_data(const std::vector<Forcast>& forcastData)`!

Finally, the Weather Channel wants you to **shuffle** your `Forecasts`!

> [!NOTE]
>
> We need to **shuffle** our filtered forecasts to meet the requirements of the Weather Channel. Make use of:
>
> ```cpp
> std::shuffle( RandomIt first, RandomIt last, URBG&& g );
> ```
>
> `std::shuffle` expects a source of randomness`URBG&& g`
>
> You can create a source of randomness, `g` in the following way:
>
> ```cpp
> std::random_device rd;
> std::mt19937 g(rd());
> ```
>
> You can read more about the shuffle method [here](https://en.cppreference.com/w/cpp/algorithm/random_shuffle)

## Part 5: Putting it all together, implement `std::vector<Forecast> run_weather_pipeline(const std::vector<std::vector<double>>& weatherData)`!

In this part of the assignment you need to put everything you've implemented previously together. `run_weather_pipeline` is the API that the Weather Channel is going to call passing in a `std::vector<std::vector<double>>& weatherData`. `weatherData` is vector containing vectors with doubles for multiple readings on each day. This part should be straightforward:

- Get a vector of `Forecast`s
- Filter the vector of `Forecast`s
- Shuffle the vector of `Forecast`s
- return the filtered vector of `Forecast`s

## 🚀 Submission Instructions

Before you submit the assignment, please fill out this [short feedback form](https://forms.gle/84NBtv9v52oQNbYx5). **Completion of the form is required to receive credit for the assignment.** After filling out the form, please upload the files to Paperless under the correct assignment heading.

Your deliverable should be:

- `main.cpp`

You may resubmit as many times as you'd like before the deadline.
