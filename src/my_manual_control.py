from minigrid.manual_control import ManualControl
from my_actions import MyActions


class MyManualControl(ManualControl):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.key_to_action = {
            "down": MyActions.backward
        }

    def key_handler(self, event):
        key: str = event.key
        action: MyActions = self.key_to_action.get(key)
        if action is None:
            super().key_handler(event)
        else:
            self.step(action)
