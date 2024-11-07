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
from tensorflow.python.distribute.device_util import current


# 坐标转换 将经纬度转为三维笛卡尔坐标
# L:经度
# B:纬度
# H:高度
# @return 一个包含x,y,z的三维笛卡尔坐标的列表
def coordinateTransformation(L,B,H):
    a = 6378137
    b = 6356752
    ee = (a**2 - b**2 )/a**2 # 偏心率平方
    W =  math.sqrt(1 - ee * (math.sin(B) ** 2))
    N = a / W
    # 将角度从度转换为弧度
    L_rad = math.radians(L)
    B_rad = math.radians(B)
    [x,y,z] = [(N+H) * math.cos(B_rad) * math.cos(L_rad) ,(N+H) * math.cos(B_rad) * math.sin(L_rad) ,(N*(1-ee)+H) * math.sin(B_rad)]
    return [x,y,z]

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
# lx,ly,lz,sx,sy,sz 分别为有人机和无人机的长度、翼展以及高度
# se 为系统误差
# @return a,b,h 为构建椭球体的三个参数
def ellipsoidParameter(lx,ly,lz,sx,sy,sz,se):
    a = 2 * [max(lx,ly,lz) + max(sx,sy,sz)]+se
    b = 2 * [ly + min(sx,sy)] + se
    h = 2 * [min(sx,sy,sz) + min(lx,ly,lz)] + se
    return a,b,h

# 判断是否在纵向间隔层
# ux : 纵向方向相对速度
# uy : 侧向方向相对速度
# uz : 垂直方向相对速度
# location : 有人机的位置
# hp : 有人机实体
def lengthwaysSpacing(ux , uy , uz, location , hp ,):
    for i in location


# 航迹位置点去重
# 在处理飞行器的航迹数据时，移除在相同时间内重复的、相同位置的坐标点。些重复点可能是由于数据采集频率高、传感器误差或其他技术原因导致的
# longtitude,latitude,trackTime , 分别传入经度、维度、时间戳
# @return 去重后的新坐标
def trackPositionPointDeweighting(longtitude,latitude,trackTime):
    # 获取当前系统时间，便于统计耗时
    current_datatime = timetime.time()
    # 创建一个空列表用于存储去重后的数据
    unique_longitude = []
    unique_latitude = []
    unique_trackTime = []

    # 使用一个集合来记录已处理的 (经度, 纬度, 时间戳) 元组
    seen_points = set()
    # 时间复杂度on 空间复杂度 on
    for lon, lat, time in zip(longtitude, latitude, trackTime):
        point = (lon, lat, time)
        # 如果这个点未出现过，则添加到结果列表和已处理集合
        if point not in seen_points:
            unique_longitude.append(lon)
            unique_latitude.append(lat)
            unique_trackTime.append(time)
            seen_points.add(point)
    # 释放不必要的空间
    del seen_points
    print("数据去重共耗时 : {} 秒".format(timetime.time() - current_datatime) )
    return unique_longitude, unique_latitude, unique_trackTime


