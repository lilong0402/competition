import time

current_datatime = time.time()
print(current_datatime)
time.sleep(3)
del current_datatime
print(current_datatime)

print("数据去重共耗时 : {} 秒".format(time.time() - current_datatime))


