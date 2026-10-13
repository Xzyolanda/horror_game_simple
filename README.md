# The Night Shift

**The Night Shift** is a short, command-line horror text adventure written in Python. You play a night-shift hotel employee investigating an ordinary-looking hotel whose records do not always match what you see.

Explore the Reception, Corridor, Staff Room, and Room 409. Move between locations, inspect objects, read the staff handbook, and decide how much attention to give the inconsistencies in the hotel's records. Your discoveries affect which ending the game reaches.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/) (recommended), or standard Python virtual-environment tools

## Clone the project

Replace `<repository-url>` with this repository's Git URL:

```sh
git clone <repository-url>
cd Horror_Game
```

## Run with uv

From the project root:

```sh
uv run python -m horror_game.main
```

`uv` reads the project's configuration and runs the game as a Python module. Running `main.py` directly will not work because the project uses package-relative imports.

## Run with a virtual environment

If you do not use `uv`:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --editable .
python -m horror_game.main
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Playing

At each prompt, enter a destination ID to move, such as:

```text
corridor
staff_room
room_409
reception
```

Other available commands include:

```text
interact          # Inspect objects in the current location
rules             # Read all handbook rules after obtaining the handbook
rule <rule_id>    # Read one handbook rule, for example: rule rule_003
quit              # Exit the game
```

The game ends automatically when you return to Reception after investigating Room 409, or when you follow the Room 409 path far enough to trigger its alternate ending.


```
