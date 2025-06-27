import click

@click.group() # turns a function (main) into  a commmand group - top lvl CLI command
def main():
    """Notes CLI - Organize your thoughts!"""
    pass

@main.command() # registers a new subcommand under a command group (main)
@click.argument("name") # adds positional argument to the CLI (name becomes required argument the user must pass in the terminal)
def greet(name):
    """Say hello to someone."""
    click.echo(f"Hello, {name}!") # this is the CLI print function

@main.command() # turns regular function into a CLI command
@click.argument("title")
@click.argument("body")
def add(title, body):
    """Add a new new note."""
    click.echo(f"Added note titled '{title}' with body: '{body}'")

@main.command()
@click.argument("note_id", type=int)
def delete(note_id):
    """Delete a note by ID."""
    click.echo(f"Deleted note #{note_id}")
