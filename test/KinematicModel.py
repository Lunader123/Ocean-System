import numpy as np
import matplotlib.pyplot as plt
import copy
from celluloid import Camera  # 保存动图时用，pip install celluloid
import math
def KinematicModel(state,control,dt):
    """机器人运动学模型
        Args:
        state (_type_): 状态量---x,y,yaw,v,w
        control (_type_): 控制量---v,w,线速度和角速度
        dt (_type_): 离散时间

    Returns:
        _type_: 下一步的状态
    """
    state[0] += control[0] * math.cos(state[2]) * dt
    state[1] += control[0] * math.sin(state[2]) * dt
    state[2] += control[1] * dt
    state[3] = control[0]
    state[4] = control[1]

    return state