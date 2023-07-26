from enum import IntEnum
from minigrid.core.actions import Actions


class MyActions(IntEnum):
    # Actions from minigrid
    # Turn left, turn right, move forward
    left = Actions.left
    right = Actions.right
    forward = Actions.forward
    # Pick up an object
    pickup = Actions.pickup
    # Drop an object
    drop = Actions.drop
    # Toggle/activate an object
    toggle = Actions.toggle

    # Done completing task
    done = Actions.done

    # New actions
    # Move backward
    backward = 10
