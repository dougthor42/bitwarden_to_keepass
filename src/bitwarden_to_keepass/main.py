"""
"""
import datetime
import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Mapping

from pykeepass import PyKeePass

from bitwarden_to_keepass import logger

# Names of environment variables.
BW_MASTER_PASSWORD_ENV = "BW_MASTER_PW"
BW_CLIENTID_ENV = "BW_CLIENTID"  # From BW docs
BW_CLIENTSECRET_ENV = "BW_CLIENTSECRET"  # From BW docs
BW_SESSION_ENV = "BW_SESSION"
BW_ORG_ID_ENV = "BW_ORG_ID"
KEEPASS_PASSWORD_ENV = "KEEPASS_PASSWORD"

# Name of the group ("folder") in KeePass to store backups to.
KEEPASS_GROUP = "Bitwarden Backups"


@contextmanager
def temp_env(new_vars: Mapping[str, str]) -> Iterator[None]:
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


def bw_export(file: Path, org: str = "") -> None:
    """
    Calls the bitwarden CLI `export` command.

    Args:
        + file: The file to save the export to.
        + org: The organization id. If given, export the organization's vault
          instead of the user's vault.
    """

    args = ["bw", "export", "--output", str(file), "--format", "json"]

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


def local_now() -> datetime.datetime:
    """
    Return the current datetime as an aware datetime object with the system timezone.
    """
    return datetime.datetime.now(tz=datetime.timezone.utc).astimezone()


def add_to_keepass(
    keepass_file: Path, password: str, attachments: Iterable[Path] = ()
) -> None:
    """
    Add an entry to KeePass, including all attachments.

    Args:
        + keepass_file: The KeePass file to act on.
        + password: The password that unlocks the KeePass file.
        + attachments: An iterable of Paths that point to the attachments to add
          to the entry.
    """
    logger.info(f"Opening {keepass_file}")
    kp = PyKeePass(str(keepass_file), password=password)

    group = kp.find_groups(name=KEEPASS_GROUP, first=True)
    if group is None:
        logger.info(f"Group {KEEPASS_GROUP} does not exist, creating.")
        group = kp.add_group(kp.root_group, group_name=KEEPASS_GROUP)

    # Now as an aware, local TZ object.
    now = local_now().isoformat(sep=" ")
    entry_name = f"Bitwarden Backup {now}"
    logger.info(f"Entry name: '{entry_name}'")

    # They raise a base exception if the entry already exists... /facepalm
    # https://github.com/libkeepass/pykeepass/issues/293
    # So instead I changed to a full UTC timestamp (instead of just date) for
    # the name.
    entry = kp.add_entry(group, entry_name, username="", password="")

    # Add the attachment. KeePass stores the attachment as a binary in the
    # database, and then stores a link to that binary in the entry.
    for path in attachments:
        logger.info(f"Adding attachment: {path}")
        binary_data = path.read_bytes()
        filename = path.name
        binary_id = kp.add_binary(binary_data)
        entry.add_attachment(binary_id, filename)

    logger.info("Saving KP Database file")
    kp.save()


def run_backup(
    master_password: str,
    keepass_password: str,
    client_id: str,
    client_secret: str,
    organization_id: str,
    keepass_file: Path,
    group: str,
) -> None:
    """
    Run the backup.
    """
    # Set a bunch of env vars
    new_env_vars = {
        BW_MASTER_PASSWORD_ENV: master_password,
        BW_CLIENTID_ENV: client_id,
        BW_CLIENTSECRET_ENV: client_secret,
        BW_SESSION_ENV: "",
        BW_ORG_ID_ENV: organization_id,
        KEEPASS_PASSWORD_ENV: keepass_password,
    }

    attachments: List[Path] = []

    with temp_env(new_env_vars):
        now = local_now().strftime("%Y%m%d%H%M%S")
        personal_vault_file = Path(f"bitwarden_export_{now}.json")
        bw_export(personal_vault_file)
        attachments.append(personal_vault_file)

    if organization_id:
        with temp_env(new_env_vars):
            now = local_now().strftime("%Y%m%d%H%M%S")
            org_vault_file = Path(f"bitwarden_org_export_{now}.json")
            bw_export(org_vault_file, org=organization_id)
            attachments.append(org_vault_file)

    add_to_keepass(
        keepass_file,
        password=keepass_password,
        attachments=attachments,
    )
