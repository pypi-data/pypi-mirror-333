import typer
import logging
from importlib.metadata import entry_points
from importlib import import_module, metadata
from typing import Annotated, Optional
from rich.table import Table
from rich import print

app = typer.Typer(pretty_exceptions_enable=False, no_args_is_help=True, name="uphy", help="U-Phy command line tools")
LOG = logging.getLogger(__name__)

for entry_point in entry_points(group='uphy.cli'):
    try:
        module_name, _, attribute = entry_point.value.partition(":")
        module = import_module(module_name)
        command = getattr(module, attribute)
        app.add_typer(command, name=entry_point.name)
    except Exception as exception:
        LOG.warning("Ignoring entry point '%s' due to error: %r", entry_point.name, exception)

def _version_callback(value: bool):
    if value:
        dist = metadata.distribution("uphy")
        print(f"{dist.name} version: {dist.version}")

        for entry_point in entry_points(group='uphy.cli'):
            print(f"{entry_point.dist.name} version: {entry_point.dist.version}")

        raise typer.Exit()

VERSION_OPTION = typer.Option(callback=_version_callback, is_eager=True, help="Print version and exit")

@app.callback()
def main(
    version: Annotated[Optional[bool], VERSION_OPTION] = None,
):
    return

@app.command()
def build():
    """Start device builder to generate configuration files."""
    typer.launch("https://devicebuilder.rt-labs.com/")

@app.command(rich_help_panel="Extra")
def readme():
    """Open browser at main documentation site"""

    print("The main documentation site for U-Phy is located at https://docs.rt-labs.com/u-phy.")
    if typer.confirm(
        "Start a web browser navigating to site?"
    ):
        typer.launch("https://docs.rt-labs.com/u-phy")


@app.command(rich_help_panel="Extra")
def discover():
    """Tries to discovery locally attached u-phy servers"""
    import serial.tools.list_ports

    table = Table("ID", "Serial Number", "Subsystem", title="Serial ports")
    for port in serial.tools.list_ports.comports():
        LOG.debug(port.usb_info())
        if port.vid != 0x04D8 or port.pid != 0x1301:
            continue
        index = port.location.split(".")[-1]
        if index == "0":
            system = "server"
        elif index == "2":
            system = "console"
        else:
            system = "unkown"
        table.add_row(port.name, port.serial_number, system)

    print(table)

if __name__ == "__main__":
    app()
