import pymysql
import json
from math import radians, cos, sin, asin, sqrt

db = pymysql.connect(host='localhost', user='root', password='1202tibame', charset='utf8mb4')
with open('E:/project_use/lat_lng/data_market_ntpe.txt', 'r', encoding='utf-8') as f:
    t = f.read().replace('},{', '}|{')
    t1 = t.split('|')
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 #經度距離
    dlat = lat2 - lat1 #緯度距離
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半徑，單位為公里
    return c * r

# #計算距離:
def distance_cal(data1,data2, distance_required):
    dis_list = []
    for i in range(len(data1)):
        for j in range(len(data2)):
            dis = haversine(data1[i][3],data1[i][4], data2[j][1],data2[j][2])
            if dis <= distance_required:
               dis_list.append(data1[i][0])
            else:
                pass
    dis_set = set(dis_list)
    return dis_set
cursor = db.cursor()
cursor.execute('''select id, url,address, longitude, latitude from realestate.chungsin''')
data_o = cursor.fetchall()
cursor.execute('''select name, longtitude, latitude from project_lat_lng.latnlng_police''')
data_m = cursor.fetchall()

for i in range(len(data_o)):
    li = []
    for j in range(len(data_m)):
        dis = haversine(data_o[i][3], data_o[i][4], data_m[j][1], data_m[j][2])
        # a = data_o[i][0] + data_m[j][0] + str(dis)
        li.append(dis)
    print(data_o[i][0], min(li))
    print('\n')
        # print(data_o[i][0], data_m[j][0], dis)