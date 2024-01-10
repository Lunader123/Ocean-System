from ipaddress import summarize_address_range
from tkinter import Grid
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation

# 二维地图大小
rows = 10
cols = 10
sum_time = 0
sum_consumption = 0

# 地图表示，0表示可通行，1表示障碍物
grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
# grid = [
#     [0,0,0],
#     [0,0,0],
#     [0,0,0]
# ]
# grid = [
#     [0,0],
#     [0,0]
# ]
# 将二维网格转换为Graph对象
G = nx.Graph()
for i in range(rows):
    for j in range(cols):
        G.add_node((i,j))
        if i > 0 :
            G.add_edge((i, j), (i - 1, j))
        if j > 0:
            G.add_edge((i, j), (i, j - 1))
def planning(graph, start):
    stack = [start]
    visited = set()
    while stack:
        current = stack.pop()
        cx, cy = current
        if current not in visited:
            yield current
            visited.add(current)
            # Your logic for processing the current node goes here
            # For example, add neighbors in a "bowtie" pattern
            neighbors = get_bowtie_neighbors(graph, cx, cy)
            # print(len(neighbors))
            stack.extend(neighbors)
def get_bowtie_neighbors(graph, x, y):
    neighbors = []

    # Right movement
    if x + 1 < cols :
        neighbors.append((x + 1, y))
    # Up movement
    if y - 1 >= 0 :
        neighbors.append((x, y - 1))

    # Left movement
    if x - 1 >= 0 :
        neighbors.append((x - 1, y))

    # Down movement
    if y + 1 < rows :
        neighbors.append((x, y + 1))

    return neighbors


# Assuming the rest of your code remains the same, you can now call the `planning` function
# start_node = (0, 0)
# planning(G, start_node,sum_time=0,sum_consumption=0)
def visualize_coverage(visited_nodes, ax):
    # 设置地图显示
    ax.imshow(grid, cmap='jet')

    # 绘制覆盖路径
    for node in visited_nodes:
        x, y = node
        ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='blue'))
def update(frame):
    ax.cla()
    ax.set_title(f"Frame {frame}")
    ax.set_xticks([])
    ax.set_yticks([])
    # print(visited_nodes)
    # 显示覆盖路径的过程
    partial_coverage = visited_nodes[:frame + 1]
    visualize_coverage(partial_coverage, ax)
start = (0, 0)
visited_nodes = list(planning(graph=G, start=(0, 0)))
for i in range(1,len(visited_nodes)):
    cx, cy = visited_nodes[i]
    cx1, cy1 = visited_nodes[i-1]
    if cx1 == cx:
        sum_consumption += 1
        sum_time += 1
    else:
        sum_consumption += 2
        sum_time += 2
    print("Total Consumption:", sum_consumption)
    print("Total Time:", sum_time)
fig, ax = plt.subplots()
animation = FuncAnimation(fig, update, frames=len(list(planning(G, (0, 0)))), repeat=False)
# 显示动画
plt.show()
