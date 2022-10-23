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
