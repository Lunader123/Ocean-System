class UnderwaterMap:
    def __init__(self, width, height, depth_values=None):
        self.width = width
        self.height = height
        self.depth_values = depth_values or self.initialize_depth_values()

    def initialize_depth_values(self):
        # 默认情况下，将深度初始化为零
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def set_depth(self, x, y, depth):
        # 设置特定坐标的深度值
        if 0 <= x < self.width and 0 <= y < self.height:
            self.depth_values[y][x] = depth
        else:
            print("Invalid coordinates")

    def get_depth(self, x, y):
        # 获取特定坐标的深度值
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.depth_values[y][x]
        else:
            print("Invalid coordinates")

    def display_map(self):
        # 显示海底地图
        for row in self.depth_values:
            print(row)

# 创建一个 3x3 的海底地图
underwater_map = UnderwaterMap(3, 3)

# 设置一些深度值
underwater_map.set_depth(0, 0, 10)
underwater_map.set_depth(1, 1, 5)
underwater_map.set_depth(2, 2, 8)

# 显示海底地图
underwater_map.display_map()
