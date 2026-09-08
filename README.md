# Pama

This is a simple accounts manager.

Frontend (i.e. package `tkinter_GUI` or simple cli at `paman/__init__.py`) interacts with `service`, and `utils` packages.

## Running the app

Checkout `pyproject.toml` `[project.scripts]` and `[project.gui-scripts]` sections (i.e., run `pama_tk` order)

## UI

### CLI
 
CLI coming from `pama/__init__.py`. run `pama` with args.

Typing passwords / keys at cli persist at shell history. Take care, use environment variables or enter keys during script execution·

### GUI With tkinter

Package `tkinter_GUI` has a secondary daemon thread used for async calls to service - database. Other GUIs doesn't need this.

run `pama_tk.`

## Settings

Edit `settings` package in order to connect with other databases (even create and use a .env or config.ini file). Default db is local SQLite db.




