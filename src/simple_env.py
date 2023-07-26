# Tutorial: https://minigrid.farama.org/content/create_env_tutorial/

from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Door, Goal, Key, Wall
from minigrid.minigrid_env import MiniGridEnv

from minigrid.core.actions import Actions
from gymnasium.core import ActType, ObsType
from typing import Any, SupportsFloat
from random import randint
from my_actions import MyActions
from my_objects import DtLogo


class SimpleEnv(MiniGridEnv):
    def __init__(
        self,
        size=10,
        agent_start_pos=(1, 1),
        agent_start_dir=0,
        max_steps: int or None = None,
        **kwargs,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 4 * size**2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            # Set this to True for maximum speed
            see_through_walls=True,
            max_steps=max_steps,
            # Set this to see all map
            agent_view_size=size if size % 2 == 1 else size + 1,
            **kwargs,
        )
        
        self.score = 0.0
        self.key_pickuped = False
        self.result_status = "time limit"

    @staticmethod
    def _gen_mission():
        return "grand mission"

    def reset(self, *args, **kwargs) -> tuple[ObsType, dict[str, Any]]:
        self.score = 0.0
        self.key_pickuped = False
        self.result_status = "time limit"
        return super().reset(*args, **kwargs)

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Generate separation wall
        if randint(0, 1) == 0:
            # Vertical line
            line_num = randint(2, width - 3)
            for i in range(0, height):
                self.grid.set(line_num, i, Wall())
            # Generate door position
            door_y = randint(1, height - 2)
            self.grid.set(line_num, door_y, Door(COLOR_NAMES[0], is_locked=True))
            # Generate key position
            key_x = randint(1, line_num - 1)
            key_y = randint(2, height - 2)
            self.grid.set(key_x, key_y, Key(COLOR_NAMES[0]))
            # Generate dt_logo position
            dt_logo_x = randint(1, line_num - 1)
            dt_logo_y = randint(2, height - 2)
            while dt_logo_x == key_x and dt_logo_y == key_y:
                dt_logo_x = randint(1, line_num - 1)
                dt_logo_y = randint(2, height - 2)
            self.grid.set(dt_logo_x, dt_logo_y, DtLogo())
        else:
            # Horizontal line
            line_num = randint(2, height - 3)
            for i in range(0, width):
                self.grid.set(i, line_num, Wall())
            door_x = randint(1, width - 2)
            self.grid.set(door_x, line_num, Door(COLOR_NAMES[0], is_locked=True))
            # Generate key position
            key_x = randint(2, width - 2)
            key_y = randint(1, line_num - 1)
            self.grid.set(key_x, key_y, Key(COLOR_NAMES[0]))
            # Generate dt_logo position
            dt_logo_x = randint(2, width - 2)
            dt_logo_y = randint(1, line_num - 1)
            while dt_logo_x == key_x and dt_logo_y == key_y:
                dt_logo_x = randint(1, line_num - 1)
                dt_logo_y = randint(2, height - 2)
            self.grid.set(dt_logo_x, dt_logo_y, DtLogo())

        # Generate verical separation wall
        # for i in range(0, height):
        #     self.grid.set(5, i, Wall())
        
        # Place the door and key
        # self.grid.set(5, 6, Door(COLOR_NAMES[0], is_locked=True))
        # self.grid.set(3, 6, Key(COLOR_NAMES[0]))

        # Place a goal square in the bottom-right corner
        self.put_obj(Goal(), width - 2, height - 2)

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = "grand mission"


    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        try:
            obs, reward, terminated, truncated, ddict = super().step(action)
        except ValueError:
            new_terminated = False
            new_reward = None
            if action == MyActions.backward:
                back_pos = self.agent_pos - self.dir_vec
                back_cell = self.grid.get(*back_pos)
                if back_cell is None or back_cell.can_overlap():
                    self.agent_pos = tuple(back_pos)
                if back_cell is not None and back_cell.type == "goal":
                    new_terminated = True
                    new_reward = self._reward()
                if back_cell is not None and back_cell.type == "lava":
                    new_terminated = True
                print("backward")
            else:
                raise ValueError("Unknown action")
            obs, reward, terminated, truncated, ddict = super().step(Actions.done)
            if new_reward is not None:
                reward = new_reward
            terminated = new_terminated
        if truncated:
            self.result_status = "time limit"
        elif terminated:
            term_cell = self.grid.get(*self.agent_pos)
            if term_cell is not None and term_cell.type == "goal":
                self.result_status = "passed"
                self.score += 100
            else:
                self.result_status = "failed"
        if not self.key_pickuped and self.carrying is not None and isinstance(self.carrying, Key):
            self.score += 50
            self.key_pickuped = True
        return obs, reward, terminated, truncated, ddict


    def get_view_exts(self, agent_view_size=None):
        return 0, 0, self.width + 1, self.height + 1

    def gen_obs_grid(self, agent_view_size=None):
        agent_dir = self.agent_dir
        self.agent_dir = -1
        ret = super().gen_obs_grid()
        self.agent_dir = agent_dir
        return ret

    def get_result(self) -> dict[str, Any]:
        return {
            "status": self.result_status,
            "steps": self.step_count,
            "score": self.score,
        }
