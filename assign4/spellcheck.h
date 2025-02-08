#pragma once

#include <set>
#include <string>
#include <unordered_set>

struct Token {

  std::string content;
  size_t src_offset;

  template <typename It>
  Token(const std::string& source, It begin, It end)
      : src_offset{static_cast<std::size_t>(std::distance(source.begin(), begin))},
        content{std::string(begin, end)} {
    clean(source);
  }

private:
  void clean(const std::string& source);
};

struct Mispelling {
  Token token;
  std::set<std::string> suggestions;
};

using Corpus = std::set<Token>;
using Dictionary = std::unordered_set<std::string>;

Corpus tokenize(const std::string& input);
std::set<Mispelling> spellcheck(const Corpus& source, const Dictionary& dictionary);

/* Helper methods */

size_t levenshtein(const std::string&, const std::string&);
bool operator<(const Token&, const Token&);
bool operator<(const Mispelling&, const Mispelling&);