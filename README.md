# Pama

This is a simple accounts manager.

Frontend (i.e. package `tkinter_GUI`) interacts with `service`, `cryptotools` and `utils` packages.

## Running the app

Checkout `pyproject.toml` `[project.scripts]` and `[project.gui-scripts]` sections (i.e., run `pama_tk` order)

## GUI

### With tkinter

Package `tkinter_GUI` has a secondary daemon thread used for async calls to service - database. Other GUIs doesn't need this.

## Settings

Edit `settings` package in order to connect with other databases (even create and use a .env or config.ini file). Default db is local SQLite db.




