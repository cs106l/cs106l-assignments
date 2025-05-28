/*
 * CS106L Assignment 7: Unique Pointer
 * Created by Jacob Roberts-Baca.
 */

#include <functional>
#include <iostream>
#include <sstream>
#include <unordered_map>
#include <vector>

#include "unique_ptr.h"

/**
 * @brief A singly-linked list node that deallocates itself automatically
 * by using a `unique_ptr` to manage the pointer to the next node.
 * @tparam T The type of the value stored in the node.
 *
 * @note No modifications are necessary to this struct in order to complete the assignment!
 */
template <typename T> struct ListNode {

  /** @brief The value stored inside this node. */
  T value;

  /** @brief The smart pointer to the next node. May be null. */
  cs106l::unique_ptr<ListNode<T>> next;

  /**
   * @brief Constructs a single element linked list, setting `next` to `nullptr`.
   * @param value The value to store in the node.
   */
  ListNode(T value) : value(value), next(nullptr) {
    /* This line is just here for logging purposes so we can see when the
     * constructor runs!
     */
    std::cout << "Constructing node with value '" << value << "'\n";
  }

  ~ListNode() {
    /* This line is just here for logging purposes so we can see when the
     * destructor runs!
     */
    std::cout << "Destructing node with value '" << value << "'\n";
  }
};

/**
 * @brief Creates a singly-linked list from a vector of values.
 * @param values The values to store in the list.
 * @return A `unique_ptr` to the head of the list.
 */
template <typename T> cs106l::unique_ptr<ListNode<T>> create_list(const std::vector<T>& values) {
  /* STUDENT TODO: Implement this method */
  throw std::runtime_error("Not implemented: createList");
}

/**
 * @brief Applies a function to each element in the linked list.
 * @tparam T The type of the value stored in the list.
 * @tparam Func The type of the function to apply.
 * @param head The head of the linked list.
 * @paragraph func The function to apply to each element.
 */
template <typename T, typename Func>
void map_list(const cs106l::unique_ptr<ListNode<T>>& head, const Func& func) {
  if (!head)
    return;
  func(head->value);
  map_list(head->next, func);
}

/**
 * @brief An example of using a singly-linked list with `unique_ptr`.
 */
void linked_list_example() {
  std::vector<std::string> names{"Jacob", "Fabio", "Keith", "Chris", "Sean"};
  auto head = create_list(names);
  map_list(head, [](const std::string& name) { std::cout << name << "\n"; });
}

#include "autograder/utils.hpp"