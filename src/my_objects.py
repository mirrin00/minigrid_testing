from email.mime import image
from minigrid.core.world_object import WorldObj
import update_minigrid
from minigrid.core.world_object import WorldObj
from minigrid.core.constants import IDX_TO_COLOR, COLOR_NAMES
import numpy as np
import pygame


def new_decode(type_idx: int, color_idx: int, state: int) -> WorldObj or None:
    name: str = update_minigrid.NEW_IDX_TO_OBJECT[type_idx]
    color: str = IDX_TO_COLOR[color_idx]
    if name == "dt_logo":
        return DtLogo()
    else:
        return None

update_minigrid.new_decode = new_decode


images = {
    "dt_logo": pygame.image.load("assets/dt_logo.jpeg")
}

class DtLogo(WorldObj):

    def __init__(self):
        super().__init__("dt_logo", COLOR_NAMES[0])

    def can_overlap(self) -> bool:
        return True

    def can_pickup(self) -> bool:
        return True

    def render(self, r: np.ndarray) -> np.ndarray:
        h, w = r.shape[:2]
        new_image = pygame.transform.scale(images["dt_logo"], (w, h))
        result_array = pygame.surfarray.array3d(new_image)
        result_array = result_array.swapaxes(0, 1)
        r[:] = result_array[:]
        return result_array
