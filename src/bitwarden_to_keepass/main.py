"""
"""
import os
import pathlib
import subprocess
from contextlib import contextmanager
from typing import Dict
from typing import Iterator

from bitwarden_to_keepass import logger

# Names of environment variables.
BW_MASTER_PASSWORD_ENV = "BW_MASTER_PW"
BW_CLIENTID_ENV = "BW_CLIENTID"  # From BW docs
BW_CLIENTSECRET_ENV = "BW_CLIENTSECRET"  # From BW docs
BW_SESSION_ENV = "BW_SESSION"
KEEPASS_PASSWORD_ENV = "KEEPASS_PASSWORD"


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


@contextmanager
def bw_login() -> Iterator[None]:
    """
    Context manager that logs into Bitwarden on entry and logs out on exit.

    Uses the env vars BW_CLIENTID and BW_CLIENTSECRET, as specified in the
    Bitwarden CLI docs.
    """
    logger.info("Logging into Bitwarden")

    try:
        login = ["bw", "login", "--apikey"]
        subprocess.run(login, check=True)
        yield
    finally:
        logger.info("Logging out")
        logout = ["bw", "logout"]
        subprocess.run(logout, check=True)


@contextmanager
def bw_unlock(password_env: str = BW_MASTER_PASSWORD_ENV) -> Iterator[str]:
    """
    Context manager that unlocks a bitwarden vault and yields the session key.

    Vault is locked upon exiting the CM.

    Args:
        + password_env: The name of the environment variable that stores the
          Bitwarden master password.
    """
    logger.info("Unlocking vault")

    try:
        unlock = ["bw", "unlock", "--passwordenv", password_env]
        result = subprocess.run(unlock, capture_output=True, check=True)
        logger.info("Sucessfully unlocked vault.")
        # There's a line like `$ export BW_SESSION="..."` - grab that.
        session_key = grab_session_key(result.stdout)
        yield session_key
    finally:
        logger.info("Locking vault")
        lock = ["bw", "lock"]
        subprocess.run(lock, check=True)


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


def bw_export(file: pathlib.Path):
    """
    Calls the bitwarden CLI `export` command.

    Args:
        + file: The file to save the export to.
    """

    args = ["bw", "export", "--output", str(file), "--format", "json"]

    org = None
    if org:
        args.extend(["--organizationid", org])

    with bw_login():
        with bw_unlock() as session_key:
            os.environ[BW_SESSION_ENV] = session_key
            logger.info(args)
            output = subprocess.run(args, capture_output=True)
            if output.returncode == 0:
                logger.info(output)
            else:
                logger.warning(output)


def run_backup(
    master_password: str,
    keepass_password: str,
    client_id: str,
    client_secret: str,
    keepass_file: pathlib.Path,
    group: str,
):
    """
    Run the backup.
    """
    # Set a bunch of env vars
    new_env_vars = {
        BW_MASTER_PASSWORD_ENV: master_password,
        BW_CLIENTID_ENV: client_id,
        BW_CLIENTSECRET_ENV: client_secret,
        BW_SESSION_ENV: "",
        KEEPASS_PASSWORD_ENV: keepass_password,
    }
    with temp_env(new_env_vars):
        logger.warning("Debug - would export.")
        bw_export(pathlib.Path("foo.json"))
        #  add_to_keepass()
