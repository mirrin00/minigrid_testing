from base_solution import BaseSolution

class Solution(BaseSolution):

    def generate_actions(self, observation):
        try:
            key_pos = self.find_object(observation, "key")
            door_pos = self.find_object(observation, "door")
            goal_pos = self.find_object(observation, "goal")
            if key_pos[0] is None:
                key_pos = (0, 0)
            if door_pos[0] is None:
                door_pos = (1, 1)
            if goal_pos[0] is None:
                goal_pos = (2, 2)
            direction = "right"
            agent_coords = [1, 1]
            if key_pos[1] == 1:
                # Agent on row with key, no rotate is need
                self.add_action_forward(key_pos[0] - agent_coords[0] - 1)
                agent_coords[0] += key_pos[0] - agent_coords[0] - 1
                self.add_action_pickup()
            else:
                self.add_action_forward(key_pos[0] - agent_coords[0])
                agent_coords[0] += key_pos[0] - agent_coords[0]
                self.add_action_right()
                direction = "down"
                self.add_action_forward(key_pos[1] - agent_coords[1] - 1)
                agent_coords[1] += key_pos[1] - agent_coords[1] - 1
                self.add_action_pickup()
            if self.get_object_name(observation, door_pos[0] - 1, door_pos[1]) == "wall":
                # vertical door
                if direction == "down":
                    self.add_action_left()
                    direction = "right"
                if door_pos[0] < agent_coords[0]:
                    self.add_action_backward(agent_coords[0] - door_pos[0])
                else:
                    self.add_action_forward(door_pos[0] - agent_coords[0])
                self.add_action_right()
                direction = "down"
                self.add_action_forward(door_pos[1] - agent_coords[1])
                self.add_action_toogle()
                self.add_action_forward(2)
                agent_coords = [door_pos[0], door_pos[1] + 1]
            else:
                # horizontal door
                if direction == "right":
                    self.add_action_right()
                    direction = "down"
                if door_pos[1] < agent_coords[1]:
                    self.add_action_backward(agent_coords[1] - door_pos[1])
                else:
                    self.add_action_forward(door_pos[1] - agent_coords[1])
                self.add_action_left()
                direction = "right"
                self.add_action_forward(door_pos[0] - agent_coords[0])
                self.add_action_toogle()
                self.add_action_forward(2)
                agent_coords = [door_pos[0] + 1, door_pos[1]]
            if direction == "down":
                self.add_action_left()
                direction = "right"
            if goal_pos[0] < agent_coords[0]:
                self.add_action_backward(agent_coords[0] - goal_pos[0])
                agent_coords[0] -= agent_coords[0] - goal_pos[0]
            else:
                self.add_action_forward(goal_pos[0] - agent_coords[0] + 1)
                agent_coords[0] += goal_pos[0] - agent_coords[0] + 1
            self.add_action_right()
            if goal_pos[1] < agent_coords[1]:
                self.add_action_backward(agent_coords[1] - goal_pos[1])
            else:
                self.add_action_forward(goal_pos[1] - agent_coords[1] + 1)
        except Exception as e:
            print("Error:", e)
            raise e
