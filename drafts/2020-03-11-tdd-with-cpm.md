---
layout: post
title: "The Fizzbuzz Kata with cpm"
author: Jordi Sánchez
---

* Install cest bit
* Create test file
* Include cest header
* Create first test
* Compile and fail
* Continue

## Test Bits

Projects can depend on bits only for testing purposes. In this case, those bits can be declared as `test_bits`:
 
```yaml
name: awesome-project
build:
  packages:
    math/multiplication:
test:
  bits:
    cest: '1.0'
```

This is particularly useful when developing bits. When installing a bit, the dependencies will be installed transitively. For example, if the project depends on bit A and bit A depends on bit B, then cpm will install transitively bit B when installing bit A. Imagine that now, bit A depends on <a href="https://cestframework.com/" rel="noopener" target="_blank">Cest</a> for testing. We don't want that dependency to permeate through to our project so bit A should declare `Cest` as a `test_bit`.
