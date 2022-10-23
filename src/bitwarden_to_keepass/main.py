"""
"""
from bitwarden_to_keepass import logger


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
