"""
A Bazel shim for executing pytest.

By default, the `py_test` bazel rule (https://bazel.build/reference/be/python#py_test)
will simply run the test module. In the `unittest` world, typically every module
will have:

```python
if __name__ == "__main__":
    unittest.main()
```

so tests actually get run during `bazel test`.

However, this project uses `pytest` as a test runner and test modules don't
have `if __name__ == "__main__":` code in them, so when `bazel test` runs,
nothing actually happens.

This shim gets added to all `pytest_test` rules and set to bazel's `main`, so
it's what gets executed when a pytest file is "run" with `bazel test`.
"""
import sys

import pytest

if __name__ == "__main__":
    exit_code = pytest.main(sys.argv[1:])
    sys.exit(exit_code)
