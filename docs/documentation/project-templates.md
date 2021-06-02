---
layout: documentation
title: project-templates
---

# Project Templates

Starting from cpm version 1.7.0, project templates are supported. A cpm project can be created from a template. Such template will be downloaded from cpm-hub, provided it exists. A project can be created from a template as follows:

```bash
cpm create -t arduino-uno:0.2.0 project-from-template
```

The above command will download the `arduino-uno` template from cpm-hub and create a project based on it. When the project is created, the template `project.yaml` will be edited to set the project name and the project version. 

## Publishing your project as a cpm template

The project templates infrastructure is quite similar to the bit infrastructure. Any cpm project can be published as a template. In order to publish a template, publish the project using the `-t` flag:

```bash
cpm publish -t -s https://repo.cpmbits.com:8000
```

When publishing a project template, the project descriptor, its packages, the `main.cpp` file and the dockerfiles in use (if any) will get published.

