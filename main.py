import argparse
import os
import json
import multiprocessing
from pomdp_runner import PomdpRunner
from util import RunnerParams
from environments.map import grid3
import numpy as np
from ipaddress import summarize_address_range
from tkinter import Grid
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation


grid_array = np.array(grid3)
# 获取行数和列数
rows, cols = grid_array.shape

def visualize_coverage(visited_nodes, ax):
    # 设置地图显示
    ax.imshow(grid3, cmap='jet')

    # 绘制覆盖路径
    for node in visited_nodes:
        x, y = node
        ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='white', alpha=0.6))

def update(frame):
    ax.cla()
    ax.set_title(f"Frame {frame}")
    ax.set_xticks([])
    ax.set_yticks([])
    # print(visited_nodes)
    # 显示覆盖路径的过程
    partial_coverage = coordinates[:frame + 1]
    visualize_coverage(partial_coverage, ax)

if __name__ == '__main__':
    """
    Parse generic params for the POMDP runner, and configurations for the chosen algorithm.
    Algorithm configurations the JSON files in ./configs

    Example usage:
        > python main.py pomcp --env Tiger-2D.POMDP
        > python main.py pbvi --env Tiger-2D.POMDP
    """
    parser = argparse.ArgumentParser(description='Solve pomdp')
    parser.add_argument('config', type=str, help='The file name of algorithm configuration (without JSON extension)')
    parser.add_argument('--env', type=str, default='GridWorld.POMDP', help='The name of environment\'s config file')
    parser.add_argument('--budget', type=float, default=float('inf'), help='The total action budget (defeault to inf)')
    parser.add_argument('--max_play', type=int, default=5, help='Maximum number of play steps')
    parser.add_argument('--snapshot', type=bool, default=False, help='Whether to snapshot the belief tree after each episode')
    parser.add_argument('--logfile', type=str, default=None, help='Logfile path')
    parser.add_argument('--random_prior', type=bool, default=False,
                        help='Whether or not to use a randomly generated distribution as prior belief, default to False')
    args = vars(parser.parse_args())
    params = RunnerParams(**args)
    with open(params.algo_config) as algo_config:
        algo_params = json.load(algo_config)
        runner = PomdpRunner(params)
        runner.run(**algo_params)
    visited_nodes = list(map(int,runner.trajectory))
    coordinates = [(index // cols, index % cols) for index in visited_nodes]
    print(coordinates)
    fig, ax = plt.subplots()
    animation = FuncAnimation(fig, update, frames=len(list(coordinates)), repeat=False)
    # 显示动画
    plt.show()
