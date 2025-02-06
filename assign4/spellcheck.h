#pragma once

#include <string>
#include <set>

struct Token {
  size_t src_offset;
  size_t src_length;
  std::string content;
};

struct Mispelling {
  Token token;
  std::set<std::string> suggestions;
};

using Corpus = std::set<Token>;

Corpus tokenize(const std::string& input);
std::set<Mispelling> spellcheck(const Corpus& source, const Corpus& dictionary);

/* Helper methods */

size_t levenshtein(const std::string&, const std::string&);
bool operator<(const Token&, const Token&);
bool operator<(const Mispelling&, const Mispelling&);

