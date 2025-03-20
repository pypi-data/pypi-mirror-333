"""CLI (Command Line Interface) of OE Python Template."""

from enum import StrEnum
from typing import Annotated

import typer
import uvicorn
import yaml
from rich.console import Console

from oe_python_template import Service, __version__
from oe_python_template.api import app as api

console = Console()

cli = typer.Typer(name="Command Line Interface of OE Python Template")


@cli.command()
def echo(
    text: Annotated[
        str, typer.Argument(help="The text to echo")
    ] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    json: Annotated[
        bool,
        typer.Option(
            help=("Print as JSON"),
        ),
    ] = False,
) -> None:
    """Echo the text."""
    if json:
        console.print_json(data={"text": text})
    else:
        console.print(text)


@cli.command()
def hello_world() -> None:
    """Print hello world message and what's in the environment variable THE_VAR."""
    console.print(Service.get_hello_world())


@cli.command()
def serve(
    host: Annotated[str, typer.Option(help="Host to bind the server to")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Port to bind the server to")] = 8000,
    watch: Annotated[bool, typer.Option(help="Enable auto-reload")] = True,
) -> None:
    """Start the API server."""
    console.print(f"Starting API server at http://{host}:{port}")
    uvicorn.run(
        "oe_python_template.api:app",
        host=host,
        port=port,
        reload=watch,
    )


class OutputFormat(StrEnum):
    """
    Enum representing the supported output formats.

    This enum defines the possible formats for output data:
    - YAML: Output data in YAML format
    - JSON: Output data in JSON format

    Usage:
        format = OutputFormat.YAML
        print(f"Using {format} format")
    """

    YAML = "yaml"
    JSON = "json"


@cli.command()
def openapi(
    output_format: Annotated[
        OutputFormat, typer.Option(help="Output format", case_sensitive=False)
    ] = OutputFormat.YAML,
) -> None:
    """Dump the OpenAPI specification to stdout (YAML by default)."""
    schema = api.openapi()
    match output_format:
        case OutputFormat.JSON:
            console.print_json(data=schema)
        case OutputFormat.YAML:
            console.print(yaml.dump(schema, default_flow_style=False), end="")


def _apply_cli_settings(cli: typer.Typer, epilog: str) -> None:
    """Add epilog to all typers in the tree and configure default behavior."""
    cli.info.epilog = epilog
    cli.info.no_args_is_help = True
    for command in cli.registered_commands:
        command.epilog = cli.info.epilog


_apply_cli_settings(
    cli,
    f"🧠 OE Python Template v{__version__} - built with love in Berlin 🐻",
)


if __name__ == "__main__":
    cli()
