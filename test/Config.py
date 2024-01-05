import numpy as np
import matplotlib.pyplot as plt
import copy
from celluloid import Camera  # 保存动图时用，pip install celluloid
import math
class Config:
    """
    simulation parameter class
    """

    def __init__(self):
        # robot parameter
        # 线速度边界
        self.v_max = 1.0  # [m/s]
        self.v_min = -0.5  # [m/s]
        # 角速度边界
        self.w_max = 40.0 * math.pi / 180.0  # [rad/s]
        self.w_min = -40.0 * math.pi / 180.0  # [rad/s]
        # 线加速度和角加速度最大值
        self.a_vmax = 0.2  # [m/ss]
        self.a_wmax = 40.0 * math.pi / 180.0  # [rad/ss]
        # 采样分辨率 
        self.v_sample = 0.01  # [m/s]
        self.w_sample = 0.1 * math.pi / 180.0  # [rad/s]
        # 离散时间间隔
        self.dt = 0.1  # [s] Time tick for motion prediction
        # 轨迹推算时间长度
        self.predict_time = 3.0  # [s]
        # 轨迹评价函数系数
        self.alpha = 0.15
        self.beta = 1.0
        self.gamma = 1.0

        # Also used to check if goal is reached in both types
        self.robot_radius = 0.4  # [m] for collision check
        
        self.judge_distance = 10 # 若与障碍物的最小距离大于阈值（例如这里设置的阈值为robot_radius+0.2）,则设为一个较大的常值

        # 障碍物位置 [x(m) y(m), ....]
        self.ob = np.array([[-1, -1],
                    [0, 2],
                    [6.0,8.0],
                    [3.0,6.0],
                    [4.0, 2.0],
                    [5.0, 4.0],
                    [5.0, 6.0],
                    [5.0, 9.0],
                    [8.0, 9.0],
                    [7.0, 9.0],
                    [8.0, 10.0],
                    [9.0, 11.0],
                    [12.0, 13.0],
                    [12.0, 12.0],
                    [15.0, 15.0],
                    [13.0, 13.0]
                    ])
        # 目标点位置
        self.target = np.array([10,10])
