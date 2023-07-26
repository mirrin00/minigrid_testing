from minigrid.core.constants import IDX_TO_OBJECT
from my_actions import MyActions


class BaseSolution:

    def __init__(self) -> None:
        self.action_list = []

    def get_action(self):
        if len(self.action_list) == 0:
            return MyActions.done
        else:
            return self.action_list.pop(0)

    def find_object(self, observation, obj_name):
        for i, row in enumerate(observation):
            for j, col in enumerate(row):
                if IDX_TO_OBJECT[col[0]] == obj_name:
                    return i, j
        return None, None

    def get_object_name(self, observation, i, j):
        return IDX_TO_OBJECT.get(observation[i, j, 0], "empty")

    def __add_action(self, action, times=1):
        for _ in range(times):
            self.action_list.append(action)

    # If use setattr for this function, IDE cannot show tips for function names
    def add_action_forward(self, times=1):
        self.__add_action(MyActions.forward, times)

    def add_action_backward(self, times=1):
        self.__add_action(MyActions.backward, times)

    def add_action_left(self, times=1):
        self.__add_action(MyActions.left, times)

    def add_action_right(self, times=1):
        self.__add_action(MyActions.right, times)

    def add_action_done(self, times=1):
        self.__add_action(MyActions.done, times)

    def add_action_drop(self, times=1):
        self.__add_action(MyActions.drop, times)

    def add_action_toogle(self, times=1):
        self.__add_action(MyActions.toggle, times)

    def add_action_pickup(self, times=1):
        self.__add_action(MyActions.pickup, times)

    def generate_actions(self, observation):
        # May be refactor observation for more comfortable use
        pass  # There should be solution
