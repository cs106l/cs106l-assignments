#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <optional>
#include <ostream>
#include <random>
#include <string>

#include "autograder/utils.hpp"
#include "spellcheck.h"

void print_output(const std::string& source, const std::set<Mispelling>& mispellings) {
  std::string_view sv(source);
  size_t last_ofs = 0;
  for (const auto& mispelling : mispellings) {
    // Print text before the mispelling
    std::cout << sv.substr(last_ofs, mispelling.token.src_offset - last_ofs);

    std::cout << ansi::fg_red << "<<";
    std::cout << sv.substr(mispelling.token.src_offset, mispelling.token.content.size());
    std::cout << ">>" << ansi::reset;
    last_ofs = mispelling.token.src_offset + mispelling.token.content.size();
  }

  std::cout << sv.substr(last_ofs) << "\n\n";

  for (const auto& mispelling : mispellings) {
    std::cout << ansi::fg_red;
    std::cout << sv.substr(mispelling.token.src_offset, mispelling.token.content.size());
    std::cout << ansi::reset;

    std::cout << ": {";

    bool first = true;
    for (const auto& suggestion : mispelling.suggestions) {
      if (!first)
        std::cout << ", ";
      std::cout << suggestion;
      first = false;
    }

    std::cout << "}\n";
  }
}

void print_success() {
  std::vector<std::string> messages = {
      "You're a spelling wizard! If words had a kingdom, you'd rule it.",
      "Are you secretly a dictionary in disguise? Impressive!",
      "If spelling were an Olympic sport, you'd have gold by now.",
      "Your spelling skills are so good, even autocorrect is taking notes.",
      "The spelling bee champions fear you. Rightfully so.",
      "Your grasp of spelling is tighter than a jar lid no one can open.",
      "I checked the dictionary, and your name is under 'spelling genius.'",
      "Shakespeare just sent a 'Well done!' from the beyond.",
      "You spell so well, even Scrabble pieces arrange themselves for you.",
      "Your spelling game is so strong, spellcheck just quit its job."};

  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_int_distribution<size_t> dist(0, messages.size() - 1);

  std::cout << ansi::fg_green << messages[dist(gen)] << ansi::reset << std::endl;
}

int main(int argc, char** argv) {
  if (argc == 1) {
    return run_autograder();
  }

  bool read_stdin = false;
  std::string input;
  std::string dictionary_file = "words.txt";
  bool styled = true;

  TimerSummary summary;
  summary.set_trial_noun("token");

  for (int i = 1; i < argc; ++i) {
    std::string arg = argv[i];
    if (arg == "--dict" && i + 1 < argc) {
      dictionary_file = argv[++i];
    } else if (arg == "--unstyled") {
      styled = false;
    } else if (arg == "--stdin") {
      read_stdin = true;
    } else if (arg == "--profile") {
      summary.enable();
    } else {
      input += argv[i];
    }
  }

  if (styled)
    std::cout << ansi::styled;
  else
    std::cout << ansi::unstyled;

  if (read_stdin)
    input += read_stream(std::cin);

  std::ifstream dict_stream(dictionary_file);
  if (!dict_stream.is_open()) {
    std::cerr << "Failed to open dict file '" << dictionary_file << "'" << std::endl;
    return EXIT_FAILURE;
  }

  std::cout << ansi::fg_gray << "Loading dictionary... ";

  std::string dict_contents = read_stream(dict_stream);

  Timer tokenize_dict_timer { summary, "Tokenizing dictionary" };
  Corpus dictionary_tokens = tokenize(dict_contents);
  tokenize_dict_timer.stop();
  tokenize_dict_timer.set_trials(dictionary_tokens.size());

  Dictionary dictionary;
  std::for_each(dictionary_tokens.begin(), dictionary_tokens.end(),
                [&](const Token& t) { dictionary.insert(t.content); });

  std::cout << "loaded " << dictionary.size() << " unique words." << std::endl;
  std::cout << "Tokenizing input... ";

  Timer tokenize_source_timer { summary, "Tokenizing input"};
  Corpus source = tokenize(input);
  tokenize_source_timer.stop();
  tokenize_source_timer.set_trials(source.size());

  std::cout << "got " << source.size() << " tokens." << ansi::reset << "\n\n";

  Timer spellcheck_timer { summary, "Spellcheck", source.size() };
  std::set<Mispelling> mispellings = spellcheck(source, dictionary);
  spellcheck_timer.stop();

  print_output(input, mispellings);

  if (styled && !dictionary.empty() && mispellings.empty())
    print_success();

  return mispellings.empty() ? 0 : EXIT_FAILURE;
}