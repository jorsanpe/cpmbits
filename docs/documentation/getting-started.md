---
layout: documentation
title: getting-started
---
## Installation

```bash
pip3 install cpm-cli
```

CPM depends on [CMake](https://cmake.org/) and [ninja](https://ninja-build.org/) for the build process.

## Create a Project
```bash
cpm create DeathStartLaserBackend
cd DeathStartLaserBackend
cpm
build
```

After creating the project, the binary will be available in the project root directory. 

```bash
./DeathStartLaserBackend
```

## Manage dependencies

CPM manages your project dependencies through CPM-Hub. In order to install a bit, first declare the dependency in the project descriptor like this:

```yaml
build:
  bits:
    sqlite3: '3.32.3'
```

Then install the project bits with

```bash
cpm install
```

## Run your tests

```bash
cpm test
```

Test sources reside in the `tests` directory. They are found recursively from the root directory
 using the expression `test_*.cpp`.
