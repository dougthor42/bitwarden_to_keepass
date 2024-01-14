# Bitwarden to KeePass

A simple little script that backs up a Bitwarden vault to a local KeePass file.

```console
$ bitwarden_to_keepass --keepass-file /path/to/file.kdbx
```


## Installation and Usage

1.  Install the Bitwarden CLI.
2.  Install this code.
3.  Run.


### Install the Bitwarden CLI

1.  Head to the [Bitwarden CLI page][bw-cli] page and download the native executable
    for your system.
2.  Place this file somewhere in your `PATH`. For example, on Linux you might
    download it to `/usr/local/bin`. Make sure that the file is executable (eg:
    `chmod a+x /usr/local/bin/bw`).

For convenience, you can use this command to do all of the above (on Linux)

```console
wget https://github.com/bitwarden/clients/releases/download/cli-v2023.7.0/bw-linux-2023.7.0.zip \
&& sudo unzip -d /usr/local/bin bw-linux-2023.7.0.zip \
&& sudo chmod a+x /usr/local/bin/bw
```


### Install this code

```console
pip install bitwarden-to-keepass
```

Or see [Development](#development).


### Run

Run `bitwarden_to_keepass`.

You'll be prompted for all the secrets and whatnot. Each secret arg has an
associated env var (see `bitwarden_to_keepass --help` for env var names). If
that env var is found, the value from the env var will be used and you will
not be prompted.

You can also send in your secrets via command line, though this is not
recommended.

Personally I like to create a `secrets.sh` file:

```shell
#!/bin/bash
export BW_MASTER_PW=<Bitwarden master password>
export BW_CLIENTID=<Bitwarden API Client ID>
export BW_CLIENTSECRET=<Bitwarden API Client Secret>

# If you also want to backup your Organization data:
export BW_ORG_ID=<Organization ID>
```

and source it before running:

```console
$ source secrets.sh
$ bitwarden_to_keepass --keepass-file /c/foo/bar.kdbx
```

It might be useful to put everything into a script:

```shell
#!/bin/bash
# run.sh
echo "Activating venv"
source .venv/bin/activate
echo "Setting env vars"
source secrets.sh
echo "Running"
bitwarden_to_keepass --keepass-file "/path/to/file.kdbx"
echo "Removing files"
rm bitwarden_*export_*.json
echo "Deactivating venv"
deactivate
```

```console
$ ./run.sh
```


## Development

Install the Bitwarden CLI and the KeePass CLI as mentioned above.

1.  Clone the repo: `git clone https://github.com/dougthor42/bitwarden_to_keepass`
2.  Move into that dir: `cd bitwarden-to-keepass`
3.  Create a virtual environment: `python -m venv .venv`
4.  Activate it: `. .venv/bin/activate`
5.  Install python packages:
    1.  `pip install -U pip setuptools wheel`
    2.  `pip install -e .[dev]`
6.  Run tests to verify: `pytest`
7.  Install pre-commit hooks: `pre-commit install`
8.  Ready to develop


### Releasing

1.  Update `CHANGELOG.md` by inserting a new heading:
    ```diff
    --- a/CHANGELOG.md
    +++ b/CHANGELOG.md
    @@ -3,6 +3,9 @@

     ## Unreleased

    +
    +## v1.0.0 (2023-01-14)
    +
     + Finally decided to work on this again and got things to decent working state!
       This should be usable now and ticks all of the original requirements.
    ```

2.  Update pyproject.toml with the new version:
    ```diff
    --- a/pyproject.toml
    +++ b/pyproject.toml
    @@ -4,7 +4,7 @@ build-backend = "setuptools.build_meta"

     [project]
     name = "bitwarden_to_keepass"
    -version = "0.0.1"
    +version = "1.0.0"
     description = "A simple little script that backs up a Bitwarden vault to a local KeePass file."
     readme = "README.md"
     requires-python = ">=3.8"
    ```
3.  Commit these changes.
4.  Create a new git tag `git tag v1.0.0 -m "Release v1.0.0"`.

Then push tags to github. CI will build the source distribution and wheel and
upload them to PyPI.


### Bazel

I'm experimenting with [`bazel`][bazel] for running tests (and perhaps also compiling
a binary in the future).

First, install `bazel`:

```console
$ source setup_bazel.sh
```

To run tests:

```console
$ bazel test //tests:test_main
```

If a test fails, you'll see something like:

```
INFO: Build completed, 1 test FAILED, 2 total actions
//tests:test_main                                                        FAILED in 1.7s
  /home/dthor/.cache/bazel/_bazel_dthor/7076d176777da645a0c7cf0359126a31/execroot/_main/bazel-out/k8-fastbuild/testlogs/tests/test_main/test.log

  Executed 1 out of 1 test: 1 fails locally.
```

To see the logs of that test, open that file in `less` or whatever you prefer:

```console
$ less bazel-out/k8-fastbuild/testlogs/tests/test_main/test.log
```

There are a couple other CLI args that might be useful:

+ `--test_output=streamed`: Run tests serially and show the output of pytest.

To build (though note that this doesn't fully work yet):

```console
$ bazel build //src/bitwarden_to_keepass:cli
```


## Changelog

See [CHANGELOG.md](./CHANGELOG.md).


[bw-cli]: https://bitwarden.com/help/cli/
[bazel]: https://bazel.build/
