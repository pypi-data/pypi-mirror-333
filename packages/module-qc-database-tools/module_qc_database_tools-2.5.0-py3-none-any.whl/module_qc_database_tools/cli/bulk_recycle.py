from __future__ import annotations

import logging

import typer
from rich import print as rich_print

from module_qc_database_tools.cli.globals import CONTEXT_SETTINGS, OPTIONS, Protocol
from module_qc_database_tools.cli.utils import get_dbs_or_client
from module_qc_database_tools.recycle import recycle_component

app = typer.Typer(context_settings=CONTEXT_SETTINGS)
log = logging.getLogger(__name__)


@app.command()
def main(
    serial_number: str = OPTIONS["serial_number"],
    ssl: bool = OPTIONS["ssl"],
    mongo_serverSelectionTimeout: int = OPTIONS["mongo_serverSelectionTimeout"],
    mongo_uri: str = OPTIONS["mongo_uri"],
    localdb_name: str = OPTIONS["localdb_name"],
    userdb_name: str = OPTIONS["userdb_name"],
    host: str = OPTIONS["host"],
    port: int = OPTIONS["port"],
    protocol: Protocol = OPTIONS["protocol"],
):
    """
    Main executable for bulk recycling a module entirely.

    !!! note "Added in version 2.5.0"

    """
    # pylint: disable=duplicate-code
    client, _ = get_dbs_or_client(
        localdb=True,
        ssl=ssl,
        mongo_serverSelectionTimeout=mongo_serverSelectionTimeout,
        mongo_uri=mongo_uri,
        localdb_name=localdb_name,
        userdb_name=userdb_name,
    )

    localdb_uri = f"{protocol.value}://{host}:{port}/localdb/"

    try:
        status, results = recycle_component(
            client, serial_number, localdb_uri=localdb_uri
        )
    except ValueError as exc:
        rich_print(f":warning: [red bold]Error[/]: {exc}")
        raise typer.Exit(2) from exc

    if not status:
        rich_print(
            ":error: [red bold]Error[/]: one of the test results could not recycle"
        )
        rich_print(results)
        raise typer.Exit(1)

    rich_print("[green]All done.[/]")


if __name__ == "__main__":
    typer.run(main)
