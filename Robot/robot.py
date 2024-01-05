class Robot:
    def __init__(self, underwater_map):
        self.underwater_map = underwater_map
        self.current_position = (0, 0)

    def move(self, action):
        # 根据动作更新机器人的位置
        x, y = self.current_position
        if action == "up" and y < self.underwater_map.height - 1:
            y += 1
        elif action == "down" and y > 0:
            y -= 1
        elif action == "right" and x < self.underwater_map.width - 1:
            x += 1
        elif action == "left" and x > 0:
            x -= 1
        self.current_position = (x, y)

    def sense(self):
        # 返回当前位置的深度值
        x, y = self.current_position
        return self.underwater_map.get_depth(x, y)

