#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

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

  /* #### Assignment Specific Operations #### */
  auto allMatches = get_applicants("students.txt");
  auto studentMatches = find_matches(kYourName, allMatches);
  auto match = get_match(studentMatches);

  std::fstream matchFile("autograder/student_output/match.txt");
  std::fstream setFile("autograder/student_output/set.txt");

  matchFile << kYourName << '\n' << "Your match is: " << match << '\n';
  for (const auto& student : allMatches) {
    setFile << student << '\n';
  }

  // Flush streams so that the Python autograder is guaranteed to see their
  // changes
  matchFile.flush();
  setFile.flush();
  /* #### End of Assignment Specific Operations #### */

  return run_program(python, { "autograder/autograder.py" });
}

int
main()
{
  return run_autograder();
}