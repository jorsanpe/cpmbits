# Project Descriptor {.title}

The project descriptor is a YAML file with the name `project.yaml` that contains the description of the different elements of the application. A folder containing this file with the proper schema will be identified as a CPM project.

<br/>

## Elements of the project descriptor {.subtitle .is-3}

<br/>

### `name: string` {.subtitle .is-4}

The project name field is a string identifying the project. The application will be compiled into a binary file with this name. The `name` should not contain any spaces.

<br/>

### `description: string` {.subtitle .is-4}

This field has currently no practical purpose other than allowing the user to include a larger description of the project.

<br/>

### `version: string` {.subtitle .is-4}

This field is required when the current project is intended to be published in CPM Hub. The version will be used to publish the plugin accordingly. When not present, the `version` field defaults to `"0.1"`.

<br/>

### `packages: object` {.subtitle .is-4}

This section contains the list of packages of the project. A `package` in CPM is the root directory of a set of source files. For example, when declaring an `api` package, CPM will recursively search `*.c` and `*.cpp` source files in the directory with that name.

<br/>

### `packages.{name}: object` {.subtitle .is-4}

Each package has to be declared in the `packages` section with the same name as its root folder. For example, for declaring the `api/json` directory as a package, the project descriptor should be:

```
packages:
    api/json:
```

<br/>

### `packages.{name}.cflags: [string]` {.subtitle .is-4}

Packages can be assigned specific compilation flags with the `cflags` property. This allows, among other things, mixing C99 and C++11 code in the same executable.

<br/>

### `bits: object` {.subtitle .is-4}

This section is used to declare which `bits` the project depends on. The entries in the `bits` section will be used to access CPM Hub and download the declared version of each bit when updating the project.

<br/>

### `compile_flags: [string]` {.subtitle .is-4}

This property allows the user to configure the global compilation options. This flags will only apply to the project sources.

<br/>

### `link_options: object` {.subtitle .is-4}

This property allows the user to define the link options of the binary.

<br/>

### `link_options.libraries: [string]` {.subtitle .is-4}

The libraries section contains a list of strings, each one describing a library that must be used during the final link process. This list translates into a CMake `target_link_libraries` option with the list expanded.

<br/>

### `actions: object` {.subtitle .is-4}

The user can define project specific actions in this section.

<br/>

### `actions.{name}: string` {.subtitle .is-4}

Each key in the actions section is the action alias. The value is a string with the command to be executed for that action:

```
actions:
    deploy: "echo Deploy!"
```

<br/>

## Sample file {.subtitle .is-3}

```yaml
project_name: 'PortalGunFirmware'
description: 'Project description'
packages:
    - api:
        cflags: ['-std=c++11']
    - domain:
    - infrastructure:
        cflags: ['-std=c++11']
bits:
    - cest: '1.0'
    - mongoose: '6.16'
    - json: '3.7.3'
    - fakeit: '2.0.5'
link_options:
    libraries: ['pthread']
actions:
    deploy: 'echo Deploy!'
```

