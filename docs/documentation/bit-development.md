---
layout: documentation
title: bit-development
---

# Bit Development

Every bit published in the cpmbits repository is a cpm project. This means that at any point in time, you can publish your project as a bit in the repository, provided you have an account.

## Create your cpmbits Account

Go to the [cpmbits registration page](https://cpmbits.com/registration_page.html){:target="_blank"} and create an account. Once you verify your email, you're set to go.

## How cpm bits are Published

Name and version are the way bits are uniquely identified. At the time of this writing, cpm bit names are globally unique, which means that if some user publishes a bit with a certain name, no other user will be able to publish a bit with the same name. We have plans to remove this limitation in the future and allow different users to publish bits with the same name, much like different users can create Github repositories with the same name.

Every bit version can be published only once. This is a must in order to allow users trust the versions of the bits they are using.

## Version numbering

For the time being, cpm allows publishing versions using a custom formatting, similar to but not completely compatible with [SemVer](https://semver.org/){:target="_blank"}. We're targetting full compliance with SemVer in the future. For the time being, following are valid version numbers:

```
2020            # <number>
2020.4          # <number>.<number>
4.5.32          # <number>.<number>.<number>
3.2.23-alpha    # <number>.<number>.<number>-<alphanumeric>
```

## Publishing your project as a cpm bit

Use the following command of the cpm cli:

```bash
cpm publish -s https://repo.cpmbits.com:8000/bits
```

cpm will prompt for your user and password and then will proceed to package your project and publish it in the cpmbits repository. By providing the URL, we allow users to publish different bits in different repositories (therefore supporting custom cpm-hub installations).

