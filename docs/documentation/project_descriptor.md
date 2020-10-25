---
layout: documentation
title: getting-started
---
The project descriptor is a YAML file with the name `project.yaml` that contains the description of the different elements of the application. A folder containing this file with the proper schema will be identified as a CPM project.

## Elements of the project descriptor

<table>
  <colgroup>
    <col width="35%" />
    <col width="65%" />
  </colgroup>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>

<tr><td markdown="span"> `name: string`</td><td markdown="span"> The project name field is a string identifying the project. The application will be compiled into a binary file with this name. The `name` should not contain any spaces.</td></tr>
<tr><td markdown="span"> `description: string`</td><td markdown="span"> This field has currently no practical purpose other than allowing the user to include a larger description of the project.</td></tr>
<tr><td markdown="span"> `version: string`</td><td markdown="span"> This field is required when the current project is intended to be published in CPM Hub. The version will be used to publish the plugin accordingly. When not present, the `version` field defaults to `"0.1"`.</td></tr>
<tr><td markdown="span"> `packages: [object]`</td><td markdown="span"> This section contains the list of packages of the project. A `package` in CPM is the root directory of a set of source files. For example, when declaring an `api` package, CPM will recursively search `*.c` and `*.cpp` source files in the directory with that name.</td></tr>
<tr><td markdown="span"> `packages.{name}: object`</td><td markdown="span"> Each package has to be declared in the `packages` section with the same name as its root folder.</td></tr>
<tr><td markdown="span"> `packages.{name}.cflags: [string]`</td><td markdown="span"> Packages can be assigned specific compilation flags with the `cflags` property. This allows, among other things, mixing C99 and C++11 code in the same executable.</td></tr>
<tr><td markdown="span"> `bits: object`<br>`bits.{name}: string`</td><td markdown="span"> This section is used to declare which `bits` the project depends on. The entries in the `bits` section will be used to access CPM Hub and download the declared version of each bit when updating the project. Each declared bit is an entry in the `bits` object with the name of the bit as the key and the bit version as the value.</td></tr>
<tr><td markdown="span"> `compile_flags: [string]`</td><td markdown="span"> This property allows the user to configure the global compilation options. This flags will only apply to the project sources.</td></tr>
<tr><td markdown="span"> `link_options.libraries: [string]`</td><td markdown="span"> The libraries section contains a list of strings, each one describing a library that must be used during the final link process. This list translates into a CMake `target_link_libraries` option with the list expanded.</td></tr>
<tr><td markdown="span"> `test: object`</td><td markdown="span"> The `test` section contains test-only compilation rules.</td></tr>
<tr><td markdown="span"> `test.packages.{name}: object`</td><td markdown="span"> Packages that will be included only as part of the test compilation. This is useful when implementing utility functions or mocks for testing.</td></tr>
<tr><td markdown="span"> `test.packages.{name}.cflags: [string]`</td><td markdown="span"> Test-only packages can be assigned specific compilation flags with the `cflags` property.</td></tr>
<tr><td markdown="span"> `test.cflags: [string]`</td><td markdown="span"> Compilation flags that will affect only the test packages and the main test files themselves.</td></tr>
<tr><td markdown="span"> `test.bits: object`<br>`test.bits.{name}: string`</td><td markdown="span"> This is useful to avoid including test-only `bits` as part of the final application binary. In the case of test-only `bits`, the won't be followed when installing transitive dependencies (bits depending on other bits).</td></tr>
<tr><td markdown="span"> `test.link_options.libraries: [string]`</td><td markdown="span"> Compilation flags that will affect only the test packages and the main test files themselves.</td></tr>
<tr><td markdown="span"> `actions: object`</td><td markdown="span"> The user can define project specific actions in this section.</td></tr>
<tr><td markdown="span"> `actions.{name}: string`</td><td markdown="span"> Each key in the actions section is the action alias. The value is a string with the command to be executed for that action.</td></tr>
<tr><td markdown="span"> `targets: object`<br>`targets.{name}: object`<br>`targets.{name}.image: string`</td><td markdown="span"> The `targets` section is currently used to define a custom Docker image from which to build the application.</td></tr>
  </tbody>
</table>


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
link_options:
    libraries: ['pthread']
test:
    packages:
        tests/mocks:
    cflags: ['-O0']
    bits:
        fakeit: '2.0.5'
    link_options:
        libraries: ['cpputest']
actions:
    deploy: 'echo Deploy!'
targets:
    ubuntu:
        image: 'ubuntu:18.04'
</code></pre>
