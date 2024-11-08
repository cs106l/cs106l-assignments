/*
 * CS106L Assignment 5: TreeBook
 * Created by Fabio Ibanez with modifications by Jacob Roberts-Baca.
 */

/* ========================================================================= *
 * Don't worry about anything beyond this point.                             *
 * (unless you are really curious and want to!)                              *
 * ========================================================================= */

#include <concepts>
#include <fstream>
#include <functional>
#include <ios>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

#include "autograder/diagnostics.hpp"
#include "autograder/utils.hpp"
#include "user.h"

void test_memory_leak_exit_code() {
  std::cout << MemoryDiagnostics::MemoryGuard::get_exit_code() << "\n";
}

template <typename T>
concept printable = requires(T t) {
  { std::cout << t } -> std::same_as<std::ostream&>;
};

template <typename TUser> void test_insertion_operator() {
  if constexpr (printable<TUser>) {
    TUser alice("Alice");
    std::cout << alice << "\n";

    TUser bob("Bob");
    bob.add_friend("Alice");
    std::cout << bob << "\n";

    TUser charlie("Charlie");
    charlie.add_friend("Alice");
    charlie.add_friend("Bob");
    std::cout << charlie << "\n";
  } else {
    std::cerr << "User does not have a valid operator<<." << "\n";
    std::exit(1);
  }
}

template <typename TUser> void test_destructor() {
  MemoryDiagnostics::MemoryGuard guard(
      "Did you remember to delete[] _friends inside the destructor?");
  TUser alice("Alice");
  for (size_t i = 0; i < 100; ++i) {
    alice.add_friend("Friend");
  }
}

template <typename TUser> void test_copy_constructor() {
  if constexpr (printable<TUser>) {
    if constexpr (std::is_copy_constructible_v<TUser>) {
      TUser a("Alice");
      for (size_t i = 0; i < 9; i++) {
        a.add_friend("F");
      }

      TUser b(a);
      b.set_friend(0, "Bob");
      b.set_friend(1, "Alice");
      b.set_friend(2, "Charlie");

      std::cout << a << "\n";
      std::cout << b << "\n";
    } else {
      std::cerr << "User does not have a valid copy constructor." << "\n";
      std::exit(1);
    }
  } else {
    std::cerr << "User does not have a valid operator<<." << "\n";
    std::exit(1);
  }
}

template <typename TUser> void test_copy_assignment() {
  if constexpr (printable<TUser>) {
    if constexpr (std::is_copy_assignable_v<TUser>) {
      MemoryDiagnostics::MemoryGuard guard(
          "Did you remember to delete[] the old value of _friends inside the copy "
          "assignment operator?");

      TUser a("Alice");
      for (size_t i = 0; i < 9; i++) {
        a.add_friend("AF");
      }

      TUser b("Bob");
      for (size_t i = 0; i < 9; i++) {
        b.add_friend("BF");
      }

      a = b;

      std::cout << a << "\n";
      std::cout << b << "\n";
    } else {
      std::cerr << "User does not have a valid copy constructor." << "\n";
      std::exit(1);
    }
  } else {
    std::cerr << "User does not have a valid operator<<." << "\n";
    std::exit(1);
  }
}

template <typename TUser> void test_move_constructor() {
  if constexpr (std::move_constructible<TUser>) {
    std::cerr << "User should not be move constructible. Did you remember to "
                 "delete the move constructor?\n";
    std::exit(1);
  }
}

template <typename TUser> void test_move_assignment() {
  if constexpr (std::is_move_assignable_v<TUser>) {
    std::cerr << "User should not be move assignable. Did you remember to "
                 "delete the move assignment operator?\n";
    std::exit(1);
  }
}

template <typename T>
concept compound_assignable = requires(T a, T b) {
  { a += b } -> std::same_as<T&>;
};

template <typename TUser> void test_compound_assignment() {
  if constexpr (printable<TUser>) {
    if constexpr (compound_assignable<TUser>) {
      TUser a("Alice");
      TUser b("Bob");
      a += b;
      std::cout << a << "\n";
      std::cout << b << "\n";
    } else {
      std::cerr << "User does not have a valid operator+=. Function signature "
                   "should be:\n\n\tUser& operator+=(User& "
                   "other);\n\ninside the User class."
                << "\n";
      std::exit(1);
    }
  } else {
    std::cerr << "User does not have a valid operator<<." << "\n";
    std::exit(1);
  }
}

template <typename TUser>
concept comparable = requires(TUser a, TUser b) {
  { a < b } -> std::same_as<bool>;
};

template <typename TUser> void test_comparable() {
  if constexpr (comparable<TUser>) {
    TUser a("A");
    TUser b("B");
    TUser c("C");

    std::vector<std::pair<TUser, TUser>> pairs = {{a, b}, {b, a}, {b, c}, {c, b}, {c, a}, {a, c}};
    std::cout << std::boolalpha;
    for (const auto& [left, right] : pairs) {
      std::cout << left.get_name() << " < " << right.get_name() << " is " << (left < right) << "\n";
    }
  } else {
    std::cerr << "User does not have a valid operator<. Function signature "
                 "should be:\n\n\tbool operator<(const "
                 "User& other);\n\ninside the User class."
              << "\n";
    std::exit(1);
  }
}

const std::unordered_map<std::string, std::function<void()>> test_functions = {
    {"memory_leak_exit_code", test_memory_leak_exit_code},
    {"insertion_operator", test_insertion_operator<User>},
    {"destructor", test_destructor<User>},
    {"copy_constructor", test_copy_constructor<User>},
    {"copy_assignment", test_copy_assignment<User>},
    {"move_constructor", test_move_constructor<User>},
    {"move_assignment", test_move_assignment<User>},
    {"compound_assignment", test_compound_assignment<User>},
    {"comparable", test_comparable<User>}};

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