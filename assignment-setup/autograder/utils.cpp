#include <iostream>
#include <sstream>
#include <string>
#include <fstream>
#include <vector>


int
run_autograder()
{
  auto run_program = [](std::string program,
                        std::initializer_list<std::string> args,
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
  for (const auto& option :
       { "python", "python3", "/usr/bin/python3", "/usr/bin/python" }) {
    if (run_program(option, { "--version" }, true) == 0) {
      python = option;
      break;
    }
  }

  if (python.empty()) {
    std::cerr
      << "Python was not found on your system. Please install Python and "
         "try again."
      << "\n";
    std::exit(1);
  }

  return run_program(python, { "autograder/autograder.py" });
}

std::vector<std::string> split(std::string s, char delim) {
    std::vector<std::string> return_vec;
    std::stringstream ss(s);
    std::string token;
    while (getline(ss, token, delim)) {
      return_vec.push_back(token);
    }
    return return_vec;
}

std::vector<std::string> read_lines(std::string filename) {
    std::vector<std::string> lines;
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Could not open file " << filename << "\n";
        std::exit(1);
    }

    std::string line;
    while (std::getline(file, line)) lines.push_back(line);
    return lines;
}