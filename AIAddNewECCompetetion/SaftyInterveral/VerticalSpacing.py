'''
@Project ：experiment
@File    ：VerticalSpacing.py
@IDE     ：PyCharm
@Author  ：李龙
@Date    ：2024/11/6 10:38
'''

import Tools as tl
import math
import  numpy as np
# from scipy import integrate
# 无人机
# 'uLong','uWidth','uHeight' ： 为无人机的尺寸
class UAV:
    __slots__ = ('uLong','uWidth','uHeight')

# 有人机
# 'hLong','hWidth','hHeight' ： 有人机尺寸
class HP:
    __slots__ = ('hLong','hWidth','hHeight')


# ux、uy、uz 飞行器在三个方向上的相对速度
# longitude  latitude Height 经纬度 + 高度
# uav_Class hp_class 代表无人机与有人机实体
def verticalRisk(ux,uy,uz,uLongitude,uLatitude,uHeight,hLongtitude,hLatitude,hHeight,uav_Class,hp_Class):
    # 数据预处理
        #去重

    # 转为三维笛卡尔坐标
    [uavx_o,uavy_o,uavz_o] = tl.coordinateTransformation(uLongitude,uLatitude,uHeight)
    [hpx_o,hpy_o,hpz_o] = tl.coordinateTransformation(hLongtitude,hLatitude,hHeight)


    # 将无人机视为质点，以无人机为中心建立坐标系
    [hpx_n,hpy_n,hpz_n] = [hpx_o,hpy_o,hpz_o] - [uavx_o,uavy_o,uavz_o]
    # 筛选出可能发生碰撞的点
    [hpx, hpy, hpz] = tl.lengthwaysSpacing(ux,uy,uz,[hpx_n,hpy_n,hpz_n],hp_Class)
    # 取 py0 为 0.9739
    # 取 pz0 为 0.4881
    # 取 ES  为 0.2
    Pcl0 = 0.9739 * 0.4881 * (1+(uz/ux) * (hp_Class.hLong/hp_Class.hHeight)) * (1+(uy/ux)*(hp_Class.hLong/hp_Class.hWidth))
    ## 缺少传参以及实现
    P0 = 0.2 * tl.overlappingProbability()

    return 2 * Pcl0 * P0 , hpx




