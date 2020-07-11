# CPM: A Modern Tool for C/C++

Unlike other more modern languages, C/C++ does not have a unified centralized tool for package and project management. Take for example `pip`; this tool offers an ecosystem from which developers can greatly benefit. It speeds up development, as dependencies are just one command away, without the need for complex installation recipes or hunting for repositories. Python is not the only one to offer a "dependency hub"; others like Java, Ruby or JavaScript also have their own ecosystems.

The main goal of CPM is to offer an ecosystem for C/C++ developers. It is composed of two main ingredients: the command line tool and the bits repository.

## A Tutorial

CPM is written in Python 3.7. It can be installed using `pip`:

```
pip install cpm-cli
```

The command line tool is not a build system, it's an orchestrator, so two additional tools are required in order to compile the project sources. First, CPM generates compilation recipes for <a href="https://cmake.org" target="_blank" rel="noopener">CMake</a>. Second, it uses the CMake <a href="https://ninja-build.org" target="_blank" rel="noopener">Ninja</a> generator. Needless to say that a C/C++ compiler is also required. CPM does not rely on any particular version of the aforementioned tools, so if you install the latest version of each you should be good to go.

## Creating a new Project

Creating a new project is straightforward:

```
cpm create awesome-project
```

The newly created project includes a hello world template that can be built right away:

```
cd awesome-project
cpm build
```

New projects are created with sample "Hello World" code. The build files are placed in the `build` folder so in order to run the compiled project:

```
./build/awesome-project
Hello World!
```

Let's take a look at the project contents. Right now, they are:

```
project.yaml
main.cpp
```

The `project.yaml` file is the project descriptor and it contains the project configuration as defined by the user. The `main.cpp` file is the program entry point and at the time of writing this tutorial it is required to be at the project root (the reasons for this are beyond the scope of this tutorial).

### Packages

Projects in CPM are structured around <strong>packages</strong>. A package is a collection of (hopefully) related code that can be addressed from the package root. They try to be analogous to Python or Java packages. Let's see how they work with an example of a package named `authentication`.

First, we have to create the package root directory:

```
mkdir authentication
```

Second, we have to declare the package in the project descriptor:

```
name: awesome-project
packages:
    authentication:
```

Finally, let's create an `Authenticator` class belonging to that package:

```
authentication/Authenticator.cpp
authentication/Authenticator.h
```

By design, both source and header files are placed in the same directory. Now, imagine that we want to make use of the `Authenticator` class. In order to do so, we need to include the class header from elsewhere:

```
#include <authentication/Authenticator.h>
```

CPM will automatically solve the include directories required to make this work. Packages can be declared at any level. For example, if the package root directory is not contained directly under the root directory:

```
domain/authentication/Authenticator.cpp
domain/authentication/Authenticator.h
```

The project descriptor would be:

```
name: awesome-project
packages:
    domain/authentication:
```

And the usage would still be the same:

```
#include <authentication/Authenticator.h>
```

Nesting packages (packages inside other packages) is currently not supported.

### Bits

Bits are the way to share code with CPM. Bits are shared as source code and installed in the directory `bits`. Bits should not be included as part of the project repository. 

There are two ways in which you can install a bit. First, you can simply install them from command line. Let's say we want to install the <a href="https://cestframework.com/" rel="noopener" target="_blank">Cest</a> plugin. Cest is a testing framework installed as a header only plugin.

```
cpm install cest
```

After having run this command, the project structure is updated:

```
main.cpp
project.yaml
authentication/Authenticator.cpp
authentication/Authenticator.h
bits/cest/plugin.yaml
bits/cest/cest/cest.h
```

This is a fast way of installing a dependency. However, the dependency is not recorded anywhere so if someone else downloads your project, the bit dependencies will not be known. In order to keep track of the project dependencies, the bits can be declared in the project descriptor:

```
name: awesome-project
packages:
    domain/authentication:
bits:
    cest: '1.0'
```

The bits declared in the project descriptor can be installed all at once using the following command from the project root:

```
cpm install
```

This command will detect which bits are not installed and will automatically download and install them. 

### Test Bits

Projects can depend on bits only for testing purposes. In this case, those bits can be declared as `test_bits`:

```
name: awesome-project
packages:
    domain/authentication:
test_bits:
    cest: '1.0'
```

This is particularly useful when developing bits. When installing a bit, the dependencies will be installed transitively. For example, if the project depends on bit A and bit A depends on bit B, then CPM will install transitively bit B when installing bit A. Imagine that now, bit A depends on <a href="https://cestframework.com/" rel="noopener" target="_blank">Cest</a> for testing. We don't want that dependency to permeate through to our project so bit A should declare `Cest` as a `test_bit`.

### Testing

CPM is Test Driven Development ready. 
