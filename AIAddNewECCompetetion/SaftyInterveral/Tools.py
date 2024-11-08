#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：experiment
@File    ：Tools.py
@IDE     ：PyCharm
@Author  ：李龙
@Date    ：2024/11/5 22:43
'''
# 此模块用于提供计算无人机安全间隔的方法
import  math
import numpy as np
import time as timetime
import sys


# 一个用于统计耗时的装饰器
def decorator(func):
    def wrapper(*args, **kwargs):
        current_time = timetime.time()
        rec = func(*args, **kwargs)
        # sleep(2)
        end_time = timetime.time()
        print("{}  耗时： {} 秒".format(sys._getframe().f_back.f_code.co_name,end_time-current_time))
        return rec
    return wrapper

# 坐标转换 将经纬度转为三维笛卡尔坐标
# L:经度
# B:纬度
# H:高度
# @return 一个包含x,y,z的三维笛卡尔坐标的列表
@decorator
def coordinateTransformation(L,B,H):
    a = 6378137 # 赤道半径
    b = 6356752
    ee = (a**2 - b**2 )/a**2 # 偏心率平方

    L_new = np.array(L)
    B_new = np.array(B)
    H_new = np.array(H)

    W =  np.sqrt(1 - ee * (np.sin(B_new)  ** 2))
    N = a / W # 计算曲率半径
    # 将角度从度转换为弧度
    L_rad = np.radians(L_new)
    B_rad = np.radians(B_new)
    [x,y,z] = [(N+H_new) * np.cos(B_rad) * np.cos(L_rad) ,(N+H_new) * np.cos(B_rad) * np.sin(L_rad) ,(N*(1-ee)+H_new) * np.sin(B_rad)]
    return [x,y,z]

# 航迹位置点去重
# 在处理飞行器的航迹数据时，移除在相同时间内重复的、相同位置的坐标点。些重复点可能是由于数据采集频率高、传感器误差或其他技术原因导致的
# longtitude,latitude,trackTime , 分别传入经度、维度、时间戳
# @return 去重后的新坐标
@decorator
def trackPositionPointDeweighting(longtitude,latitude,height,trackTime):
    # 创建一个空列表用于存储去重后的数据
    unique_longitude = []
    unique_latitude = []
    unique_height = []
    unique_trackTime = []

    # 使用一个集合来记录已处理的 (经度, 纬度 , 高度 , 时间戳) 元组
    seen_points = set()
    # 时间复杂度on 空间复杂度 on
    for lon, lat, het, time in zip(longtitude, latitude,height, trackTime):
        point = ( lon , lat , het , time )
        # 如果这个点未出现过，则添加到结果列表和已处理集合
        if point not in seen_points:
            unique_longitude.append(lon)
            unique_latitude.append(lat)
            unique_height.append(het)
            unique_trackTime.append(time)
            seen_points.add(point)
    # 释放不必要的空间
    del seen_points
    return unique_longitude, unique_latitude, unique_trackTime

#print(coordinateTransformation(151.2093,-33.86882,4500))4
# 计算系统误差
# NSE ： 导航误差
# FTE ： 飞行技术误差
# @return 系统误差
def sysError(NSE , FTE):
    TSE =  math.sqrt(NSE ^ 2 + FTE ^ 2)
    return TSE

# 计算重叠概率
def overlappingProbability():
    pass

#print(sysError(2,2))
# 构建椭球碰撞盒
# UAV HP 为无人机与有人机
# se 为系统误差
# @return a,b,h 为构建椭球体的三个参数
def ellipsoidParameter(UAV,HP,se):
    a = 2 * [max(HP.hLong,HP.hWidth,HP.hHeight) + max(UAV.uLong,UAV.uWidth,UAV.uHeight)]+se
    b = 2 * [HP.hWidth + min(UAV.uLong,UAV.uWidth)] + se
    h = 2 * [min(UAV.uLong,UAV.uWidth,UAV.uHeight) + min(HP.hLong,HP.hWidth,HP.hHeight)] + se
    return a,b,h
# 判断是否在椭球体碰撞模型内
# a,b,h 为椭球体的三个参数
# r 球体半径
# location[x,y,z] 坐标
def ifInEllipsoid(a,b,c,location):
    return (location[0] ** 2) / (a ** 2) + (location[1] ** 2) / (b ** 2) + (location[2] ** 2) / (c ** 2) <= 1

# 判断是否在球体内
# cent 圆心坐标
# r 球体半径
# location[x,y,z] 坐标
def ifInSphere(cent , r , location):
    return (location[0] - cent[0]) ** 2 + (location[1] - cent[1]) ** 2 +(location[2] - cent[2]) ** 2 < r

# 判断是否在纵向间隔层
# ux : 纵向方向相对速度
# uy : 侧向方向相对速度
# uz : 垂直方向相对速度
# location : 有人机的位置
# hp : 有人机实体
def lengthwaysSpacing(ux , uy , uz, location , hp ,):
    pass






