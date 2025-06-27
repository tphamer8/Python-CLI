import click

@click.command() # turns regular function into a CLI command
@click.argument("name") # adds positional argument to the CLI (name becomes required argument the user must pass in the terminal)

def main(name):
    """Say hello to someone."""
    click.echo(f"Hello, {name}!") # this is the CLI print functino