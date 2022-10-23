import os

import pytest

from bitwarden_to_keepass import main


# A copy-paste from the `bw unlock` command with fake session key.
STDOUT = b"""
? Master password: [hidden]
Your vault is now unlocked!

To unlock your vault, set your session key to the `BW_SESSION` environment variable. ex:
$ export BW_SESSION="foobar1234"
> $env:BW_SESSION="foobar1234"

You can also pass the session key to any command with the `--session` option. ex:
$ bw list items --session foobar1234
"""


def test_grab_session_key():
    want = "foobar1234"
    got = main.grab_session_key(STDOUT)
    assert got == want


def test_grab_session_key_raises():
    with pytest.raises(ValueError):
        main.grab_session_key(b"foobar")


def test_temp_env():
    user = os.environ["USER"]
    home = os.environ["HOME"]
    with main.temp_env({"USER": "xxx", "HOME": "42", "NONEXISTENT": "?"}):
        os.environ["SHOULD_EXIST"] = "foobar"
        assert os.environ["USER"] == "xxx"
        os.environ["USER"] = "yyy"
        assert os.environ["USER"] == "yyy"
        assert os.environ["HOME"] == "42"
        assert os.environ["NONEXISTENT"] == "?"
    assert os.environ["USER"] == user
    assert os.environ["HOME"] == home
    assert "NONEXISTENT" not in os.environ
    assert "SHOULD_EXIST" in os.environ
    os.environ.pop("SHOULD_EXIST", None)
