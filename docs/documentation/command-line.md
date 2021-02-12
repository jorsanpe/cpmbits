---
layout: documentation
title: command-line
---
The command line is structured around commands, similar to what you can find in other tools (e.g. Git):

```bash
cpm <action> [options]
```

## Built-in Actions

### `create`
Create a new cpm project. This command is intended for creating new cpm projects from scratch.

**SYNOPSIS**
```bash
cpm create <project_name>
```

<div class="divider" data-content=""></div>

### `init`
Initialize the current directory as a new cpm project. This command is intended for creating cpm projects from existing sources.

**SYNOPSIS**
```bash
cpm init <project_name>
```

<div class="divider" data-content=""></div>

### `build`
Build cpm project. The build command creates a CMake recipe in the project root directory. It then calls `cmake` and `ninja` to build the project using the `build` directory for the output files. The output binary will have the same name as the `project_name` field in the project descriptor and it will be placed in the project root directory.

**SYNOPSIS**
```bash
cpm build [<target>]
```

**OPTIONS**

  `<target>` The target option allows you to compile the application for a specific target. When this option is not specified, `cpm` will use the installed compiler. If this option is specified, then `cpm` will download the corresponding image from the [cpmbits docker repositories](https://hub.docker.com/orgs/cpmbits/repositories) as long as the target is available. The docker images are prepared to compile applications for the particular targets pointed by their names. 

**EXAMPLE**

```bash
cpm build ubuntu:20.04
cpm build raspberrypi4:64
```

<div class="divider" data-content=""></div>

### `test`
Compile and run project tests. If no files or dirs are specified, tests will be found recursively starting from the `tests` directory, located in the project root. The tests compilation recipe are placed in the directory `recipes/tests` which is also used during the compilation process. For each test suite found, an executable file with the same name will be built and run.

**SYNOPSIS**
```bash
cpm test [files or dirs]
```
  
**OPTIONS**

  `<pattern>...` The pattern option allows you to run only the tests contained in the test files that match the pattern. Multiple patterns can be specified.

<div class="divider" data-content=""></div>

### `clean`
Clean cpm project. The clean command basically removes the `recipes` directory, effectively removing any CMake recipes built and all compilation caches.

**SYNOPSIS**
```bash
cpm clean
```

### `publish`
Publish a cpm project as a bit in cpm-hub. The publish command packs the project and uploads it to the cpm-hub bit repository.

**SYNOPSIS**
```bash
cpm publish -s <repository-url>
```

<div class="divider" data-content=""></div>

### `install`
Install all the bits declared in the project descriptor, upgrading/downgrading the bits as required. Installed bits will be installed into the `bits` directory.

**SYNOPSIS**
```bash
cpm install
```

<div class="divider" data-content=""></div>

### `prep`

This command is useful for integration with some IDEs. It generates the would-be CMakeLists.txt recipe so that the IDE can use it as an input for indexing and other related functionalities.

**SYNOPSIS**
```bash
cpm prep
```
