/*
 * CS106L Assignment 4: Weather Forecast
 * Created by Haven Whitney with modifications by Fabio Ibanez & Jacob Roberts-Baca.
 */

/* ========================================================================= *
 * Don't worry about anything beyond this point.                             *
 * (unless you are really curious and want to!)                              *
 * ========================================================================= */

#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

const static std::string kInputFile = "autograder/data.txt";
const static std::string kOutputFile = "autograder/student.txt";

int run_autograder() {
  auto run_program = [](std::string program, std::initializer_list<std::string> args,
                        bool silent = false) {
    std::stringstream ss;

    ss << program;
    for (const auto& arg : args) {
      ss << ' ' << arg;
    }

    if (silent) {
#ifdef _WIN32
      ss << " >nul 2>&1";
#else
      ss << " >/dev/null 2>&1";
#endif
    }

    std::cout.flush();
    return system(ss.str().c_str());
  };

  std::string python;
  for (const auto& option : {"python", "python3", "/usr/bin/python3", "/usr/bin/python"}) {
    if (run_program(option, {"--version"}, true) == 0) {
      python = option;
      break;
    }
  }

  if (python.empty()) {
    std::cerr << "Python was not found on your system. Please install Python and "
                 "try again."
              << "\n";
    std::exit(1);
  }

  return run_program(python, {"autograder/autograder.py"});
}

int main() {
  std::vector<std::vector<double>> weatherData;
  std::ifstream file(kInputFile);

  if (!file.is_open()) {
    std::cerr << "Could not open file: " << kInputFile << std::endl;
    return 1;
  }

  std::string line;
  while (std::getline(file, line)) {
    std::istringstream iss(line);
    std::vector<double> row;
    double value;
    while (iss >> value) {
      row.push_back(value);
    }
    weatherData.push_back(row);
  }

  auto forecasts = run_weather_pipeline(weatherData);

  std::ofstream out(kOutputFile);

  if (!out.is_open()) {
    std::cerr << "Could not open file: " << kOutputFile << std::endl;
    return 1;
  }

  for (const auto& forecast : forecasts) {
    out << forecast.min_temp << ' ' << forecast.max_temp << ' ' << forecast.avg_temp << '\n';
  }

  out.flush();

  /* #### Please don't change this line! #### */
  return run_autograder();
}