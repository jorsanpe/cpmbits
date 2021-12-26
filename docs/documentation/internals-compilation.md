---
layout: documentation
title: internals-compilation
---

# Internals: Compilation

cpm orquestrates the compilation using cmake. Each time the project is built or tested, cpm generates a new `CMakeLists.txt` custom tailored for the build target.

## Compilation Plans

At the broadest level, cpm uses a concept call a [compilation plan](/documentation/project-descriptor.html#compilation-plan). A compilation plan defines the project packages, the compilation options and the dependencies. There are four compilation plans, that are combined in order to generate the final compilation options:
  - *Common build compilation plan*, defined in the `build` element of the project descriptor.
  - *Common test compilation plan*, defined in the `test` element of the project descriptor.
  - *Target specific build compilation plan*, defined in the `target.<target_name>.build` element of the project descriptor.
  - *Target specific test compilation plan*, defined in the `target.<target_name>.test` element of the project descriptor.

As you can see, each target has its own compilation plan. **For the time being, the only target specific test compilation plan supported is the `default` one.**

The different compilation plans are combined to generate the final set of compilation options for all the files of that target. Let's say you build the project for the `default` target using `cpm build`, then the cflags that will be used to compiled all files will be the cflags defined in the common build compilation plan plus the cflags defined in the `default` target build compilation plan. Additionally, the packages of each project can have additional compilation options that will apply only to the compilation of that package. 

Below there is a more detailed example. Having the following project descriptor:

```yaml
build:
  packages:
    package1:
      cflags: ['-DPACKAGE1_DEFINE']
    package2:
      cflags: ['-DPACKAGE2_DEFINE']
  cflags: ['-DBUILD_DEFINE']
test:
  cflags: ['-DTEST_DEFINE']
targets:
  default:
    build:
      cflags: ['-DDEFAULT_TARGET_DEFINE']
  ubuntu:
    build:
      cflags: ['-DUBUNTU_TARGET_DEFINE']
```

Then, the following set of compilation options apply:

| command line | package | cflags used for the package files | 
| `cpm build` | `package1` | `-DPACKAGE1_DEFINE -DBUILD_DEFINE -DDEFAULT_TARGET_DEFINE` |
| `cpm build` | `package2` | `-DPACKAGE2_DEFINE -DBUILD_DEFINE -DDEFAULT_TARGET_DEFINE` |
| `cpm test` | `package1` | `-DPACKAGE1_DEFINE -DBUILD_DEFINE -DDEFAULT_TARGET_DEFINE  -DTEST_DEFINE` |
| `cpm build ubuntu` | `package1` | `-DPACKAGE2_DEFINE -DBUILD_DEFINE -DUBUNTU_TARGET_DEFINE` |

Packages are the most basic compilation unit. This is required as different packages can have different cflags. When generating the `CMakeLists.txt` file, cpm creates an object library for each package. Then, the final compilation step consists in combining the different object libraries, each one corresponding to a package, to form the final target binaries.

## Mixing C and C++ Files

While C and C++ source code can be mixed, some of the compilation flags used in the command line are incompatible. In order to solve this problem, cpm will create a different object library for C and C++ files inside the same package. `cflags` and `cppflags` are mutually exclusive, so that the C files will be compiled using `cflags` and the C++ using `cppflags`.

```yaml
build:
  packages:
    package1:
      cflags: ['-DC_DEFINE']
      cppflags: ['-DCPP_DEFINE']
```

| package | language | compilation flags used |
| `package1` | `C` | `-DC_DEFINE` |
| `package1` | `C++` | `-DCPP_DEFINE` |

## Bit Compilation

Bits are themselves cpm projects, so the compilation is similar. One of the things to take into account is that, unless the bit compilation is customized, the compilation flags of the project do not affect the compilation flags of the bit. Let's see this with an example. 

Suppose we have the following project:

```yaml
build:
  packages:
    package1:
  cflags: ['-DBUILD_DEFINE']
  bits:
    sqlite3: 'latest'
targets:
  default:
    build:
      cflags: ['-DDEFAULT_TARGET_DEFINE']
```

Then imagine the bit has the following `project.yaml`:

```yaml
build:
  packages:
    sqlite3_package:
  cflags: ['-DBUILD_DEFINE']
targets:
  default:
    build:
      cflags: ['-DDEFAULT_BIT_TARGET_DEFINE']
  ubuntu:
    build:
      cflags: ['-DUBUNTU_BIT_TARGET_DEFINE']
```

Then, the following set of compilation options apply:

| command line | package | cflags used for the package files | 
| `cpm build` | `sqlite3_package` | `-DBUILD_DEFINE -DDEFAULT_BIT_TARGET_DEFINE` |

### Customized Bit Compilation

It's possible to customize parts of the compilation of the bit packages by adding additional `cflags` and selecting the `target` that we want to use from the bit. 

Suppose we modify the project descriptor as follows:

```yaml
build:
  packages:
    package1:
  cflags: ['-DBUILD_DEFINE']
  bits:
    sqlite3:
      version: 'latest'
      cflags: ['-DEXTRA_BIT_CFLAG']
      target: 'ubuntu'
targets:
  default:
    build:
      cflags: ['-DDEFAULT_TARGET_DEFINE']
```

Then, the following set of compilation options apply:

| command line | package | cflags used for the package files | 
| `cpm build` | `sqlite3_package` | `-DBUILD_DEFINE -DEXTRA_BIT_CFLAG -DUBUNTU_BIT_TARGET_DEFINE` |

## Include Directories

Apart from being the basic compilation unit, packages also define the set of include directories. When a package is declared, the parent directory of the package is added to the include paths used during compilation. For example, if we declare a package `cpm-hub/bits`, then the directory `cpm-hub` will be added to the include directories. This allows then including the package header files starting from the package name. If we have a file `cpm-hub/bits/Class.h` inside a package declared as `cpm-hub/bits`, then the way to include the file is `#include <bits/Class.h>`.

## Testing

When testing, cpm builds one binary per test suite, that is, one binary per each `test_*.cpp` file. The main purpose of doing so is the ability to support mocking functions in C code. In C, it's not really easy to mock the functionality, as we don't have classes readily available. Instead, we can re-define symbols, so that we can replace certain functions with mocks. If we had a single binary for all the tests, mocking a function would replace the implementation for all the test suites. Having multiple binaries allow us to mock different functions on different test suites.
