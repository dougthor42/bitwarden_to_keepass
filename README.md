# Bitwarden to KeePass

A simple little script that backs up a Bitwarden vault to a local KeePass file.


## Installation and Usage

1.  Install the Bitwarden CLI.
2.  Install the KeePass CLI.
3.  Install this code.


### Install the Bitwarden CLI

1.  Head to the [Bitwarden CLI page][bw-cli] page and download the native executable
    for your system.
2.  Place this file somewhere in your `PATH`. For example, on Linux you might
    download it to `/usr/local/bin`. Make sure that the file is executable (eg:
    `chmod a+x /usr/local/bin/bw`).

For convenience, you can use this command to do all of the above (on Linux)

```console
wget https://github.com/bitwarden/cli/releases/download/v1.22.1/bw-linux-1.22.1.zip \
&& sudo unzip -d /usr/local/bin bw-linux-1.22.1.zip \
&& sudo chmod a+x /usr/local/bin/bw
```


### Install the KeePass CLI

We use [this CLI for KeePass][kp-cli].

```console
sudo apt install kpcli \
  && wget https://cfhcable.dl.sourceforge.net/project/kpcli/kpcli-3.8.1-1.deb \
  && sudo dpkg -i ./kpcli-3.8.1-1.deb
```

... Actually I don't know if that will work. That's an interactive CLI
and we need something more script-friendly.

Maybe [pykeepass](https://github.com/libkeepass/pykeepass) instead.


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


## Changelog

See [CHANGELOG.md](./CHANGELOG.md).


[bw-cli]: https://bitwarden.com/help/cli/
[kp-cli]: https://kpcli.sourceforge.io/
