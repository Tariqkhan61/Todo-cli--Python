import click  # To Create a CLI
import json  # To save and load tasks from a file
import os  # For operating system functionalities, like checking if a file exists

# Make a constant variable for the to-do file.
TODO_FILE = "todo.json"

# Function to load tasks from the JSON file.
def load_tasks():
    if not os.path.exists(TODO_FILE):  # Corrected condition
        return []  # If the file doesn't exist, return an empty list
    with open(TODO_FILE, "r") as file:
        return json.load(file)

# Function to save tasks to the JSON file.
def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Python Decorator: Initialize the click group for our project.
@click.group()
def cli():
    """Simple Todo List Manager"""
    pass

# Command to add a new task.
@click.command()
@click.argument("task")
def add(task):
    """Add a new task to the list"""
    tasks = load_tasks()
    tasks.append({"task": task, "done": False})  # `done` defaults to False
    save_tasks(tasks)
    click.echo(f"Task added successfully: {task}")

# Command to list all tasks.
@click.command(name="list")  # Explicitly name the command 'list'
def list_tasks():
    """List all the tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks found.")
        return
    # Display tasks with their status
    for index, task in enumerate(tasks, 1):
        status = "✅" if task["done"] else "❌"
        click.echo(f"{index}. {task['task']} [{status}]")

# Command to mark a task as completed.
@click.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as completed"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):  # Fixed syntax error with colon
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as completed")
    else:
        click.echo(f"Invalid task number: {task_number}")

# Command to remove a task from the list.
@click.command()
@click.argument("task_number", type=int)
def remove(task_number):
    """Remove a task from the list"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"Removed task: {removed_task['task']}")
    else:
        click.echo(f"Invalid task number: {task_number}")

# Add the commands to the CLI group.
cli.add_command(add)
cli.add_command(list_tasks)
cli.add_command(complete)
cli.add_command(remove)

# Run the CLI application
if __name__ == "__main__":
    cli()
