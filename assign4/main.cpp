/*
 * CS106L Assignment 4: Weather Forecast
 * Created by Haven Whitney with modifications by Fabio Ibanez & Jacob Roberts-Baca.
 */

#include <algorithm>
#include <random>
#include <vector>
#include <iostream>


/* #### Please feel free to use these values, but don't change them! #### */
double kMaxTempRequirement = 5;
double uAvgTempRequirement = 60;

std::random_device rd;
std::mt19937 g(rd());

struct Forecast {
  double min_temp;
  double max_temp;
  double avg_temp;
};

Forecast compute_forecast(const std::vector<double>& dailyWeather) {
  // STUDENT TODO 1: return a forecast for the daily weather that is passed in.
  if(dailyWeather.empty()) {
    return Forecast{0.0, 0.0, 0.0}; 
  }
  double min = *std::min_element(dailyWeather.begin(), dailyWeather.end());
  double max = *std::max_element(dailyWeather.begin(), dailyWeather.end());
  double sum = std::accumulate(dailyWeather.begin(), dailyWeather.end(), 0.0);
  double avg = sum / dailyWeather.size();
  return Forecast{min, max, avg};
}

std::vector<Forecast> get_forecasts(const std::vector<std::vector<double>>& weatherData) {
  /*
   * STUDENT TODO 2: returns a vector of Forecast structs for the weatherData which contains
   * std::vector<double> which contain values for the weather on that day.
   */
    std::vector<Forecast> forecasts;
    
    // 使用 std::transform 对每一天的气温数据应用 compute_forecast
    std::transform(weatherData.begin(), weatherData.end(), std::back_inserter(forecasts), compute_forecast);
    return forecasts;
}

std::vector<Forecast> get_filtered_data(const std::vector<Forecast>& forecastData) {
  // STUDENT TODO 3: return a vector with Forecasts filtered for days with specific weather.
    std::vector<Forecast> filteredData = forecastData;
    double kMax = kMaxTempRequirement;
    double uAvg = uAvgTempRequirement;

    // 使用 std::remove_if 和 lambda 函数进行过滤
    filteredData.erase(
        std::remove_if(filteredData.begin(), filteredData.end(), [kMax, uAvg](const Forecast& forecast) {
            // 过滤条件：最大温度和最小温度差大于 kMaxTempRequirement，且平均温度大于等于 uAvgTempRequirement
            return (forecast.max_temp - forecast.min_temp) <= kMax || forecast.avg_temp < uAvg;
        }),
        filteredData.end()  // 删除符合条件的元素
    );

    return filteredData;
}


std::vector<Forecast> get_shuffled_data(const std::vector<Forecast>& forecastData) {
  // STUDENT TODO 4: Make use of a standard library algorithm to shuffle the data!
  std::vector<Forecast> shuffledData = forecastData;
  std::shuffle(shuffledData.begin(), shuffledData.end(), g);
  return shuffledData;
}

std::vector<Forecast> run_weather_pipeline(const std::vector<std::vector<double>>& weatherData) {
  // STUDENT TODO 5: Put your functions together to run the weather pipeline!
  std::vector<Forecast> forecasts = get_forecasts(weatherData);
  std::vector<Forecast> filted = get_filtered_data(forecasts);
  std::vector<Forecast> shuffled = get_shuffled_data(filted);
  return shuffled;
}

/* #### Please don't change this line! #### */
#include "utils.cpp"