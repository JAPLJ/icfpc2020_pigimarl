# ICFPC2020 Team Pigimarl

This is a git repository by the team "Pigimarl" for ICFPC 2020.

There are several `submissions/***` branches used for submissions during the contest. Among them, the submission `submissions/FINAL_PIGIMARL` is selected to play the final stage. The final submission branch is now merged to `master` so that you can see whole source codes which will be used in the final stage. It contains not only AIs for the game but also a galaxy interpreter and "Galaxy Pad".

## What is in this repository

- `app/`, `test/`: contains some utility functions and unit tests
- `log/`: keeped empty as an output directory for local battles (see `run_local_battle.py`)
- `tools/`: contains AIs and the galaxy interpreter

In short, `tools/` contains almost all of our programs.

## Short comments for each component

### Galaxy Pad

- `tools/galaxy_lazy.py` is the interpreter of galaxy implemented in Python. The interpreter simply parses an input and evaluates it, and all the expression are lazily evaluated. The source file also contains several utility functions for conversion between a list in lambda calculus form and a cons list using Python tuples.
- `tools/client.py`, `tools/annotate_picture.py`, `tools/multiple_draw.py`: **TODO**
- `tools/api_server.py`: **TODO**
- `visualizer.html`: **TODO**

### Platform for developing AIs

- `tools/ai_interface.py`, `tools/common_interface.py`, `tools/conversion.py`: define data types and implement conversions between an encoded list used to HTTP Proxy and the corresponding decoded game state information provided to AI
- `tools/tournament_client.py`: send ship commands decided by AIs to alian server and pass its response to AIs
- `tools/multiship.py`, `tools/ai_selector.py`: utility wrapper classes for AIs.

### AIs

There are three types of AIs we will use in the final game.

- `tools/missile_man.py`: used when our team is attacker and the opponent seems to have multiple engines. **TODO**
- `tools/sniper.py`: used when our team is attacker and the opponent has a single engine. The "sniper" first goes into an orbit and then fires a high power laser if the relative position to the opponent's ship is good that we can do high damage. It also predicts an opponent's next move to decide where to shoot.
- `tools/split_escaper.py`: used when our team is defender. The "split escaper" has many engines and produces as many ships as it can.

### Game visualizer

- `game_state_player.html`: **TODO**

### Misc.

- `tools/cons_list.py`, `tools/deep_tuple.py`, `tools/mod_dem.py`: utilities
- **TODO: others?**
