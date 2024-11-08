'''
@Project ：experiment
@File    ：VerticalSpacing.py
@IDE     ：PyCharm
@Author  ：李龙
@Date    ：2024/11/6 10:38
'''
from tensorflow.python.distribute.device_util import current

import Tools as tl
import math
import  numpy as np
# from scipy import integrate
# 无人机
# 'uLong','uWidth','uHeight' ： 为无人机的尺寸
# 'speed','course' 为无人机的航向和速度
class UAV:
    __slots__ = ('uLong','uWidth','uHeight','speed','course')

# 有人机
# 'hLong','hWidth','hHeight' ： 有人机尺寸
class HP:
    __slots__ = ('hLong','hWidth','hHeight','speed','course')


# ux、uy、uz 飞行器在三个方向上的相对速度
# longitude  latitude Height 经纬度 + 高度
# uav_Class hp_class 代表无人机与有人机实体
def verticalRisk(ux,uy,uz,uLongitude,uLatitude,uHeight,hLongtitude,hLatitude,hHeight,uav_Class,hp_Class):
    # 数据预处理
        #去重
    [uavx_longtitude,uavy_latitude,uavz_height] = tl.trackPositionPointDeweighting(uLongitude,uLatitude,uHeight)
    [hpx_longtitude,hpy_latitude,hpz_height] = tl.trackPositionPointDeweighting(hLongtitude,hLatitude,hHeight)
    # 转为三维笛卡尔坐标
    [uavx_o,uavy_o,uavz_o] = tl.coordinateTransformation(uavx_longtitude,uavy_latitude,uavz_height)
    [hpx_o,hpy_o,hpz_o] = tl.coordinateTransformation(hpx_longtitude,hpy_latitude,hpz_height)
    del [uavx_longtitude,uavy_latitude,uavz_height]
    del [hpx_longtitude,hpy_latitude,hpz_height]
    # 计算系统误差
    TSE = tl.sysError(0,0)
    # 建立椭球碰撞模型
    [a,b,h] = tl.ellipsoidParameter(uav_Class,hp_Class,TSE)
    # 建立球体的碰撞区
    # 以有人机为中心建立坐标系
    [uavx_n,uavy_n,uavz_n] =[uavx_o,uavy_o,uavz_o] - [hpx_o,hpy_o,hpz_o]

    # 筛选出可能发生碰撞的点
    [uavx, uavy, uavz] = tl.lengthwaysSpacing(ux,uy,uz,[uavx_n,uavy_n,uavz_n],hp_Class)
    # 取 py0 为 0.9739
    # 取 pz0 为 0.4881
    # 取 ES  为 0.2
    Pcl0 = 0.9739 * 0.4881 * (1+(uz/ux) * (hp_Class.hLong/hp_Class.hHeight)) * (1+(uy/ux)*(hp_Class.hLong/hp_Class.hWidth))
    ## 缺少传参以及实现
    P0 = 0.2 * tl.overlappingProbability()

    return 2 * Pcl0 * P0 , hpx




