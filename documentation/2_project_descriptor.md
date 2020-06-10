The project descriptor is a YAML file with the name `project.yaml` that contains the description of the different elements of the application. A folder containing this file with the proper schema will be identified as a CPM project.

## Elements of the project descriptor

| Parameter        | Description     |
| ---------------- | --------------- |
| `name: string`   | The project name field is a string identifying the project. The application will be compiled into a binary file with this name. The `name` should not contain any spaces. |
| `description: string`      | This field has currently no practical purpose other than allowing the user to include a larger description of the project. |
| `version: string` | This field is required when the current project is intended to be published in CPM Hub. The version will be used to publish the plugin accordingly. When not present, the `version` field defaults to `"0.1"`. |
| `packages: [object]` | This section contains the list of packages of the project. A `package` in CPM is the root directory of a set of source files. For example, when declaring an `api` package, CPM will recursively search `*.c` and `*.cpp` source files in the directory with that name. |
| `packages.{name}: object` | Each package has to be declared in the `packages` section with the same name as its root folder. |
| `packages.{name}.cflags: [string]` | Packages can be assigned specific compilation flags with the `cflags` property. This allows, among other things, mixing C99 and C++11 code in the same executable. |
| `bits: object` | This section is used to declare which `bits` the project depends on. The entries in the `bits` section will be used to access CPM Hub and download the declared version of each bit when updating the project. |
| `bits.{name}: string` | Each declared bit is an entry in the `bits` object with the name of the bit as the key and the bit version as the value. |
| `test_bits: object`<br>`test_bits.{name}: string` | The `test_bits` section is treated exactly the same as the `bits` section. The main difference is that, when installing a bit that has transitive dependencies, the `test_bits` won't be followed. |
| `compile_flags: [string]` | This property allows the user to configure the global compilation options. This flags will only apply to the project sources. |
| `link_options: object` | This property allows the user to define the link options of the binary. |
| `link_options.libraries: [string]` | The libraries section contains a list of strings, each one describing a library that must be used during the final link process. This list translates into a CMake `target_link_libraries` option with the list expanded. |
| `actions: object` | The user can define project specific actions in this section. |
| `actions.{name}: string` | Each key in the actions section is the action alias. The value is a string with the command to be executed for that action. |

## Sample file

<pre><code class="language-yaml">name: 'PortalGunFirmware'
description: 'Project description'
version: '1.0'
packages:
    - api:
        cflags: ['-std=c++11']
    - domain:
    - infrastructure:
        cflags: ['-std=c++11']
compile_flags: ['-g']
bits:
    mongoose: '6.16'
    json: '3.7.3'
test_bits:
    cest: '1.0'
    fakeit: '2.0.5'
link_options:
    libraries: ['pthread']
actions:
    deploy: 'echo Deploy!'
</code></pre>
