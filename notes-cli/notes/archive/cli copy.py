import click
import json
import os

NOTES_FILE = "notes.json"

def load_notes():
    if not os.path.exists(NOTES_FILE): # check if notes file exists
        return [] # makes empty list 
    with open(NOTES_FILE, "r") as f: # with keyword automatically closes the file
        return json.load(f)

def saves_notes(notes):
    with open(NOTES_FILE, "w") as f: # 'f' is the file object
        json.dump(notes, f, indent=2) # write python data to a file in JSON format

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
    notes = load_notes() # loads existing notes
    note_id = max([n["note_id"] for n in notes], default=0) + 1 # gets the next available note_id
    notes.append({"note_id": note_id, "title": title, "body": body}) # adds note to json file
    saves_notes(notes)
    click.echo(f"Added note titled '{title}' with body: '{body}'")

@main.command()
@click.argument("note_id", type=int)
def delete(note_id):
    """Delete a note by ID."""
    notes = load_notes()

    # new_notes = [n for n in notes if n["note_id"] != note_id] # Filters out the deleted note 
    new_notes = []

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
        saves_notes(new_notes)
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
        click.echo(f"{note['note_id']}. {note['title']}")

@main.command()
def clear():
    """Deletes all notes"""
    saves_notes([])


@main.command()
@click.argument("note_id", type=int)
def display(note_id):
    """Display a note by ID."""
    notes = load_notes()
    # found = False

    left = 0
    right = len(notes)

    # Binary Search
    while left <= right:
        mid = (left+right) // 2
        current_id = notes[mid]['note_id']

        if note_id < current_id:
            right = mid - 1
        elif note_id > current_id:
            left = mid + 1
        else:
            note = notes[mid]
            click.echo(f"{note['note_id']} . {note['title']} : {note['body']}")
            return
        
    click.echo("Note not found.")
    return

def find_note(note_id):
    notes = load_notes()
    left = 0
    right = len(notes)
    if note_id > right:
        return -1

    # Binary Search
    while left <= right:
        mid = (left+right) // 2
        current_id = notes[mid]['note_id']

        if note_id < current_id:
            right = mid - 1
        elif note_id > current_id:
            left = mid + 1
        else:
            note = notes[mid]
            return note

    click.echo("Note not found.")


