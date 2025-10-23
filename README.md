## Todo CLI

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Stable-success.svg)](#)
[![Platform](https://img.shields.io/badge/Platform-CLI-lightgrey.svg)](#)

A simple command-line todo list manager written in Python.  
Supports adding, listing, completing, and deleting tasks, with optional priority, due dates, and categories.

## Features

- Add new tasks with optional priority and due date
- List, filter, or delete tasks
- Mark tasks as completed
- JSON-based storage

## Installation

```bash
git clone https://github.com/PaulsyWaulsy/todo.git
cd todo
```

## Usage

Run the program from the project directory:

```bash
python -m src.main [OPTIONS]
```

## Command-Line Options

| Option                                | Description                            |
| ------------------------------------- | -------------------------------------- |
| `-a`, `--add` _TEXT_                  | Add a new todo item with a description |
| `-l`, `--list`                        | List all tasks (can be filtered)       |
| `-c`, `--complete` _ID_               | Mark a task as completed               |
| `-d`, `--delete` _ID_                 | Delete a task by ID                    |
| `-C`, `--category` _NAME_             | Assign or filter by category           |
| `-p`, `--priority` _[Low, Med, High]_ | Specify or filter by priority          |
| `--due` _YYYY-MM-DD_                  | Specify a due date                     |
| `--completed`                         | Show only completed tasks              |
| `--pending`                           | Show only pending tasks                |
| `-f`, `--file` _PATH_                 | Specify a custom storage file          |
| `--debug`                             | Enable debug mode                      |
| `--version`                           | Show version information               |

## Examples

Add a new task:

```bash
todo -a "Finish Computer Science assignment" -p High --due 2025-11-01
```

List all pending tasks:

```bash
todo -l --pending
```

Filter by priority:

```bash
todo -l -p High
```

Mark a task as complete:

```bash
todo -c todo_20251023_091501
```

Delete a task:

```bash
todo -d todo_20251023_091501
```

Check version:

```bash
todo --version
```

## Storage

Tasks are stored as JSON in `data/todo.json`, with fields such as:

- `id`
- `description`
- `priority`
- `due_date`
- `category`
- `completed`
- `created_at`

