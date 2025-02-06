size_t levenshtein(const std::string& a, const std::string& b) {
  size_t sa = a.size(), sb = b.size();
  if (sa == 0)
    return sb;
  if (sb == 0)
    return sa;

  if (std::abs(int(sa) - int(sb)) > 1) // Early exit if length difference > 1
    return 2;

  std::vector<size_t> prev(sb + 1), curr(sb + 1);
  for (size_t i = 0; i <= sb; ++i)
    prev[i] = i;

  for (size_t i = 1; i <= sa; ++i) {
    curr[0] = i;
    size_t min_edit = i;
    for (size_t j = 1; j <= sb; ++j) {
      size_t cost = (a[i - 1] == b[j - 1]) ? 0 : 1;
      curr[j] = std::min({prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost});
      min_edit = std::min(min_edit, curr[j]);
    }

    if (min_edit >= 2)
      return 2;
    prev.swap(curr);
  }

  return prev[sb];
}

bool operator<(const Token& a, const Token& b) {
  return std::tie(a.src_offset, a.content) < std::tie(b.src_offset, b.content);
}

bool operator<(const Mispelling& a, const Mispelling& b) { return a.token < b.token; }

template <typename Iterator, typename UnaryPred>
std::vector<Iterator> find_all(Iterator begin, Iterator end, UnaryPred pred) {
  std::vector<Iterator> its{begin};
  for (auto it = begin; it != end; ++it) {
    if (pred(*it))
      its.push_back(it);
  }
  its.push_back(end);
  return its;
}

void Token::clean(const std::string& source) {
  auto begin = source.begin() + src_offset;
  auto end = source.begin() + src_offset + content.size();

  auto left = std::find_if(begin, end, ::isalnum);
  auto right =
      std::find_if(std::make_reverse_iterator(end), std::make_reverse_iterator(begin), ::isalnum)
          .base();
  src_offset += std::distance(begin, left);

  if (left < right) {
    content = std::string(left, right);
  } else {
    content = "";
  }

  std::transform(content.begin(), content.end(), content.begin(), ::tolower);
}
