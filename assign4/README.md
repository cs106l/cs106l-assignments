# Assignment 4: Ispell

Due Friday, February 14th at 11:59PM

## Overview

Now that we've spent some time discussing the core components of the STL—containers, iterators, functors, and algorithms—and the key ingredient that powers it all—templates—let's put it all together! 
In this assignment, you will write the core logic for [Ispell](https://en.wikipedia.org/wiki/Ispell), an old Unix style spell checker that does a simple spellcheck. To do so, you will write some
code that makes use of the `<algorithm>` header and the new C++ ranges library.

All of your code will go into `spellcheck.cpp`. Once you are done, you will have a spell checker that looks like this:

<p align="center">
  <img src="docs/spellcheck.png" alt="An example terminal run of the spellcheck program" />
</p>

To download the starter code for this assignment, please see the instructions for [**Getting Started**](../README.md#getting-started) on the course assignments repository.

## Running your code

To run your code, first you'll need to compile it. Open up a terminal (if you are using VSCode, hit <kbd>Ctrl+\`</kbd> or go to **Terminal > New Terminal** at the top). Then make sure that you are in the `assign2/` directory and run:

```sh
g++ -std=c++20 main.cpp spellcheck.cpp -o main
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
> g++ -static-libstdc++ -std=c++20 main.cpp spellcheck.cpp -o main
> ```
>
> in order to see output. Also, the output executable may be called `main.exe`, in which case you'll run your code with:
>
> ```sh
> ./main.exe
> ```

## Building Ispell

The classic Unix program Ispell works as follows. First, a dictionary is loaded into memory containing all of the common English words. Then, each word in the input is compared to each word in the dictionary. A word is mispelled if it can't be found in the dictionary. Then, suggestions for the mispelled word are found using the [Damerau-Levenshtein distance](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance), which tells you approximately how many edits (consisting of insertions, deletions or substitutions of a single character, or swapping two adjacent characters) must be done to change one word into the other. If the Damerau-Levenshtein distance is exactly one between the mispelled word and one of the dictionary words, then it is added to the list of suggestions. The idea here is that when one mispells a word, usually they are only off by one small change (for example, consider "stopping" vs. "stoping").

In this assignment, we have given you all the infrastructure to build this spellchecker, including implementations of the Damerau-Levenshtein function. Your job will be to implement the core of the algorithm that spellchecks words. Specifically, you will write an algorithm that splits an input string into a set of tokens (`tokenize`), and another algorithm that actually identifies mispelled words given a (tokenized) input string and a dictionary (`spellcheck`). To add a bit of an extra challenge (and to make this relevant to the last week's lectures), there's a catch: you can't use any for/while loops in your code or helper functions. You must implement these tasks entirely using the STL: `tokenize` using the traditional STL algorithms, and `spellcheck` using the brand new ranges library. In the process, you will get exposure to how we can manipulate modern data structures in C++ using algorithms and lambda functions.

This may sound like a lot, but don't worry! This handout will walk you through each of the algorithms in detail.

### `tokenize`

The `tokenize` method will take an input string and split it up into a set of `Token` objects. Take a look at the `Token` struct we've defined in `spellcheck.h`. A `Token` represents a single piece of content within a larger file: conceptually, it is just a single word appearing in a broader text; in code, it is a `std::string` apppearing somewhere in a file at index `src_offset`. Our goal is to split up an input file into a set of `Token`s, which we refer to as a `Corpus` (a `Corpus` is just a type-alias for an `std::set<Token>`).

A key constraint for this problem is as follows: tokens are surrounded by whitespace and/or the boundaries of the input file. For example, the short string `"history will absolve me"` consists of four tokens: 

* `{ content: "history", src_offset: 0 }`
* `{ content: "will", src_offset: 8 }`
* `{ content: "absolve", src_offset: 13 }`
* `{ content: "me", src_offset: 21 }`

To implement `tokenize`, we will use the traditional STL methods like `std::transform`, without any for/while loops. Our high level strategy to do this will be to:

1. Identify all iterators to space characters
2. Generate tokens between consecutive space characters
3. Get rid of empty tokens

Here's a step-by-step guide you can follow to accomplish this:

1. **Step One: Identify all iterators to space characters**  
    If we can get all iterators in the string pointing to whitespace characters, then we can more-or-less think of the tokens present in the string as the characters between any two whitespace characters. We almost want to call `find_if` multiple times to collect all of iterators to whitespace characters. Fortunately, we have provided you with a method to do just that, `find_all`.

    > [!NOTE]
    > ```cpp
    > template <typename Iterator, typename UnaryPred>
    > std::vector<Iterator> find_all(Iterator begin, Iterator end, UnaryPred pred);
    > ```
    >
    > Returns a vector of all the iterators between `begin` and `end` whose element matches the unary predicate `pred`. **This vector also includes the boundary iterators, `begin` and `end`**. In other words, if `it` is an iterator in the returned vector, then either `pred(*it)` or `it == begin` or `it == end`. The iterators in the vector are guaranteed to be in order.

    We can get a vector of all the iterators to whitespace character by calling `find_all` on our `source` string and passing in a unary predicate that checks if a character is whitespace. We thankfully have such a function built-in to C++: it is called `isspace`.

    > [!NOTE]
    > When passing `isspace` to `find_all`, we must pass it as `isspace` and not `std::isspace`. This is because there are actually multiple versions of the `isspace` method:
    >
    > ```cpp
    > int isspace( int ch );                        // Defined in header <cctype> and <ctype.h>
    >
    > template< class CharT >
    > bool isspace( CharT ch, const locale& loc );  // Defined in header <locale>
    > ```
    >
    > Technically, the first version is defined both [as part of the `namespace std`](https://en.cppreference.com/w/cpp/header/cctype) and [as a free-floating function inherited from C](https://en.cppreference.com/w/c/string/byte) (and not in any particular namespace). Writing `isspace` refers to the C version, whereas `std::isspace` refers to both of the above functions and so the compiler has a hard time inferring the `UnaryPred` type parameter.
    >
    > Sometimes you will see people write `::isspace`: this just tells C++ to look in the *global namespace* (not inside `std`) for `isspace`, and accomplishes a similar thing.

2. **Step Two: Generate tokens between consecutive space characters**
    Now that we have all of the iterators to space characters, we can consider a token as any range of characters between any two consecutive iterators. To see why, consider this diagram:

    ```
    "history will absolve me"
     ▲      ▲    ▲       ▲  ▲
     ├──────┼────┼───────┼──┤
     │  t1  │ t2 │   t3  │t4│
    ```

    The arrows represent the return value of `find_all`, and as you can see, the tokens can be found between the arrows. Don't worry whether or not the iterator actually does point to whitespace or not—`Token` has a constructor that takes in a pair of iterators and automatically handles trimming whitespace around the edges.

    > [!NOTE]
    > ```cpp
    > template <typename It>
    > Token(const std::string& source, It begin, It end);
    > ```
    >
    > Given a `source` string and a pair of iterators `begin` and `end` identifying the extents of a token inside `source`, constructs a `token`. Automatically handles trimming extra whitespace and punctuation characters at the edges of the token.

    We need to somehow call this constructor for each pair of consecutive iterators. To do this, we will use [overload (3) of `std::transform`](https://en.cppreference.com/w/cpp/algorithm/transform).

    > [!NOTE]
    > ```cpp
    > template <class InputIt1, class InputIt2, class OutputIt, class BinaryOp>
    > OutputIt transform( InputIt1 first1, InputIt1 last1, InputIt2 first2,
    >               OutputIt d_first, BinaryOp binary_op );
    > ```
    > 
    > Given two equally-sized ranges, one starting at `first1` and the other starting at `first2` (such that end iterator of the first range is `last1`), applies a binary function `binary_op` and stores the result to the output range (of the same size) starting at `d_first`. 
    
    For our `binary_op`, we can provide a lambda function that takes in two `std::string::iterator`s (you might choose to use `auto` parameters here, as discussed in lecture) `it1` and `it2`, and constructs the `Token` using `Token { source, it1, it2 }`. Note that we must pass `source` to this constructor, so you will need to capture it in the lambda function you create!

    For the output range (`d_first`), we will first create a `std::set<Token>` to store the tokens that we find. Suppose we call that variables `tokens`. Then, we can create an [`std::inserter(tokens, tokens.end())`](https://en.cppreference.com/w/cpp/iterator/inserter) to store the resulting tokens to.

    > [!NOTE]
    > ```cpp
    > template <class Container>
    > std::insert_iterator<Container> inserter(Container& c, typename Container::iterator i);
    > ```
    >
    > An output iterator that inserts any value written to it into the container `c` at position `i` (where `i` is of the container's iterator type). The return value is an [`std::insert_iterator<Container>`](https://en.cppreference.com/w/cpp/iterator/insert_iterator) which can be passed as the output range to other STL algorithms (for example, `std::transform`).

    For the input ranges (`first1`, `last1`, and `first2`), we will need to be a bit clever in our choice of iterators. We must choose iterators such that the `binary_op(first1, first2)` constructs the first token in the container, `binary_op(first1 + 1, first2 + 1)` constructs the second token in the container, etc. How can we manipulate the iterators to allow this behaviour? Remember, `tokens.begin()` is the first iterator of the container, `tokens.begin() + 1` is the second iterator, etc. Also note: there is nothing preventing the range given by `first1` from overlapping with the range given by `first2`!

3. **Step Three: Get rid of empty tokens**  
    Some of the tokens we've produced so far will only consist of whitespace (for example, what if there were multiple consecutive whitespace characters in our string). We will need to remove these characters. Luckily, there is a [`std::erase_if` function](https://en.cppreference.com/w/cpp/container/set/erase_if) that can remove elements from an `std::set` which match some condition.

    > [!NOTE]
    > ```cpp
    > template <class Key, class Compare, class Alloc, class Pred>
    > std::set<Key, Compare, Alloc>::size_type erase_if (std::set<Key, Compare, Alloc>& c, Pred pred);
    > ```

    For `pred`, we can pass a lambda function which checks if a token is empty. For example, if `token` is a `Token`, we could check `token.content.empty()`.

    Finally, you can return `tokens`!

Once you've finished this step, your spellcheck should start reporting token counts. If you compile your code, you can run:

```sh
./main "hello wrld"
```

to spellcheck the string `"hello wrld"`. Notice that it now reports:

```
Loading dictionary... loaded 464811 words.
Tokenizing input... got 2 tokens.
```

Your tokenize method has tokenized an English dictionary of about a half-million words, as well as the input string, `"hello wrld"`, in lightning speed. However, it's not quite yet spell-checking: `"wrld"` is reported as correctly spelled. To fix this, we will need to implement the `spellcheck` function.

### `spellcheck`