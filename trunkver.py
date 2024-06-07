import click
import os
from app import get_semver

@click.group()
def cli():
    pass

@cli.command()
@click.option("-p", "--path", type=str, help="Path of git repository (defaults to current working dir)", default="")
def run(path):
    path = path if path else os.getcwd()
    click.echo(f"Executing on path '{path}'")
    semver = get_semver(path)
    click.echo(semver)
