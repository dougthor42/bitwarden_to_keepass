"""
"""
import os
from contextlib import contextmanager
from typing import Dict

from bitwarden_to_keepass import logger


@contextmanager
def temp_env(new_vars: Dict[str, str]) -> Iterator[None]:
    """
    Context manager that restores env vars on exit.

    Any env vars that are added while this CM is active will continue to exist
    after exiting the CM. Env vars that are modified while this CM is active
    will be reverted to their original values.

    Modified from https://gist.github.com/igniteflow/7267431 and subsequent
    comments.

    Args:
        + new_vars: Dict of new or updated environment variables.
    """
    original_env = os.environ.copy()
    os.environ.update(new_vars)
    try:
        yield
    finally:
        # Remove any new ones.
        for key in new_vars.keys():
            os.environ.pop(key, None)  # Avoids KeyError
        # And restore the original
        os.environ.update(original_env)


def grab_session_key(text: bytes) -> str:
    """
    Grabs the Bitwarden session key from text.

    Args:
        + text: the bytes string returned by the `bw unlock` subprocess.
    """
    logger.debug("Grabbing session key")
    text_str = text.decode("utf-8")
    for line in text_str.splitlines():
        if line.startswith("$ export BW_SESSION"):
            # Simple text processing. Can upgrade to regex later if needed.
            session_key = line.split('"')[1]
            logger.info(f"Grabbed session key {session_key}")
            return session_key
    else:
        raise ValueError(f"Did not find BW_SESSION key in '{text_str}'")
