/** Contains memory diagnostics to track memory allocations and report memory leaks. */

#pragma once

#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <new>
#include <unordered_map>

namespace MemoryDiagnostics {
namespace detail {

/**
 * In order to initialize an unordered_map inside of the MemoryTracker class below,
 * we must make dynamic allocations. However, the default allocator for unordered_map
 * calls operator new and delete, which would cause infinite recursion. To avoid this,
 * we define a custom allocator that uses std::malloc and std::free instead and define
 * the unordered_map in MemoryTracker to use this allocator.
 *
 * See https://en.cppreference.com/w/cpp/named_req/Allocator for more information.
 */
template <class T> struct Mallocator {
  using value_type = T;

  Mallocator() = default;

  template <class U> constexpr Mallocator(const Mallocator<U>&) noexcept {}

  [[nodiscard]] T* allocate(std::size_t n) {
    if (n > std::numeric_limits<std::size_t>::max() / sizeof(T))
      throw std::bad_array_new_length();

    if (auto p = static_cast<T*>(std::malloc(n * sizeof(T)))) {
      return p;
    }

    throw std::bad_alloc();
  }

  void deallocate(T* p, std::size_t n) noexcept { std::free(p); }
};

template <class T, class U> bool operator==(const Mallocator<T>&, const Mallocator<U>&) {
  return true;
}

template <class T, class U> bool operator!=(const Mallocator<T>&, const Mallocator<U>&) {
  return false;
}

class MemoryTracker {
  using AllocationsMap = std::unordered_map<void*, size_t, std::hash<void*>, std::equal_to<void*>,
                                            Mallocator<std::pair<void* const, size_t>>>;
  size_t bytes_outstanding = 0;
  AllocationsMap allocations;

public:
  void* allocate(size_t size) {
    if (size == 0)
      ++size; // avoid std::malloc(0) which may return nullptr on success

    void* ptr = std::malloc(size);
    if (ptr == nullptr)
      throw std::bad_alloc{}; // required by [new.delete.single]/3

    bytes_outstanding += size;
    allocations[ptr] = size;
    return ptr;
  }

  void deallocate(void* ptr) {
    std::free(ptr);
    auto it = allocations.find(ptr);
    if (it != allocations.end()) {
      bytes_outstanding -= it->second;
      allocations.erase(it);
    }
  }

  size_t get_bytes_outstanding() const { return bytes_outstanding; }
};

MemoryTracker& get_tracker() {
  static MemoryTracker tracker;
  return tracker;
}

} // namespace detail

/**
 * MemoryGuard makes sure that the dynamic allocation count at construction
 * matches the count at destruction. If the counts do not match, MemoryGuard
 * will print an error message to stderr and exit the program with a predefined
 * exit code.
 */
class MemoryGuard {
public:
  MemoryGuard(const char* message)
      : message(message), initial_bytes_outstanding(detail::get_tracker().get_bytes_outstanding()) {
  }

  ~MemoryGuard() {
    if (initial_bytes_outstanding != detail::get_tracker().get_bytes_outstanding()) {
      if (message)
        std::cerr << message << std::endl;
      std::exit(exit_code);
    }
  }

  static int get_exit_code() { return exit_code; }

private:
  const char* message = nullptr;
  size_t initial_bytes_outstanding;
  static constexpr const int exit_code = 106;
};

} // namespace MemoryDiagnostics

void* operator new(std::size_t sz) { return MemoryDiagnostics::detail::get_tracker().allocate(sz); }

void* operator new[](std::size_t sz) {
  return MemoryDiagnostics::detail::get_tracker().allocate(sz);
}

void operator delete(void* ptr) noexcept {
  MemoryDiagnostics::detail::get_tracker().deallocate(ptr);
}

void operator delete(void* ptr, std::size_t size) noexcept {
  MemoryDiagnostics::detail::get_tracker().deallocate(ptr);
}

void operator delete[](void* ptr) noexcept {
  MemoryDiagnostics::detail::get_tracker().deallocate(ptr);
}

void operator delete[](void* ptr, std::size_t size) noexcept {
  MemoryDiagnostics::detail::get_tracker().deallocate(ptr);
}