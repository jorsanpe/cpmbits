---
layout: documentation
title: project-descriptor
---

# Project descriptor

Every cpm project is configured through the **project descriptor**, a YAML file with the name `project.yaml` located at the project root directory that contains the description of the different elements of the application. A folder containing this file with the proper schema will be identified as a cpm project.

### Project information

#### name

The name of the project, besides the obvious, is required for two things. First, when compiling the project, the project name is used to name the binary file generated. Second, the `name` and the `version` fields are required when publishing the project as a `bit` in [cpm-hub](https://github.com/jorsanpe/cpm-hub).

#### version

The `name` and the `version` are the way cpm bits are uniquely indentified in cpm-hub. Once published, it's not possible to publish again the same `name` and `version`.

#### description

This field is intended for future uses. Include here a description of the project.

#### schema

This field identifies the project descriptor schema version, as the time of writing this documentation, the only existing version is the `1.0`.

Here's an example on how to use the above items:

```yaml
name: 'Project'
version: '1.1'
description: 'The description of the project goes here'
schema: '1.0'
```

### Compilation

#### build

The `build` section includes the base *compilation plan*. It contains the information required by cpm to generate the compilation recipe for building the project. The build section compilation plan is considered to be the generic part of the compilation, common to all targets. The build section will be used also by the tests.

#### test

The `test` section includes the base *compilation plan* for testing. The base testing compilation plan is combined with the base build compilation plan for each test. It is intended to allow the user to include test-only packages, flags and dependencies.

### Compilation plan

The compilation plan includes a number of sections required for the generation of the compilation recipe.

#### packages

The package section is where the different packages of the application are defined. A *package* in the project descriptor is defined as the path to the root of the package directory. Packages are the minimum project compilation unit as defined by cpm. Each package contains a tree of source files. When defining a package, it's contents will be addressable for inclusion starting from the package folder. Each package is compiled independently. Nested packages are not supported. Here's how it works:

```yaml
name: 'Project'
build:
  packages:
    sqlite3:
```

```C++
// somefile.cpp
#include <sqlite3/...>
```

Each package can have specific `cflags` and `cppflags`.

#### cflags

The `cflags` element is used to define the compilation options for `C` files in a particular compilation unit. The `cflags` can be defined at different scopes, including generic build, generic test, package specific and target specific.

#### cppflags

The `cppflags` element is used to define the compilation options for `C++` files in a particular compilation unit. The `cppflags` can be defined at different scopes, including generic build, generic test, package specific and target specific.

#### ldflags

The `ldflags` element is used to define the options passed to the linker for a particular compilation plan.

#### libraries

The `libraries` element is included for convenience (to avoid including the libraries as `ldflags`). It is a list of strings, each containing the name of a library without the leading `lib` suffix. 

#### includes

The `includes` element allows the user to specify user-defined include directories. The list of include directories specified here will be passed to the compiler as the plain old `-I` option. This can be useful in some situations, for example, when some source code files are automatically generated, refactoring the files can be inconvenient.

#### bits

The `bits` element is used to declare the dependencies for a particular compilation plan. The `bits` element can be used in two different ways:

##### bits: string

When the `bits` section is configured as a string, the string indicates the version of the bit that our project depends on. Here's how it works:

```yaml
build:
  bits:
    base64: '1.0'
```

##### bits: dictionary

When the `bits` section is configured as a dictionary, additional options are available that allow finer grained configuration of the bit. 

###### bits.&lt;name&gt;.version

This field allows specifying the bit version to be used.

###### bits.&lt;name&gt;.target

A bit can have configuration defined for multiple targets. This field allows choosing the specific bit target to use. This is useful for certain embedded systems, like arduino, which have libraries that give support for many different platforms.

###### bits.&lt;name&gt;.cflags

When specified, all bit `C` files will be compiled using this compilation flag. This is useful for certain bits that require configuring the compilation via compilation flags.

###### bits.&lt;name&gt;.cppflags

When specified, all bit `C++` files will be compiled using this compilation flag.

Here's in summary how the bit compilation can be customized from the project descriptor:

```yaml
build:
  bits:
    ArduinoCode-mbed:
      version: '1.0'
      target: 'ArduinoNano33BLE'
      cflags: ['-O2']
```

#### Example of a Compilation Plan

Here's a complete example of a compilation plan:

```yaml
build:
  packages:
    sqlite3:
      cflags: ['-DSQLITE_MUTEX_NOOP']   # These flags apply only for the sqlite3 package
  cflags: ['-g']                        # These flags apply globally
  cppflags: ['-std=c++11']              # These flags apply globally
  ldflags: []
  libraries: ['pthread', 'ssl']
  bits:
    base64: '1.0'
    spdlog: 
      version: '1.6.1'
      cppflags: ['-DSPDLOG_COMPILED_LIB']
test:
  packages:
    tests/helpers:
  cflags: ['-O0']
  ldflags: []
  libraries: ['CppUTest', 'CppUTestExt']
  bits:
    cest: '1.0'
```

In this example:
* The application contains one package named `sqlite3`. The directory `<project_root>/sqlite3` is expected to contain the sources of the package. 
* When building the application, all source files in the `sqlite3` package will be compiled using the flags `-g -DSQLITE_MUTEX_NOOP`.
* The application will be linked agains the libraries `libpthread libssl`.
* The `spdlog` bit packages will be compiled using the bit defined flags plus the defined `-DSPDLOG_COMPILED_LIB` flag.
* When running the tests, an additional `tests/helpers` package will be included in the compilation of each test suite.
* When running the tests, all source files in the `sqlite3` package will be compiled using the flags `-g -DSQLITE_MUTEX_NOOP -O0`.
* When running the tests, each test suite will be linked against the libraries `libpthread libssl libCppUTest libCppUTestExt`.

### Targets

#### targets

The targets section contains instructions for compiling the project against a particular target. Each of the keys in the targets section refers to a particular target.

#### targets.&lt;target_name&gt;.main

Use to configure the location of the file containing the `main` function. This is useful when having different boot sequences for different targets.

#### targets.&lt;target_name&gt;.build

Each target can extend the base compilation plan with some particular compilation instructions. This is useful, for example, when a particular package should be built only when compiling for a particular target.

#### targets.&lt;target_name&gt;.image

Use this to indicate the name of a Docker image where the project will be built. This allows developers to share docker images where the toolchains and all the compilation dependencies are already installed, so complex toolchain and library setups can be avoided.

#### targets.&lt;target_name&gt;.dockerfile

Use this to indicate the path to a Dockerfile. The purpose is the same as with `targets.<target_name>.image`, but instead of downloading a pre-built docker image, cpm uses this Dockerfile to build an image on the fly and compile inside it. The `image` and `dockerfile` sections are mutually exclusive so if both are specified, `image` will be used.

#### targets.&lt;target_name&gt;.test_image

Use this to indicate the name of a Docker image where the project tests will be built and run. Similarly to the `image` configuration parameter, this allows developers to share docker images where the toolchains and all the testing dependencies are already installed.

#### targets.&lt;target_name&gt;.test_dockerfile

Use this to indicate the path to a Dockerfile. The purpose is the same as with `targets.<target_name>.test_image`, but instead of downloading a pre-built docker image, cpm uses this Dockerfile to build an image on the fly and compile and run the tests inside of it. The `test_image` and `test_dockerfile` sections are mutually exclusive so if both are specified, `test_image` will be used.

#### targets.&lt;target_name&gt;.post_build

Sometimes, the result of the build process will be not be the final deployable artifact. The `post_build` action allows the user to specify a list of shell commands that will be automatically run by cpm *within the compilation context*. Notice that this implies that when using a Docker image for compiling, the post-build action will be executed *inside the container*, and *the working directory will be the project root*.

#### targets.&lt;target_name&gt;.toolchain_prefix

The `tolchain_prefix` allows the user to specify the toolchain to be used for compiling the target. This gives the user full control over the location of the toolchain. This parameter is optional for cross compiling the project, but can be useful some scenarios. For example, one scenario would be having the toolchain installed in the host, thus not requiring the use of Docker for cross compiling. Another use could be to have multiple toolchains installed in a single Docker image, so that the same image can be used for compiling all required targets, thus reducing maintenance.

Notice that the `toolchain_prefix` will be prepended to the compiler name so the final dash must be specified (see example below).

```yaml
targets:
  default:
    main: 'main.cpp'
    image: 'cpmbits/raspberrypi4:64'
    test_dockerfile: 'ubuntu.20.04.Dockerfile'
    post_build: 'objcopy -S build/binary'
    toolchain_prefix: 'arm-linux-gnueabihf-'
```

## Sample file

The following corresponds to the project descriptor used in [cpm-hub](https://github.com/jorsanpe/cpm-hub).

```yaml
name: 'cpm-hub'
version: '1.0.0'
description: 'cpm-hub open source server for hosting cpm bits'
build:
  packages:
    cpm-hub/http:
    cpm-hub/infrastructure:
    cpm-hub/management:
    cpm-hub/bits:
    cpm-hub/users:
    cpm-hub/authentication:
    cpm-hub/logging:
    cpm-hub/kpi:
    cpm-hub/database:
  cppflags: [ '-std=c++11', '-g' ]
  bits:
    mongoose: '6.16'
    json: '3.7.3'
    base64: '1.0'
    blake3: '1.0'
    inih: '1.0'
    spdlog: 
      version: '1.6.1'
      cppflags: ['-DSPDLOG_COMPILED_LIB']
    sqlite3: '3.32.3'
  libraries: [ 'boost_filesystem', 'boost_system', 'boost_program_options', 'pthread', 'ssl', 'crypto' ]
test:
  packages:
    tests/mocks:
  bits:
    fakeit: '2.0.5'
    cest: '1.0'
  libraries: [ 'CppUTest', 'CppUTestExt' ]
targets:
  default:
    main: 'main.cpp'
```
