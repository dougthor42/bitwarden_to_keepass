load("@rules_python//python:defs.bzl", "py_binary")
load("@pypi//:requirements.bzl", "requirement")

py_library(
    name = "__init__",
    srcs = ["__init__.py"],
    deps = [],
)

py_library(
    name = "main",
    srcs = ["main.py"],
    deps = [
        ":__init__",
        requirement("pykeepass"),
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "cli",
    srcs = ["cli.py"],
    deps = [
        ":main",
        requirement("click"),
    ],
)
