#include "spellcheck.h"

#include <algorithm>
#include <numeric>
#include <vector>

Corpus tokenize(const std::string& input) { 
  return Corpus(); 
}

std::set<Mispelling> spellcheck(const Corpus& source, const Corpus& dictionary) {
  return std::set<Mispelling>();
}

/* Helper methods */

size_t levenshtein(const std::string& a, const std::string& b) {
  size_t sa = a.size(), sb = b.size();
  if (sa == 0)
    return sb;
  if (sb == 0)
    return sa;

  std::vector<size_t> prev(sb + 1), curr(sb + 1);
  for (size_t i = 0; i <= sb; ++i)
    prev[i] = i;

  for (size_t i = 1; i <= sa; ++i) {
    curr[0] = i;
    for (size_t j = 1; j <= sb; ++j) {
      size_t cost = (a[i - 1] == b[j - 1]) ? 0 : 1;
      curr[j] = std::min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost);
    }
    prev.swap(curr);
  }

  return prev[sb];
}

bool operator<(const Token& a, const Token& b) {
  return std::tie(a.offset, a.content) < std::tie(b.offset, b.content);
}

bool operator<(const Mispelling& a, const Mispelling& b) { return a.token < b.token; }