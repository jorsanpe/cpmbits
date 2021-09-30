---
layout: documentation
title: project-structure
---

# Project Structure

cpm offers a lot of flexibility for organizing the project sources. You can take [cpm-hub](https://github.com/jorsanpe/cpm-hub){:target="_blank"} for a reference project based on cpm.

A cpm project has:
 - The project descriptor file `project.yaml`.
 - One or more `main.cpp` files (depending on the project targets).
 - The `bits` directory, where the project dependencies are installed for the time being.
 - The project tests. By default, they are expected to be located in the directory of the same name.
 - The project packages. Nested packages are not supported for the time being.

For reference, this is how a cpm project could be structured:

```
Project/
    main.cpp
    project.yaml
    package/
        code.cpp
        code.h
    tests/
        test_suite.cpp
    bits/
        cest/
            project.yaml
            cest/
                cest.h
```

### `project.yaml`

The project description is stored in this file following the [cpm project descriptor structure](/documentation/project-descriptor.html). This file contains the description of the project, the packages that compose the source code, the `bits` it depends on and the rules for specific targets.

### `main.cpp`

The `main.cpp` files contains the `main` function of the application. They are kept separate from the project packages in order to enable testing, as testing frameworks will normally implement their own `main` functions. The file containing the `main` function is configured per project.

## Packages

Packages allow the user to structure the code however needed. By design, we're removing the `src <-> include` separation. Instead, source code and header files are stored next to each other, creating a proper structure for packages. A _package_ in cpm is the root of a set of source files with no particular structure. The package sources are found recursively from the package root. Nested packages are not supported.

Using packages is pretty straightforward. First, package your code however you require:

```
Project/
    api/
        api.cpp
        api.h
```

Second, declare the packages in `project.yaml`:

```yaml
project_name: 'cpm-hub'
description: 'cpm-hub open source server for hosting cpm software'
build:
  packages:
    api:
      cflags: 
        - -std=c++11
```

Each entry in `packages` is the path to the package, followed by a dictionary of properties for that package. This section is under development so, for now, only the `cflags` property is implemented. The `cflags` property allows the developer to specify compilation flags for each package. The properties defined to the package will be applied to all the source files of the package.

Once the package has been created, the parent path of the package will be included with '-I' flag. This way, a package like the one declared above can be used in the code with:

```c
#include <api/api.h>
```

## Bits

cpm `bits` are the main way of sharing code between cpm projects. All bits are installed under the `bits` directory. That directory should not be included as part of the project VCS, as it's automatically managed by `cpm`. 

## Tests

When testing, cpm will find for files matching the `test_*.cpp` pattern and will consider them as test suites. Each test suite will be compiled separately as a binary application and run. cpm leaves the choice of the testing framework to the developer.

cpm is developed jointly with cpm-hub, which is both the bits repository and the first cpm project. In turn, cpm-hub is using [cest](https://github.com/cegonse/cest){:target="_blank"}, so there's good synergy between them. 

