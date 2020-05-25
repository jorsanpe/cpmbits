# CPM: A Modern Tool for C/C++

Unlike other more modern languages, C/C++ does not have a unified centralized tool for package and project management. Take for example `pip`; this tool offers an ecosystem from which developers can greatly benefit. It speeds up development, as dependencies are just one command away, without the need for complex installation recipes or hunting for repositories. Python is not the only one to offer a "dependency hub"; others like Java, Ruby or JavaScript also have their own ecosystems.

The main goal of CPM is to offer an ecosystem for C/C++ developers. It is composed of two main ingredients: the command line tool and the plugins repository.

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

The `project.yaml</code> is the project descriptor and it contains the project configuration as defined by the user. The <code>main.cpp` file is the program entry point and at the time of writing this tutorial it is required to be at the project root (the reasons for this are beyond the scope of this tutorial).

### Packages

Projects in CPM are structured around <strong>packages</strong>. A package is a collection of (hopefully) related code that can be addressed from the package root. They are analogous to Python or Java packages. Let's see how they work with an example of a package named `authentication`.

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

CPM will automatically solve the include directories required to make this work. Packages can be declared at any level. For example, if the package is not contained directly under the root directory:

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

### Plugins

Plugins are the way to share code with CPM. The term <em>plugin</em> (as opposed to <em>library</em> or <em>package</em>) has been used on purpose in order to avoid confusion. Plugins are currently shared as source code and installed in the directory `plugins`. 

Let's say we want to install the <a href="https://cestframework.com/" rel="noopener" target="_blank">Cest</a> plugin. Cest is a testing framework installed as a header only plugin. As we'll see later, CPM has been developed with testing in mind.

```
cpm install cest
``` 

After having run this command, the project structure is updated:

```
main.cpp
project.yaml
authentication/Authenticator.cpp
authentication/Authenticator.h
plugins/cest/plugin.yaml
plugins/cest/cest/cest.h
```

### Testing

