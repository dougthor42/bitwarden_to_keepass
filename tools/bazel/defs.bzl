load("@rules_python//python:defs.bzl", _py_test = "py_test")
load("@pypi//:requirements.bzl", "requirement")

def pytest_test(name, srcs, deps, **kwargs):
    """
    A bazel rule for running python tests via pytest.

    Usage:
        ```bazel
        pytest_test(
            name = "test_main",
            srcs = ["test_main.py"],
            deps = [
                # The module to test
                "//src/my_package:main",
                # Still need to include pytest. See TODO below.
                requirement("pytest"),
            ],
        )
        ```
    """
    if "main" in kwargs:
        fail("Can't set 'main' - we set it in pytest_test rule definition.")

    shim = "//tools/bazel:pytest_shim.py"

    # TODO: We can automagically update the deps if we want. For now, to make
    #   sure I understand bazel, I won't be doing that.
    # deps =

    # Include the shim as a source.
    all_srcs = [shim] + srcs

    _py_test(
        name = name,
        srcs = all_srcs,
        main = shim,
        # TODO: What's this 'location'?
        args = ["$(location {})".format(src) for src in srcs],
        # Within bazel, `$HOME` is typically set to $TEST_TMPDIR`, but it looks
        # like there's a bug? https://github.com/bazelbuild/bazel/issues/10652
        # So we inject it manually.
        # TODO: Don't point to root, point to $TEST_TMPDIR instead.
        env = {"HOME": "/"},
        deps = deps,
        **kwargs,
    )
