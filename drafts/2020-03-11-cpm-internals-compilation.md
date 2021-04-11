---
layout: post
title: "cpm Internals: Compilation"
author: Jordi Sánchez
---

* Packages are the basic compilation unit
* Each package is compiled separately, generating an object library
* The CMakeLists.txt file is custom-tailored for the selected build target -> need clean project before switching targets
* Each test is compiled as a different application
* When declaring a package, cpm will add the parent folder to the include directories.
