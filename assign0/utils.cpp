/*
 * CS106L Assignment 0: Environment Setup!
 * Created by Fabio Ibanez
 */


/* ========================================================================= *
 * Don't worry about anything beyond this point.                             *
 * (unless you are really curious and want to!)                              *
 * ========================================================================= */

int run_autograder() {
  auto run_program = [](std::string program, std::initializer_list<std::string> args) {
    std::stringstream ss;

    ss << program;
    for (const auto& arg : args) {
      ss << ' ' << arg;
    }

    std::cout.flush();
    return system(ss.str().c_str());
  };

  std::string python;
  for (const auto& option : {"python", "python3", "/usr/bin/python3", "/usr/bin/python"}) {
    if (run_program(option, {"--version"}) == 0) {
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