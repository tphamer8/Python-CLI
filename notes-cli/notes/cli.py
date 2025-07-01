import click
from notes.cli_state import cli_state
import json
import os
from pydantic import BaseModel

@click.group() # turns a function (main) into  a commmand group - top lvl CLI command
@click.option("--file", type=click.Path(), default="notes.json", help="Path to notes file")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def main(file, verbose):
    """Notes CLI - Organize your thoughts!"""
    cli_state.file = file
    cli_state.verbose = verbose
    pass

def load_notes():
    if not os.path.exists(cli_state.file): # check if notes file exists
        return [] # makes empty list 
    with open(cli_state.file, "r") as f: # with keyword automatically closes the file
        return json.load(f)

def save_notes(notes):
    with open(cli_state.file, "w") as f: # 'f' is the file object
        json.dump(notes, f, indent=2) # write python data to a file in JSON format

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
    notes = load_notes() # loads existing notes
    note_id = max([n["note_id"] for n in notes], default=0) + 1 # gets the next available note_id
    notes.append({"note_id": note_id, "title": title, "body": body}) # adds note to json file
    save_notes(notes)
    click.echo(f"Added note titled '{title}' with body: '{body}'")

@main.command()
@click.argument("note_id", type=int)
def delete(note_id):
    """Delete a note by ID."""
    notes = load_notes()

    # new_notes = [n for n in notes if n["note_id"] != note_id] # Filters out the deleted note 
    new_notes = []
    found = False

    for n in notes:
        if n["note_id"] == note_id:
            found = True
            continue # skip deleted note
        elif n["note_id"] > note_id: # notes after the deleted
            n["note_id"] -= 1
        new_notes.append(n)

    if not found:
        click.echo(f"Note #{note_id} not found. ❌")
    else:
        save_notes(new_notes)
        click.echo(f"Deleted note #{note_id} 🗑️")

@main.command()
def list():
    """List all notes by ID and title."""
    notes = load_notes()

    if not notes:
        click.echo("No notes found.")
        return
    
    click.echo("Notes:")
    for note in notes:
        click.echo(f"{note['note_id']} . {note['title']}")

@main.command()
def clear():
    """Deletes all notes"""
    save_notes([])

def find_note(note_id):
    
    notes = load_notes()
    index = note_id - 1
    length = len(notes)

    if 1 <= index < length: # Check if not exists
        return notes[index]
    else:
        click.echo("Note not found.")
        return

@main.command()
@click.argument("note_id")
def display(note_id):
    """Display a note by ID."""

    notes = load_notes()

    if note_id.lower() == "all":
        if not notes:
            click.echo("No notes found.")
        for note in notes:
            click.echo(f"{note['note_id']} . {note['title']} : {note['body']}")
    else:
        try:
            note_id = int(note_id)
        except ValueError:
            click.echo("Invalid note ID. Use an integer or 'all'.")
            return
        
        note = find_note(note_id)
        if note:
            click.echo(f"{note['note_id']} . {note['title']} : {note['body']}")

@main.command()
@click.argument("note_id", type=int)
@click.argument("body")
def bodyr(note_id, body):
    """Replace note body"""
    notes = load_notes()
    index = note_id - 1

    if 0 <= index < len(notes):
        notes[index]['body'] = body
        save_notes(notes)
        click.echo(f"Replaced body – {notes[index]['note_id']} . {notes[index]['title']} : {notes[index]['body']}")
    else:
        click.echo("Note not found.")

@main.command()
@click.argument("note_id", type=int)
@click.argument("body")
def bodya(note_id, body):
    """Append to note body"""
    notes = load_notes()
    index = note_id - 1

    if 0 <= index < len(notes):
        notes[index]['body'] += ", " + body
        save_notes(notes)
        click.echo(f"Appended body – {notes[index]['note_id']} . {notes[index]['title']} : {notes[index]['body']}")
    else:
        click.echo("Note not found.")




