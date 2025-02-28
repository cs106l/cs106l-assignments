/* ========================================================================= *
 * Don't worry about anything beyond this point.                             *
 * (unless you are really curious and want to!)                              *
 * ========================================================================= */

#include "diagnostics.hpp"

static const std::string kReallyLongString =
    "this is a really long string! It should be long enough that attempting to iterate "
    "through it will eventually cause a segfault if the pointer is dangling, because some "
    "region of the memory is OOB. This string is brought to you by CS106L, the course that "
    "believes in the importance of understanding memory safety, because one missed pointer "
    "could mean the difference between A and F! Go Cardinal! Also, consider this a gentle "
    "reminder: this isn’t Python, so manual memory management may be included at no extra "
    "charge. You’re welcome. Speaking of pointers, has anyone seen the \"mystery byte\"? "
    "It’s just hanging around, waiting for a dereference. Maybe it’s busy \"pointing\" out "
    "the occasional nullptr. Ah, the smell of freshly allocated memory. By the way, in case "
    "you forgot, we're a couple hundred characters into this string now, and if you're "
    "reading this, you're probably wondering, 'Is there any actual purpose to this string, "
    "or is it just here to mess with us?' Answer: Yes. And if you think you’re almost at "
    "the end... not quite. Consider this a page-sized ode to the indomitable resilience "
    "of pointers, the unsung heroes of the stack and the heap alike. Here’s to them, "
    "navigating virtual landscapes one byte at a time. Now, let’s throw in some more filler "
    "text to make sure this string really hits the memory mark, like a long C++ template "
    "compile time, slow but ultimately fulfilling! Here's a toast to dangling pointers "
    "that never quite got to dangle, references that referenced but nobody cared, and "
    "nulls that nulled all our hopes and dreams. Cheers, and remember, this is CS106L, "
    "where every day is a new lesson in why C++ might actually be the most rewarding "
    "source of frustration you’ll ever encounter! Now, brace yourself, because we’re only "
    "halfway there. In the meantime, let’s review a few key takeaways from this course: "
    "Pointers may seem daunting, but once you master them, they’re basically pets that "
    "require a lot of attention (and feeding). Smart pointers? They’re like that pet that "
    "takes care of itself (most of the time), but when they don’t, good luck explaining "
    "the problem to the debugger. Let's dive deeper into memory safety: it's like living "
    "next to a fireworks factory — thrilling, a little dangerous, and you'll need to wear "
    "safety goggles (or at least code defensively). Don’t forget, C++ loves you, it just "
    "has an unusual way of showing it, like a friend who insists that 'new' and 'delete' "
    "are still a thing. In fact, using raw pointers in modern C++ is like riding a unicycle "
    "through San Francisco traffic: technically possible but highly inadvisable. And for "
    "those brave souls exploring STL containers, just remember, std::vector is like the "
    "cafeteria food line at Stanford: it has a fixed capacity, but there's always room for "
    "more if you ask politely (or push_back). Speaking of vectors, did you know std::string "
    "is basically a vector of characters? Which means this string here is essentially a "
    "really long vector. In fact, it's so long it might just loop back around and greet "
    "you on the other side of memory. But don’t let that distract you. Let’s continue, shall "
    "we? There's still plenty of memory to allocate, and we wouldn’t want to waste it. After "
    "all, we’re in Silicon Valley, where memory is abundant, though perhaps a bit overpriced. "
    "CS106L: exploring the unexplored realms of pointers, templates, and algorithms that "
    "feel like they should be simpler, but somehow they’re not. And now for an interlude: "
    "If you’ve made it this far, you’re either incredibly dedicated or you just scrolled down "
    "to see if I was serious about making this string long enough to fill a page. Spoiler "
    "alert: I was. Here’s more filler to add weight to this epic string: from unique_ptr to "
    "shared_ptr, the whole world of C++ is a carefully orchestrated chaos. Null pointers "
    "dream of electric dereferences, references hold their ground, and const qualifiers just "
    "sit there, unmoving, unyielding, a quiet reminder of immutability in an ever-changing "
    "world. And if you’re still reading, well, hats off to you. You’ve truly embodied the "
    "spirit of CS106L, the class where we redefine what it means to ‘go the extra mile’ in "
    "memory allocation. One last bit of advice: in C++, life is short, so make sure your "
    "references are always up to date. Also, remember that every dangling pointer is just "
    "a tragedy waiting to happen, and each memory leak a tear in the fabric of the stack. "
    "So go forth, code boldly, and may all your pointers land safely!";

void test_linked_list_example() {
  MemoryDiagnostics::MemoryGuard guard("Failed to deallocate all nodes in linked list!");
  std::vector<std::string> names{"Jacob", "Fabio", "Keith", "Chris", "Sean"};
  auto head = create_list(names);
  map_list(head, [](const std::string& name) { std::cout << name << "\n"; });
}

void test_destructor() {
  MemoryDiagnostics::MemoryGuard guard("Failed to deallocate memory in unique_ptr destructor!");
  for (size_t i = 0; i < 1000; ++i) {
    auto ptr = cs106l::make_unique<std::string>("hello");
  }

  // Ensure that deallocation of empty unique_ptr is successful
  for (size_t i = 0; i < 1000; ++i) {
    cs106l::unique_ptr<std::string> ptr;
  }
}

void test_move_constructor() {
  MemoryDiagnostics::MemoryGuard guard(
      "Failed to deallocate memory in unique_ptr move constructor! It may help to review the "
      "lecture on move semantics!");
  size_t sum = 0;
  for (size_t i = 0; i < 1000; ++i) {
    auto ptr = cs106l::make_unique<std::string>(kReallyLongString);
    auto size = ptr->size();
    auto other = std::move(ptr);
    ptr.~unique_ptr(); // Forcibly destroy old pointer

    // Iterating through other should be valid.
    // Even though old was destroyed, we took ownership of the memory.

    for (size_t i = 0; i < size; ++i) {
      sum += (*other)[i];
    }
  }

  std::cout << sum << "\n";
}

void test_move_assignment() {
  MemoryDiagnostics::MemoryGuard guard(
      "Failed to deallocate memory in unique_ptr move assignment! Did you make sure to deallocate "
      "the existing data before assigning the private fields? It may help to review the lecture on "
      "move semantics!");
  for (size_t i = 0; i < 1000; ++i) {
    auto ptr1 = cs106l::make_unique<std::string>("hello");
    auto ptr2 = cs106l::make_unique<std::string>("world");
    ptr1 = std::move(ptr2);
    if (ptr2) {
      std::cerr << "Move assignment failed to set other pointer to nullptr! It may help to review "
                   "the lecture on move semantics!"
                << "\n";
      std::exit(1);
    }
  }
}

void test_move_self_assignment() {
  MemoryDiagnostics::MemoryGuard guard(
      "Failed to deallocate memory in unique_ptr move assignment with self-assignment! It may help "
      "to review the lecture on move semantics!");
  size_t sum = 0;
  for (size_t i = 0; i < 1000; ++i) {
    auto ptr = cs106l::make_unique<std::string>(kReallyLongString);
    ptr = std::move(ptr);

    // If we don't check for self-assignment in the move constructor,
    // then ptr will either be dangling or end up being nullptr.
    // This should check against that
    if (!ptr)
      break;

    for (size_t i = 0; i < ptr->size(); ++i) {
      sum += (*ptr)[i];
    }
  }

  std::cout << sum << "\n";
}

template <typename UniquePtr> void test_copy() {
  if constexpr (std::is_copy_constructible_v<UniquePtr>) {
    std::cerr << "unique_ptr should not be copy constructible. Did you remember to delete the copy "
                 "constructor?\n";
    std::exit(1);
  }

  if constexpr (std::is_copy_assignable_v<UniquePtr>) {
    std::cerr << "unique_ptr should not be copy assignable. Did you remember to delete the copy "
                 "assignment operator?\n";
    std::exit(1);
  }
}

const std::unordered_map<std::string, std::function<void()>> test_functions = {
    {"memory_leak_exit_code",
     []() { std::cout << MemoryDiagnostics::MemoryGuard::get_exit_code() << "\n"; }},
    {"destructor", test_destructor},
    {"copy", test_copy<cs106l::unique_ptr<std::string>>},
    {"move_constructor", test_move_constructor},
    {"move_assignment", test_move_assignment},
    {"move_self_assignment", test_move_self_assignment},
    {"linked_list", test_linked_list_example},
};

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

int main(int argc, char* argv[]) {
  if (argc == 2) {
    if (test_functions.find(argv[1]) != test_functions.end()) {
      test_functions.at(argv[1])();
      return 0;
    }

    std::cerr << "Test '" << argv[1] << "' not found." << "\n";
    return 1;
  }

  return run_autograder();
}