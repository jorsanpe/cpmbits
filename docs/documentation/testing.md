---
layout: documentation
title: testing
---

# Testing

Testing is an core part of cpm. cpm offers a flexible base over which multiple testing frameworks can be used.  

## Test Discovery

Unless an argument is specified, cpm will recursively look for files under the `tests` directory that match the pattern `test_*.cpp`. The user can also specify with the command line argument which file/directory to use when finding tests. Some examples:

```bash
cpm test                            # Run all test_*.cpp files under the 'tests' directory
cpm test test/api                   # Run all test_*.cpp files under the 'test/api' directory
cpm test test/test_something.cpp    # Run the test/test_something.cpp file 
```  

## Test Compilation

Each test file is compiled separately into a different application. This strategy gives the ability to mock certain functions for example in C projects. 

The C language, allows redefining functions in several ways, and that can be used to our advantage to mock the behaviour of a certain function. The main problem with function/symbol redefinition is that it replaces the definition for the entire application. If all the tests were compiled into a single binary, then the use of this strategy would not be as flexible, as redefining a function would imply that the real function implementation is no longer available for any test case.

## Test Result

cpm will interpret the exit code returned by the test binary after execution. If the test binary finished with a 0, then cpm interprets that the tests run successfully. In any other case, cpm will understand that the tests failed and will display the failure.

## Implementing the Test `main` Function 

There are several ways in which we can define the `main` function for our tests. How the main is implemented will depend on the testing framework used. Some examples are [cpputest](https://cpputest.github.io/index.html){:target="_blank"} or [cest](https://github.com/cegonse/cest){:target="_blank"}. Testing frameworks are expected to be available as bits.

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
