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
Create a new CPM project. This command is intended for creating new CPM projects from scratch.

**SYNOPSIS**
```bash
cpm create <project_name>
```

<div class="divider" data-content=""></div>

### `init`
Initialize the current directory as a new CPM project. This command is intended for creating CPM projects from existing sources.

**SYNOPSIS**
```bash
cpm init <project_name>
```

<div class="divider" data-content=""></div>

### `build`
Build CPM project. The build command creates a CMake recipe in the project root directory. It then calls `cmake` and `ninja` to build the project using the `build` directory for the output files. The output binary will have the same name as the `project_name` field in the project descriptor and it will be placed in the project root directory.

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
Clean CPM project. The clean command basically removes the `recipes` directory, effectively removing any CMake recipes built and all compilation caches.

**SYNOPSIS**
```bash
cpm clean
```

### `publish`
Publish a CPM project as a bit in CPM Hub. The publish command packs the project and uploads it to the CPM Hub bit repository.

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

### `update`
This command is useful for integration with some IDEs. It generates the would-be CMake recipe so that the IDE can use it as an input for indexing and any other related functionalities.

**SYNOPSIS**
```bash
cpm update
```

## Project Actions

The user can define project specific actions in the project descriptor. This is done through the `actions` section described in the [project descriptor](/documentation/project-descriptor.html). Actions defined there will appear in the command line.
