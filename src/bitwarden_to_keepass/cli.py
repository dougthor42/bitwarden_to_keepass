"""
Command line interface definition.

Run `bitwarden_to_keepass --help` for details.
"""
import pathlib

import click

from bitwarden_to_keepass import main


@click.command
@click.option(
    "--keepass-password",
    envvar=main.KEEPASS_PASSWORD_ENV,
    prompt="KeePass Password",  # so that capitalization is correct.
    hide_input=True,
    help=(
        "The password to the KeePass database. Will prompt if not given."
        f" Can also be provided as the env var '{main.KEEPASS_PASSWORD_ENV}'."
    ),
)
# env vars from https://bitwarden.com/help/cli/#using-an-api-key
@click.option(
    "--client-id",
    envvar=main.BW_CLIENTID_ENV,
    help=(
        "The Bitwarden API client ID."
        f" Can also be provided as the env var '{main.BW_CLIENTID_ENV}'."
    ),
)
@click.option(
    "--client-secret",
    envvar=main.BW_CLIENTSECRET_ENV,
    help=(
        "The Bitwarden API client secret."
        f" Can also be provided as the env var '{main.BW_CLIENTSECRET_ENV}'."
    ),
)
@click.option(
    "--keepass-file",
    type=click.Path(exists=True, dir_okay=False, writable=True, path_type=pathlib.Path),
    help="Path to the KeePass file to add to.",
)
@click.option("--group", help="The KeePass group to add the Bitwarden backup to.")
def run(
    keepass_password: str,
    client_id: str,
    client_secret: str,
    keepass_file: pathlib.Path,
    group: str,
) -> None:
    print("CLI entry point")
