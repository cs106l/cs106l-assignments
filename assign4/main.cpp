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

make_style(reset, "\033[0m");
make_style(fg_red, "\033[31m");
make_style(fg_lightred, "\033[91m");
make_style(fg_green, "\033[92m");

} // namespace ansi

std::string read_stream(std::istream& is) {
  std::istreambuf_iterator<char> begin(is), end;
  return std::string(begin, end);
}

void print_output(const std::string& source, const std::set<Mispelling>& mispellings) {
  std::string_view sv(source);
  size_t last_ofs = 0;
  for (const auto& mispelling : mispellings) {
    // Print text before the mispelling
    std::cout << sv.substr(last_ofs, mispelling.token.src_offset - last_ofs);

    std::cout << ansi::fg_red << "«";
    std::cout << sv.substr(mispelling.token.src_offset, mispelling.token.content.size());
    std::cout << "»" << ansi::reset;
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

  for (int i = 1; i < argc; ++i) {
    std::string arg = argv[i];
    if (arg == "-d" && i + 1 < argc) {
      dictionary_file = argv[++i];
    } else if (arg == "--unstyled") {
      styled = false;
    } else if (arg == "--stdin") {
      read_stdin = true;
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

  std::string dict_contents = read_stream(dict_stream);
  Corpus dictionary_tokens = tokenize(dict_contents);

  Dictionary dictionary;
  std::for_each(dictionary_tokens.begin(), dictionary_tokens.end(),
                [&](const Token& t) { dictionary.insert(t.content); });

  Corpus source = tokenize(input);
  std::set<Mispelling> mispellings = spellcheck(source, dictionary);
  print_output(input, mispellings);

  if (styled && !dictionary.empty() && mispellings.empty())
    print_success();

  return mispellings.empty() ? 0 : EXIT_FAILURE;
}