/* ========================================================================= *
 * Don't worry about anything beyond this point.                             *
 * (unless you are really curious and want to!)                              *
 * ========================================================================= */

#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

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

namespace ansi {

const int style_idx = std::ios_base::xalloc();

template <class CharT, class Traits>
constexpr std::basic_ostream<CharT, Traits>& styled(std::basic_ostream<CharT, Traits>& os) {
  os.iword(style_idx) = 1;
  return os;
}

template <class CharT, class Traits>
constexpr std::basic_ostream<CharT, Traits>& unstyled(std::basic_ostream<CharT, Traits>& os) {
  os.iword(style_idx) = 0;
  return os;
}

#define make_style(NAME, VALUE)                                                                    \
  template <class CharT, class Traits>                                                             \
  constexpr std::basic_ostream<CharT, Traits>& NAME(std::basic_ostream<CharT, Traits>& os) {       \
    if (os.iword(style_idx) > 0)                                                                   \
      os << VALUE;                                                                                 \
    return os;                                                                                     \
  }

make_style(reset, "\033[0m\e[0m");
make_style(fg_red, "\033[31m");
make_style(fg_lightred, "\033[91m");
make_style(fg_green, "\033[92m");
make_style(fg_gray, "\033[90m");
make_style(bg_yellow, "\e[43m");

} // namespace ansi

std::string read_stream(std::istream& is) {
  std::istreambuf_iterator<char> begin(is), end;
  return std::string(begin, end);
}

struct TimerResult {
  std::string name;
  size_t trials;
  std::chrono::nanoseconds ns;
};

class TimerSummary {
public:
  TimerSummary() : trial_noun{"trial"}, enabled{false} {}
  void add(const TimerResult& result) { results.push_back(result); }
  void set_trial_noun(const std::string& trial_noun) { this->trial_noun = trial_noun; }

  TimerSummary& operator=(const TimerSummary&) = delete;
  ~TimerSummary() {
    if (!enabled)
      return;

    std::cout << "\n";
    std::cout << ansi::bg_yellow << std::left << std::setw(120) << "Timing Results:" << ansi::reset << '\n';
    std::cout << ansi::fg_gray;
    for (const auto& [name, trials, ns] : results) {
      std::cout << " · " << name << " took ";
      format_time(ns);
      if (trials > 1) {
        std::cout << ", averaging ";
        format_time(ns / trials);
        std::cout << " per " << trial_noun;
      }
      std::cout << " (" << trials << " " << trial_noun;
      if (trials != 1) std::cout << "s";
      std::cout << ")\n";
    }
    std::cout << ansi::reset;
  }

  void enable() { enabled = true; }
  void disable() { enabled = false; }

private:
  bool enabled;
  std::string trial_noun;
  std::vector<TimerResult> results;

  void format_time(const std::chrono::nanoseconds& ns) {
    using namespace std::chrono;

    if (ns < 10us) {
      std::cout << ns.count() << "ns";
    } else if (ns < 1s) {
      std::cout << std::fixed << std::setprecision(2)
                << duration_cast<microseconds>(ns).count() / 1000.0 << "ms" << std::defaultfloat;
    } else {
      std::cout << std::fixed << std::setprecision(3)
                << duration_cast<milliseconds>(ns).count() / 1000.0 << "s" << std::defaultfloat;
    }
  }
};

class Timer {
public:
  Timer(TimerSummary& summary, const std::string& name, size_t trials = 1)
      : summary{summary}, name{name}, trials{trials},
        start{std::chrono::high_resolution_clock::now()}, stopped{false} {}

  ~Timer() {
    stop();
    auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
    summary.add({name, trials, ns});
  }

  Timer& operator=(const Timer&) = delete;

  void set_trials(size_t trials) { this->trials = trials; }

  void stop() {
    if (stopped)
      return;
    stopped = true;
    end = std::chrono::high_resolution_clock::now();
  }

private:
  std::string name;
  size_t trials;
  std::chrono::high_resolution_clock::time_point start;
  std::chrono::high_resolution_clock::time_point end;
  bool stopped;

  TimerSummary& summary;
};
