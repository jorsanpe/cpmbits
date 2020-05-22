# What is CPM

CPM is born as a tool for the modernization of C and C++ based projects. Modern languages have strong development frameworks and really amazing project management tools. Combined with CPM Hub, CPM will provide an ecosystem for creating projects in a much easier way, reducing the high entrance fee required for developing in multi-target environments. It will provide the means for sharing plugins (note that we're not using the term libraries) via source code.

### Ease of Use

Many of the features that are/will be avaiable in CPM come from other more modern languages and frameworks like NPM or Python. CPM will try to close the gap with those modern frameworks and bring that ease of use to C and C++ project.

### Use on any major OS

As this page is being written, CPM has been tested in MAC OS X and Linux. Development on Windows is pending review but it's also a target development platform. Other platforms are not currently considered.

### Performance

Being compiled languages, C and C++ can provide the best possible performance for a given workload. In some cases, this can allow running heavy loads 

### Multiple Targets

One of the main design goals of CPM is to have a tool that will allow compiling for any platform. The plugin ecosystem will provide the means to develop software for many combinations of Operating System / Architecture. Custom actions will allow users to share target-specific build scripts that could be used to develop software for many platforms (e.g. Arduino).

### Seamless Development

As long as the code is not platform / architecture dependent, the developer will be able to easily compile the project for different systems. For example, the same project could be compiled for Raspbian / Raspberry PI 3 or for a Ubuntu Docker container running on a x86_64.
