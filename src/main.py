from __future__ import annotations

import update_minigrid  # Required to update minigrid variables
from simple_env import SimpleEnv
from solution import Solution
from my_manual_control import MyManualControl
import sys


def main(render_mode=None):
    env = SimpleEnv(render_mode=render_mode)

    observation, info = env.reset()
    solution = Solution()
    solution.generate_actions(observation["image"])
    for _ in range(50):
        action = solution.get_action()
        observation, reward, terminated, truncated, info = env.step(action)

        if terminated:
            print("Win")
            break
        if truncated:
            print("Lose")
            break
    else:
        print("Lose")
    env.close()
    print(env.get_result())


def main_manual():
    env = SimpleEnv(render_mode="human")

    # enable manual control for testing
    manual_control = MyManualControl(env, seed=42)
    manual_control.start()

    
if __name__ == "__main__":
    print("Usage: main.py <control_mode> [<render_mode>]")
    if len(sys.argv) < 2:
        control_mode = "auto"
    else:
        control_mode = sys.argv[1]
    if len(sys.argv) < 3:
        render_mode = None
    else:
        render_mode = sys.argv[2]
    cmodes = ["auto", "manual"]
    if control_mode not in cmodes:
        print("Control mode must be one of", cmodes, ". Control mode is", control_mode)
        exit(1)
    rmodes = ["human", None]
    if render_mode not in rmodes:
        print("Render mode must be one of", rmodes, "where None is default value. Render mode is", render_mode)
        exit(1)
    if control_mode == "auto":
        main(render_mode=render_mode)
    else:
        main_manual()
