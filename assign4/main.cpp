/*
 * CS106L Assignment 4: Weather Forecast
 * Created by Haven Whitney with modifications by Fabio Ibanez & Jacob Roberts-Baca.
 */

#include <algorithm>
#include <random>
#include <vector>

/* #### Please don't change this line! #### */
int run_autograder();
const std::string STUDENT_OUTPUT = "autograder/student_output.txt";

// TODO: change these values
double kMaxTempRequirement = /* TODO */ 5;
double uAvgTempRequirement = /* TODO */ 5;

struct Forcast {
  // STUDENT TODO 1: Define a struct that holds min, max, average
};


Forcast compute_forcast(const std::vector<double>& dailyWeather) {
  // STUDENT TODO 2: return a forcast for the daily weather that is passed in.
}


std::vector<Forcast> get_forcasts(const std::vector<std::vector<double> >& weatherData) {
  /* 
   * STUDENT TODO 3: returns a vector of Forcast structs for the weatherData which contains std::vector<double>
   * which contain values for the weather on that day.
  */
}


std::vector<Forcast> get_filtered_data(const std::vector<Forcast>& forcastData) {
  // STUDENT TODO 4: return a vector with Forcasts filtered for days with specific weather. 
}


std::vector<double> get_shuffled_data(const std::vector<Forcast>& forcastData) {
  // STUDENT TODO 5: Make use of a standard library algorithm to shuffle the data!
}


int main() {
  // STUDENT TODO: Put it all together and call your functions to create a shuffled vector!

  /* #### Please don't change this line! #### */
  return run_autograder();
}

/* #### Please don't change this line! #### */
// JACOB TODO: assumes there is a utils.hpp for autograder
#include "utils.hpp"