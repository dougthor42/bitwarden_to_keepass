"""
Command line interface definition.

Run `bitwarden_to_keepass --help` for details.
"""
import pathlib

import click

from bitwarden_to_keepass import main


@click.command
@click.option(
    "--master-password",
    envvar=main.BW_MASTER_PASSWORD_ENV,
    prompt="Bitwarden Master Password",
    hide_input=True,
    help=(
        "Your Bitwarden master password. Will prompt if not given."
        f" Can also be provided as the env var '{main.BW_MASTER_PASSWORD_ENV}'."
    ),
)
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
@click.option(
    "--org-id",
    envvar=main.BW_ORG_ID_ENV,
    default="",
    help=(
        "The Bitwarden Organization ID to export. If not given, only the user's"
        " vault is exported."
        f" Can also be provided as the env var '{main.BW_ORG_ID_ENV}'."
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
    master_password: str,
    keepass_password: str,
    org_id: str,
    client_id: str,
    client_secret: str,
    keepass_file: pathlib.Path,
    group: str,
) -> None:
    print("CLI entry point")
    main.run_backup(
        master_password=master_password,
        keepass_password=keepass_password,
        client_id=client_id,
        client_secret=client_secret,
        organization_id=org_id,
        keepass_file=keepass_file,
        group=group,
    )
