---
layout: documentation
title: cross-compilation
---

# Cross Compilation

One of cpm's main goals is to simplify cross-compilation. cpm provides flexibility to support several ways of cross-compiling a project.

## Targets

Each time you build a cpm project, it is built for a specific **target**. Targets are labeled with a **target name**. A target name is just an alias provided by the project developer and can be any string. Targets must not be confused with platforms (see next section). A target is something that is *specific to the project*, and its name can be anything that the developer deems meaningful. This is important when dealing with dependencies, as the `targets` section of the bits are ignored.

cpm always has a target named *default*. When no target is specified in the command line, cpm will follow the build instructions configured under `default` in the `targets` section of the project descriptor.

```yaml
name: 'project'
version: 0.0.1
...
targets:
  default:
    main: 'main.cpp'
```

You can create more targets by adding more sections to the `targets`. For example, if you want to declare a target named `raspberrypi4`:

```yaml
name: 'project'
version: 0.0.1
...
targets:
  default:
    main: 'main.cpp'
  raspberrypi4:
    main: 'main.cpp'
```

## Platforms (Work in Progress)

The platforms part is Work in Progress and is not available. Refer to the [GitHub issue](https://github.com/jorsanpe/cpm/issues/230){:target="_blank"} that is tracking this feature for more information.


## Cross-compiling using a Docker image

Using a Docker image is the most straight forward way of cross-compiling a cpm project, assuming you already have one ready. 

There are a number of [Docker images available at Docker hub](https://hub.docker.com/u/cpmbits){:target="_blank"} that you can use for cross-compiling cpm projects. Some targets available as of writing this document are Ubuntu, Raspberry Pi 4 64-bit, Arduino and AWS Lambda. Some of them require some modifications to the project descriptor in order to work.

Let's see with an example how to cross-compile your project for Raspberry Pi 4 64-bit. First, add the configuration option to the project descriptor. In this case, we're going to use the `cpmbits/raspberrypi4:64` Docker image:

```yaml
name: 'project'
version: 0.0.1
...
targets:
  default:
    main: 'main.cpp'
    image: 'cpmbits/raspberrypi4:64'  # Configured here
```

That's it. Now, when you build your project, it'll generate a Raspberry Pi 4 64-bit compatible binary (this particular Docker image is a bit heavy, around 2GB, so the first time you compile using this image will take some time):

```bash
$ cpm build
pulling cpmbits/raspberrypi4:64
...
$ file build/project 
build/project: ELF 64-bit LSB executable, ARM aarch64 ...
```

In the above example, we have defined the image to be used when compiling for the `default` target.

## Cross-compiling using a Dockerfile

Instead of using pre-built images, you can create a Dockerfile with the necessary instructions for building the Docker image on the fly. This method of cross-compiling the project is almost equal to the previous one, except the instructions for building the Docker image are provided by the user.

When building using a Dockerfile, the Docker build directory will be the same as the project directory.

```yaml
name: 'project'
version: 0.0.1
...
targets:
  default:
    main: 'main.cpp'
    dockerfile: 'Dockerfile'  # Configured here
```

Dockerfiles cannot be combined with Docker images in the project descriptor as they are mutually exclusive (either you use a Dockerfile or a pre-built Docker image). When both are specified, `image` will be used.

## Considerations when using Docker images

When using a Docker image, cpm generates the `CMakeLists.txt` file outside the container. Then, it runs the container and runs the `cmake` + `ninja` commands inside it. This is intended to avoid having the images depend on cpm or any of its dependencies.

A second consideration is that the Docker containers created during the compilation process are ephemeral, and they are removed once the compilation has finished.

## Cross-compiling configuring the compiler prefix

You can also specify the toolchain prefix in the project descriptor. This alternative can be used in combination with a Docker image. In this case, cpm will prepend the toolchain prefix configuration to the toolchain tools by defining the `CMAKE_C_COMPILER` and `CMAKE_CXX_COMPILER` settings in the `CMakeLists.txt` file.

```yaml
name: 'project'
version: 0.0.1
...
targets:
  default:
    main: 'main.cpp'
    toolchain_prefix: 'arm-linux-gnueabihf-'  # Configured here
```
