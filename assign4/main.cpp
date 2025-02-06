#include <fstream>
#include <iostream>
#include <iterator>
#include <optional>
#include <string>

#include "spellcheck.h"

class StyleGuard {
public:
  StyleGuard(const std::string& prefix, const std::string& suffix) : suffix{suffix} {
    if (stylingEnabled)
      std::cout << prefix;
  }

  ~StyleGuard() {
    if (stylingEnabled)
      std::cout << suffix;
  }

  static void enabled(bool v) { stylingEnabled = v; }

  static StyleGuard highlight() { return StyleGuard("\033[1;33m", "\033[0m"); }

private:
  static bool stylingEnabled;
  std::string suffix;
};

bool StyleGuard::stylingEnabled = true;

std::string read_stream(std::istream& is) {
  std::istream_iterator<char> begin(is), end;
  return std::string(begin, end);
}

void print_output(const std::string& source, const std::set<Mispelling>& mispellings) {
  std::string_view sv(source);
  size_t last_ofs = 0;
  for (const auto& mispelling : mispellings) {
    // Print text before the mispelling
    std::cout << sv.substr(last_ofs, mispelling.token.src_offset - last_ofs);

    {
      StyleGuard::highlight();
      std::cout << sv.substr(mispelling.token.src_offset, mispelling.token.src_length);
      last_ofs = mispelling.token.src_offset + mispelling.token.src_length;
    }
  }

  std::cout << sv.substr(last_ofs) << "\n\n";

  for (const auto& mispelling : mispellings) {
    {
      StyleGuard::highlight();
      std::cout << sv.substr(mispelling.token.src_offset, mispelling.token.src_length);
    }

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

int main(int argc, char** argv) {
  if (argc == 1) {
    std::cerr << "No args passed" << std::endl;
    return EXIT_FAILURE;
  }

  bool read_stdin = false;
  std::string input;
  std::string dictionary_file = "words.txt";

  for (int i = 1; i < argc; ++i) {
    std::string arg = argv[i];
    if (arg == "-d" && i + 1 < argc) {
      dictionary_file = argv[++i];
    } else if (arg == "--unstyled") {
      StyleGuard::enabled(false);
    } else if (arg == "-i") {
      read_stdin = true;
    } else {
      input += argv[i];
    }
  }

  if (read_stdin)
    input += read_stream(std::cin);

  std::ifstream dict_stream(dictionary_file);
  if (!dict_stream.is_open()) {
    std::cerr << "Failed to open dict file '" << dictionary_file << "'" << std::endl;
    return EXIT_FAILURE;
  }

  Corpus dictionary = tokenize(read_stream(dict_stream));
  Corpus source = tokenize(input);

  std::set<Mispelling> mispellings = spellcheck(source, dictionary);
  print_output(input, mispellings);

  return 0;
}