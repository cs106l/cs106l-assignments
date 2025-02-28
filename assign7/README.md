<p align="center">
  <img src="docs/art.png" />
</p>

# Assignment 7: Unique Pointer

Due Sunday, March 9th at 11:59PM

## Overview

In this assignment, you will implement a custom version of `unique_ptr` in order to gain some exposure to concepts like RAII and smart pointers that were introduced in lecture this week. In addition, you will exercise some of the skills we've seen throughout the course: templates, operator overloading, and move semantics.

There are three files you'll work with for this assignment:

- `unique_ptr.h` - Contains all the code for your `unique_ptr` implementation.
- `main.cpp` - Contains some code that uses your `unique_ptr`. You'll write one function here!
- `short_answer.txt` - Contains a few short answer questions you'll answer as you work on the assignment.

## Running your code

To run your code, first you'll need to compile it. Open up a terminal (if you are using VSCode, hit <kbd>Ctrl+\`</kbd> or go to **Terminal > New Terminal** at the top). Then make sure that you are in the `assign7/` directory and run:

```sh
g++ -std=c++20 main.cpp -o main
```

Assuming that your code compiles without any compiler errors, you can now do:

```sh
./main
```

which will actually run the `main` function in `main.cpp`.

As you are following the instructions below, we recommend intermittently compiling/testing with the autograder as a way to make sure you're on the right track!

> [!NOTE]
>
> ### Note for Windows
>
> On Windows, you may need to compile your code using
>
> ```sh
> g++ -static-libstdc++ -std=c++20 main.cpp -o main
> ```
>
> in order to see output. Also, the output executable may be called `main.exe`, in which case you'll run your code with:
>
> ```sh
> ./main.exe
> ```

## Part 1: Implementing `unique_ptr`

In the first part of the assignment, you will implement one of the smart pointers we discussed in Thursday's lecture: `unique_ptr`. The `unique_ptr` you will implement is a simpler version of the standard library's [`std::unique_ptr`](https://en.cppreference.com/w/cpp/memory/unique_ptr). Recall that a `unique_ptr` represents a pointer to dynamically allocated memory that is owned by a single (*unique*) variable. When that variable goes out of scope, it automatically cleans up the allocated memory that it owns by calling `delete`. This behaviour is known as RAII (resource acquisition is initialization). **For our purposes, you may assume that `unique_ptr` points to a single element of type T. You will not have to call `delete[]` at any point or handle pointers to dynamically allocated arrays.**

> [!IMPORTANT]  
> ##### `short_answer.txt`  
> **Q1:** List one or two benefits of using RAII to manage memory instead manually calling `new` and `delete`.

> [!NOTE]
> While our `unique_ptr` will not support pointers to arrays, we could add this behaviour if we wanted to. For example, the C++ standard library `std::unique_ptr` uses a *template specialization* to implement different behaviour for array pointers. Such a template specialization might look like this:
>
> ```cpp
> template <typename T>
> class unique_ptr<T[]>;
> ```
>
> In effect, we would have two versions of `unique_ptr`: one for single elements and one for arrays of elements. Each version supports different operations; for example, the array version provides a subscript operator (`operator[]`) to deference elements in the array, while the single element version does not.

### Implementing `unique_ptr` functionality

Take a moment to scan over the provided code for `unique_ptr` in `unique_ptr.h`. We have provided the basic interface for a `unique_ptr`: you will implement this interface. Remember, a `unique_ptr` should look and behave like a regular pointer, supporting operations like dereferencing (`operator*`) and member access (`operator->`). Several of these methods have both `const` and non-`const` versions in order for our class to be fully const-correct.

You will implement the basic pointer interface for a `unique_ptr` by implementing the following points. Each of these tasks should be relatively straightforward and can be completed by adding/changing 1-2 lines in `unique_ptr.h`:

* The `private` section of `unique_ptr`
* `unique_ptr(T* ptr)` (constructor)
* `unique_ptr(std::nullptr_t)` (constructor for `nullptr`)
* `T& operator*()`
* `const T& operator*() const`
* `T* operator->()`
* `const T* operator->() const`
* `operator bool() const`

### Implementing RAII

At this point, our `unique_ptr` will behave as if it were a raw pointer, but it will not actually do any automatic memory management such as deallocating memory when a `unique_ptr` variable goes out of scope. Add to that, our pointer is not *unique*: multiple copies of it (all pointing to the same memory) can be made indiscriminantly. For example, let's assume that our `unique_ptr` properly cleans up its data when it goes out of scope. Consider the following code block:

```cpp
int main() 
{
  unique_ptr<int> ptr1 = make_unique<int>(5);

  // ptr1 points to 5 (dynamically allocated on the heap)

  {

    unique_ptr<int> ptr2 = ptr1; // shallow copy

  } // <-- data for ptr2 deallocated here

  std::cout << *ptr1 << std::endl;
  return 0;
}
```

Since `ptr1` and `ptr2` point to the same memory, when `ptr2` goes out of scope, it takes `ptr1`'s data with it! As a result, `*ptr1` is undefined behaviour.

On the other hand, we should still be able to **move** a `unique_ptr`. Recall that move semantics allows us to take ownership of an object's resources without making an expensive copy. Moving a unique pointer is valid because it preserves the uniqueness of the pointer — at any point in time, we still have only one pointer to the underlying memory. We simply change who (what variable) owns that memory.

In order to achieve these goals — automatic deallocation of memory, no copying, and move semantics — we must implement some special member functions on the `unique_ptr` class. **Specifically, implement the following SMFs:**

* `~unique_ptr()`: Deallocates the pointer's memory
* `unique_ptr(const unique_ptr& other)`: Copies a unique pointer. Should be deleted.
* `unique_ptr& operator=(const unique_ptr& other)`: Copy assigns a unique pointer. Should be deleted.
* `unique_ptr(unique_ptr&& other)`: Moves a unique pointer.
* `unique_ptr& operator=(unique_ptr&& other)`: Move assigns a unique pointer.

After implementing the above functions, you should be passing all of the autograder tests for **Part 1**.

> [!IMPORTANT]  
> ##### `short_answer.txt`  
> **Q2:** When implementing move semantics for a `unique_ptr`, for example in the move constructor `unique_ptr(unique_ptr&& other)`, it is essential that we set the underlying pointer of the `other` parameter to `nullptr` before exiting the function. Explain in your own words what problem would arise if we did not.

## Part 2: Using `unique_ptr`

Now that we have a `unique_ptr` implementation, let's use it! Take a look at `main.cpp`. We have given you a complete implementation of a singly-linked list (`ListNode`) that utilizes `unique_ptr` to ensure that all nodes in the list get deallocated properly. For example, this code produces the following output:

```cpp
int main()
{

  auto head = cs106l::make_unique<ListNode<int>>(1);
  head->next = cs106l::make_unique<ListNode<int>>(2);
  head->next->next = cs106l::make_unique<ListNode<int>>(3);

  // memory of head:
  //
  // head -> (1) -> (2) -> (3) -> nullptr
  //
  //

} // <- `head` destructed here!

// Output:
// Constructing node with value '1'
// Constructing node with value '2'
// Constructing node with value '3'
// Destructing node with value '1'
// Destructing node with value '2'
// Destructing node with value '3'
```

Notice that we didn't have to make any calls to `delete`! The RAII behaviour of `unique_ptr` guarantees that all memory in the list is deallocated recursively. When `head` goes out of scope, it calls the destructor of node `(1)`, which calls the destructor of `(2)`, which calls the destructor of `(3)`. 

> [!IMPORTANT]  
> ##### `short_answer.txt`  
> **Q3:** This method of recursive deallocation through RAII works great for small lists, but may pose a problem for longer lists. Why? Hint: what is the limit for how "deep" a recursive function's call stack can grow?

**Your task is to implement the function `create_list` which converts a `std::vector<T>` into a `unique_ptr<ListNode<T>>`.** The order of elements in the vector should be preserved in the list, and `nullptr` should be returned for an empty vector. There are many ways you could go about this; one is to construct the list in reverse (starting at the tail and working towards the head). **Note that you must use the `cs106l::unique_ptr` under the `cs106l` namespace, and not the `std::unique_ptr`!** Here is an algorithm you should follow in your implementation:

1. Initialize a `cs106l::unique_ptr<ListNode<T>> head = nullptr`.
2. Iterate through the `std::vector` **backwards.** For each element in the vector:
    - 2a. Create a new `cs106l::unique_ptr<ListNode<T>> node` whose value is the element in the vector.
    - 2b. Set `node->next` to `head`.
    - 2c. Set `head` to `node`
3. Finally, return `head`

> [!IMPORTANT]  
> ##### `short_answer.txt`  
> **Q4.** In your implementation of points 2b and 2c, you may have a hard time getting the compiler to allow you to assign, for example, `node->next` to `head` as it will complain that there is no copy assignment operator. That is exactly right, as `unique_ptr` cannot be copied as we discussed previously!
>
> In order to get the behaviour we want, we must force the compiler to **move assign** `head` into `node->next` rather than copy assign. Recall from the move semantics lecture that we can do this by writing `node->next = std::move(head)`.
>
> What does `std::move` do in this context? Why is it safe to use `std::move` and move semantics here?

> [!NOTE]  
> Be careful of trying to use `size_t` as an index while looping backwards through a vector. `size_t` can only be a non-negative integer, and attempting to go below zero while checking the for loop bounds can lead to unexpected behaviour.
> To fix this issue, try using an `int` instead.

Once you've implemented `create_list`, we can now create a list and print it out. For brownie points, take a look at the `map_list()` and `linked_list_example()` functions which together call your `create_list` function and print out its elements each on their own line. At this point, you should pass all of the tests in **Part 2**.

## 🚀 Submission Instructions

Before you submit the assignment, please fill out this [short feedback form](https://forms.gle/TXzLEgdKYnEPes22A). **Completion of the form is required to receive credit for the assignment.** After filling out the form, please upload the files to Paperless under the correct assignment heading.

Your deliverable should be:

- `unique_ptr.h`
- `main.cpp`
- `short_answer.txt`

You may resubmit as many times as you'd like before the deadline.
