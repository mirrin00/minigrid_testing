# Testing Minigrid solution

## Dependcies

* [MiniGrid](https://github.com/Farama-Foundation/MiniGrid)

You can install the dependencies using the `pip3 install -r requirements.txt` command

## Run solutions

To run the solution with **manual control**, use the `python3 main.py manual` command

To run the solution in automatic mode with the process shown, use the `python3 main.py auto human` commnad

To run the solution in automatic mode without graphics, use the `python3 main.py auto` commnad

## File assignment

### `main.py`

Entry point of programm

### `base_solution.py`

The base class for solution which has:
* dummy method to create the solution
* wrapper methods to add actions
* methods to get information about an object or cell

### `solution.py`

Solution implementation. The class should be created by the user

### `update_minigrid.py`

Updates constants in the MiniGrid library for new objects. Must be the first import

### `my_actions.py`

Contains new actions for agent

### `my_objects.py`

Contains new objects for the environment

### `my_manual_control.py`

Class based on `ManualControl` for manual agent control with support for new actions

### `simple_env.py`

Example of class for creating new environment with random generation, support
for new actions and result statistics

### `assets/dt_logo.jpeg`

Image for the new object `DtLogo`

## What is next?

* Use of [wrappers](https://minigrid.farama.org/api/wrappers/)
* [Example of dynamic obstacles](https://github.com/Farama-Foundation/Minigrid/blob/master/minigrid/envs/dynamicobstacles.py)
* A base class solution for each step, not a global solution