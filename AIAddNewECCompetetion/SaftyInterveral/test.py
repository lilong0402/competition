import time

from fontTools.merge.util import current_time

import Tools as tl
# current_datatime = time.time()
# print(current_datatime)
# time.sleep(3)
# del current_datatime
# print(current_datatime)

# print("数据去重共耗时 : {} 秒".format(time.time() - current_datatime))


longitudes = [116.397128, 121.473701, 104.066801, 113.280637, 117.200983,117.200983]
latitudes = [39.916527, 31.230416, 30.653076, 23.125178, 31.86166,31.86166]
altitudes = [8000, 10000, 7500, 9200, 8800,8800]
# [a,b,c] = tl.coordinateTransformation(longitudes,latitudes,altitudes)
# print(a)

print(tl.trackPositionPointDeweighting(longitudes,latitudes,altitudes))

# current_time = time.time()
# sum=0
# for i in range(100000000):
#     pass
# print(time.time() - current_time)
# print(1<2)