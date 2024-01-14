# Bazel Tools

This dir contains helpers and shims used by bazel.

It's a central location for storing things that can be used by all bazel BUILD
files.

For this project, we use it to define the pytest shim that executes `pytest`
on the project and the `pytest_test` bazel rule.

Other uses may include:

+ A shim for setting environment variables
+ Special build rules
+ Uhh... Other things


## What's In Here?

+ `BUILD`: The bazel build file that exports `pytest_shim.py` so that every
  other BUILD file can use it.
+ `defs.bzl`: Kinda like a bazel config file. Defines the `pytest_test` rule
  as a wrapper around the `py_test` rule.
+ `pytest_shim.py`: A python module that gets set as the main entry point
  when running `pytest_test` rules.
+ `README.md`: This file.
