import pathlib
import click
from .server import server as _server
from .get import get as _get
from .shutdown import shutdown as _shutdown
from hakisto.click import (
    hakisto_inline_location,
    hakisto_severity,
    hakisto_short_trace,
    hakisto_process_all,
    hakisto_use_color,
)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@hakisto_severity()
@hakisto_use_color()
@hakisto_short_trace()
@hakisto_inline_location()
@click.pass_context
def main(ctx, **kwargs):
    """Keepass utilities"""
    hakisto_process_all(**kwargs)
    ctx.ensure_object(dict)


@main.group()
@click.option("-p", "--port", type=int, default=8666, help="Port (default: 8666)")
@click.pass_context
def server(ctx, port):
    """Rest server"""
    ctx.obj["port"] = port


@server.command()
@click.option("-p", "--passphrase", prompt=True, hide_input=True, help="Passphrase")
@click.option(
    "-k",
    "--keyfile",
    type=click.Path(exists=True, dir_okay=False, readable=True, allow_dash=False, path_type=pathlib.Path),
    help="Keyfile",
)
@click.argument(
    "filename", type=click.Path(exists=True, dir_okay=False, readable=True, allow_dash=False, path_type=pathlib.Path)
)
@click.pass_context
def start(ctx, passphrase, filename, keyfile):
    """Start Server at PORT listening to 127.0.0.1 (localhost)."""
    _start(filename=filename, passphrase=passphrase, keyfile=keyfile, port=ctx.obj["port"])


def _start(filename: pathlib.Path, passphrase: str, keyfile: pathlib.Path, port: int = 8666):
    """Start Server"""
    _server(filename=filename, password=passphrase, keyfile=keyfile, port=port)


@server.command()
@click.option(
    "-s",
    "--secret",
    type=click.Path(exists=True, dir_okay=False, readable=True, allow_dash=False, path_type=pathlib.Path),
    help="File with encrypted secret",
)
@click.option(
    "-k",
    "--keyfile",
    type=click.Path(exists=True, dir_okay=False, readable=True, allow_dash=False, path_type=pathlib.Path),
    help="Keyfile",
)
@click.argument(
    "filename", type=click.Path(exists=True, dir_okay=False, readable=True, allow_dash=False, path_type=pathlib.Path)
)
@click.pass_context
def start_secret(ctx, secret, filename, keyfile):
    """Start Server at PORT listening to 127.0.0.1 (localhost) using SECRET file."""
    from ..crypt import read

    passphrase = read(secret)
    _start(filename=filename, passphrase=passphrase, keyfile=keyfile, port=ctx.obj["port"])


@server.command()
@click.pass_context
def shutdown(ctx):
    """Shutdown server at PORT"""
    print(_shutdown(port=ctx.obj["port"]))


@server.command()
@click.argument("path")
@click.argument("property")
@click.pass_context
def get(ctx, path, property):
    """
    Retrieve PATH from local REST server and print content of PROPERTY.
    """
    print(_get(path=path, property=property, port=ctx.obj["port"]))
