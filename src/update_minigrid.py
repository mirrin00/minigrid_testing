from minigrid.core import constants
from minigrid.core import world_object


NEW_OBJECT_TO_IDX = {
    "dt_logo": 11
}

NEW_IDX_TO_OBJECT = {v: k for k, v in NEW_OBJECT_TO_IDX.items()}

# It is only needed to update the `OBJECT_TO_IDX` constant. The `WorldObj.decode`
# method is only called in `MiniGridEnv.agent_sees` which is not used in the
# library itself. Without updating `decode` method, other methods/functions will work

constants.OBJECT_TO_IDX.update(NEW_OBJECT_TO_IDX)
constants.IDX_TO_OBJECT.update(NEW_IDX_TO_OBJECT)

origin_decode = world_object.WorldObj.decode
new_decode = lambda x: None  # Should be overrided

def decode(type_idx: int, color_idx: int, state: int) -> world_object.WorldObj or None:
    if type_idx in NEW_IDX_TO_OBJECT:
        return new_decode(type_idx, color_idx, state)
    else:
        return origin_decode(type_idx, color_idx, state)

world_object.WorldObj.decode = decode
