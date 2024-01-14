# Name the workspace
workspace(name = "bitwarden-to-keepass")

# Install rules_python, which allows us to define how bazel should work with python files.
# See https://rules-python.readthedocs.io/en/latest/getting-started.html#using-a-workspace-file
# Note: These "##### START ... #####" comments are just my own - they do not have
#   any meaning in bazel.
##### START install rules_python snippet (https://github.com/bazelbuild/rules_python/releases/tag/0.28.0) #####
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "d70cd72a7a4880f0000a6346253414825c19cdd40a28289bdf67b8e6480edff8",
    strip_prefix = "rules_python-0.28.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.28.0/rules_python-0.28.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()
##### END install rules_python snippet #####


# Use a hermetic python rather than relying on a system-installed interpreter:
# See https://rules-python.readthedocs.io/en/stable/getting-started.html#toolchain-registration
##### START hermetic python snippet #####
load("@rules_python//python:repositories.bzl", "py_repositories", "python_register_toolchains")

py_repositories()

python_register_toolchains(
    name = "python3_8",
    # Available versions are listed in @rules_python//python:versions.bzl.
    # We recommend using the same version your team is already standardized on.
    python_version = "3.8.18",
    # Support coverage. See https://rules-python.readthedocs.io/en/stable/coverage.html
    register_coverage_tool = True,
)

load("@python3_8//:defs.bzl", interpreter = "interpreter")
##### END hermetic python snippet #####


# Install dependencies from PyPI.
# See https://rules-python.readthedocs.io/en/stable/pypi-dependencies.html#using-a-workspace-file
# and https://rules-python.readthedocs.io/en/stable/pip.html
##### START install python dependencies snippet #####
load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "pypi",
    python_interpreter_target = interpreter,  # From hermetic python snippet
    # TODO: Can requirements come from pyproject.toml?
    requirements_lock = "//:requirements_lock.txt",
)

load("@pypi//:requirements.bzl", "install_deps")

install_deps()
##### END install python dependencies snippet #####
