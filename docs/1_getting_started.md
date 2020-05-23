## Installation

```
pip3 install cpm-cli
```

CPM depends on [CMake](https://cmake.org/) and [ninja](https://ninja-build.org/) for the build process.

## Create a Project

```
cpm create DeathStartLaserBackend
cd DeathStartLaserBackend
cpm build
```

After creating the project, the binary will be available in the project root directory. 

```
./DeathStartLaserBackend
```

## Manage dependencies

CPM manages your project dependencies through CPM-Hub. In order to install a package, simply run:

```
cpm install cest
```

### Run your tests

```
cpm test
```

Test sources reside in the `tests` directory. They are found recursively from the root directory
 using the expression `test_*.cpp`.
