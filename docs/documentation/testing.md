---
layout: documentation
title: testing
---

# Testing

A core feature of cpm is how it enables testing in C/C++ projects. cpm offers a flexible base over which multiple testing frameworks can be used.

## Test Discovery

Unless an argument is specified, cpm will recursively look for files under the `tests` directory that match the pattern `test_*.cpp`. The user can also specify with the command line argument which file/directory to use when finding tests. Some examples:

```bash
cpm test                             # Run all test_*.cpp files under the 'tests' directory
cpm test tests/api                   # Run all test_*.cpp files under the 'tests/api' directory
cpm test tests/test_something.cpp    # Run the test/test_something.cpp file 
```

Notice that the tests need not be necessarily under the `tests` directory. As long as the user specifies the directory, any directory can contain tests, provided they are not mixed with any package sources.

## Test Compilation

Each test file is compiled and run as different applications. cpm picks the test main file (the one that starts with `test_`) and compiles it using the packages described in the project. This purpose of compiling a different application per test if to allow the user to mock functions per test suite, especially when writing tests for C code. When writing C code, you can mock functions by re-implementing them, so that the original symbol is replaced.

## Implementing the First Test

Following is an example of how you could implement a test. For this example, we're going to use the [cest](https://github.com/cegonse/cest){:target="_blank"} testing framework, as it is really simple to get started with it. This testing framework has been developed for C++ 11 so, depending on your operating system, you might have to declare the `-std=c++11` compilation flag.

First, assuming that you already have created a cpm project, you need to declare the `cest` bit as a testing dependency in the project descriptor, so you have to modify the `project.yaml` file as follows:

```yaml
...
test:
  bits:
    cest: '1.0'
  cppflags:
    - -std=c++11
```

Then, install the newly declared bit with:

```bash
cpm install
```

Now we're going to create our first test case. From the project root, create the file `tests/test_multiplication.cpp`. Notice the extension `.cpp`, it's the only one that is currently supported. The contents of this file can be:

```c++
#include <cest/cest.h>

using namespace cest;


describe("Multiplication", []() {
  it("can multiply numbers", []() {
    expect(2*2).toBe(4);
  });
});
```

Then you can run this test with:

```bash
cpm test
```

Your output should look something like:

```
-- Configuring done
-- Generating done
-- Build files have been written to: /user/practice/project/build
[3/3] cd /user/practice/project/build && echo

 PASS  ../tests/test_multiplication.cpp:9 it can multiply numbers
cpm: ✔ PASS  (took 1.710s)
```

## Test Result

cpm will interpret the exit code returned by the test binary after execution. If the test binary finished with a 0, then cpm interprets that the tests run successfully. In any other case, cpm will understand that the tests failed and will display the failure. cpm will also try to guess if the test suite failed as a result of a signal (say, SIGSEGV), and display a message.

## Implementing the Test `main` Function 

There are several ways in which we can implement the `main` function for our tests. 

### Shared `main`

The first way of implementing a test main function is to declare a test package in the project descriptor and create a file there implementing the `main` function. Recall that even if the main function is shared, cpm will still compile one binary per test file.

For example:

```yaml
test:
  packages:
    testing/main:
```

And then, in the filesystem:

```bash
project $ find .
.
./testing
./testing/main
./testing/main/main.cpp
...
```

### Bit provided `main`

An example of this is the [cest](https://github.com/cegonse/cest){:target="_blank"} ported bit. This bit is contained into a single header file that implements the function `main`. By including the header file in each `test_.cpp` file, the main function gets defined for that test.

### An example with CppUTest

[cpputest](https://cpputest.github.io/index.html){:target="_blank"} has been ported to cpm and it is available as a bit. An example of how the main has been implemented can be seen at [cpm-hub](https://github.com/jorsanpe/cpm-hub){:target="_blank"}. In this project the main function has been implemented in the file [test/mocks/cpputest.h](https://github.com/jorsanpe/cpm-hub/blob/master/tests/mocks/cpputest.h){:target="_blank"}. Then, the package `test/mocks`, in which the file is contained, has been declared as a test only package in the project descriptor.

Finally, each test that wants to use the CppUTest framework can simply include this file and that's all. You can see an example in the test suite [tests/unit/bits/test_bits_repository_in_sqlite.cpp](https://github.com/jorsanpe/cpm-hub/blob/master/tests/unit/bits/test_bits_repository_in_sqlite.cpp){:target="_blank"}
