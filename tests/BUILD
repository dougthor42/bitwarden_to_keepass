load("//tools/bazel:defs.bzl", "pytest_test")
load("@rules_python//python:defs.bzl", "py_binary", "py_test")
load("@pypi//:requirements.bzl", "requirement")

filegroup(
    name = "test_data",
    srcs = glob([
        "data/*",
    ]),
)

py_library(
    name = "__init__",
    srcs = ["__init__.py"],
    deps = [],
)

py_library(
    name = "conftest",
    srcs = ["conftest.py"],
    deps = [
        requirement("pytest"),
    ],
)

pytest_test(
    name = "test_main",
    srcs = ["test_main.py"],
    deps = [
        # To reference something defined in another BUILD file, prefex with
        # "//". Note that the path is relative to the top-level WORKSPACE.
        "//src/bitwarden_to_keepass:main",
        # Reference to current BUILD file
        ":__init__",
        ":conftest",
        requirement("pykeepass"),
        requirement("pytest"),
    ],
    data = [":test_data"],
)
