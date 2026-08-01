# Fantasy Hop

A small fantasy-themed platformer built with Python and pygame. Play as a
little wizard hopping around and exploring a grassy level under a gradient
sky. Every visual — the character, the terrain tiles, the clouds and hills —
is drawn procedurally in code, so the game has **no external asset files**
and runs from a single script.

## Features

- Smooth platforming physics (gravity, jumping, per-axis collision)
- A scrolling camera that follows the player through the level
- Fully procedural art — no images to download or bundle
- Packages into a single standalone `.exe` with no dependencies for players

## Controls

| Action | Keys |
| ------ | ---- |
| Move   | Arrow keys or `A` / `D` |
| Jump   | `Space`, `Up`, or `W` |

## Requirements

- Python 3.12 (pygame does not yet ship stable builds for Python 3.14)
- pygame 2.6.1

## Running from source

~~~
py -3.12 -m pip install pygame
py -3.12 fantasy_hop.py
~~~

## Building a standalone Windows .exe

~~~
py -3.12 -m pip install pyinstaller
py -3.12 -m PyInstaller --onefile --windowed fantasy_hop.py
~~~

The executable is created at `dist/fantasy_hop.exe` and runs without Python
installed. Because all art is generated in code, there are no asset files to
bundle — the single exe is fully self-contained.

> On first launch, Windows SmartScreen may warn about an unknown publisher
> since the exe isn't code-signed. Choose **More info → Run anyway**.

## Project structure

~~~
fantasy_hop.py    Main game: game loop, physics, level layout, procedural art
~~~

## Customizing

- **Level:** the `platforms` list defines the layout. Add more `make_row(...)`
  lines to expand the area to explore.
- **Feel:** tweak `GRAVITY`, `JUMP_STRENGTH`, and `MOVE_SPEED` near the top.
- **Art:** the `make_player()`, `make_tile()`, and `make_background()`
  functions build the sprites from simple shapes and colors.

## License

Released under the MIT License. See `LICENSE` for details.