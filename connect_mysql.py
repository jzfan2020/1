import pymysql
import json
from math import radians, cos, sin, asin, sqrt

db = pymysql.connect(host='localhost', user='root', password='1202tibame', charset='utf8mb4')

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
#把所有物件不分表格取出:
def get_total(db_name):
    cursor = db.cursor()
    cursor.execute('''use {}'''.format(db_name))
    sql = '''show tables'''
    cursor.execute(sql)
    a = cursor.fetchall()
    table_list = []
    for k in a:
        table_list.append(k[0])
    data = []
    for table in table_list:
        cursor.execute('''select id, url,address, longitude, latitude from {}'''.format(table))
        data_each = cursor.fetchall()
        for each in data_each:
            data.append(each)
    return data

#對照資料集
def data_set_collection(table_name):
    cursor = db.cursor()
    cursor.execute('''select name, longtitude, latitude from project_lat_lng.{}'''.format(table_name))
    data = cursor.fetchall()
    return data
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
#新增表格
def new_table():
    cursor = db.cursor()
    addnew = """create table distance_tag.dis_tag_obj(ID char(20) NOT NULL, Police int NOT NULL, Market int NOT NULL, MRT int NOT NULL, Bus int NOT NULL, Park int NOT NULL, Temple int NOT NULL)"""
    cursor.execute(addnew)

#判斷物件是否已存在資料庫裡
def check_completed(target_name):
    cursor = db.cursor()
    sql = '''select id_obj from {}'''.format(target_name)
    cursor.execute(sql)
    cmps = cursor.fetchall()
    completed = []
    for cmp in cmps:
        completed.append(cmp[0])
    return  completed
def main():

    # new_table()
    cursor = db.cursor()
    data_complete = check_completed('distance_tag.dis_tag_obj')
    data_o1 = get_total('realestate')
    data_o = []
    for each in data_o1:
        if each[0] in data_complete:
            pass
        else:
            data_o.append(each)


    data_p = data_set_collection('latnlng_police')
    data_m = data_set_collection('latnlng_market')
    data_m1 = data_set_collection('latnlng_mrt')
    data_b = data_set_collection('latnlng_bus')
    data_p1 = data_set_collection('latnlng_park')
    data_t = data_set_collection('latnlng_temple')
    a = distance_cal(data_o,data_p, 3)
    b = distance_cal(data_o, data_m, 0.3)
    c = distance_cal(data_o, data_m1, 1)
    d = distance_cal(data_o, data_b, 0.3)
    e = distance_cal(data_o, data_p1, 0.5)
    l = distance_cal(data_o, data_t, 0.5)
    result_p =[]
    # result = []
    for z in range(len(data_o)):
        tag_p = ''
        tag_m = ''
        tag_m1 = ''
        tag_b = ''
        tag_p1 = ''
        tag_t = ''
        id_p = data_o[z][0]
        if id_p in a:
            tag_p = 1
        else:
            tag_p = 0
        if id_p in b:
            tag_m = 1
        else:
            tag_m = 0
        if id_p in c:
           tag_m1 = 1
        else:
            tag_m1 = 0
        if id_p in d:
            tag_b = 1
        else:
            tag_b = 0
        if id_p in e:
            tag_p1 = 1
        else:
            tag_p1 = 0
        if id_p in l:
            tag_t = 1
        else:
            tag_t = 0

        js_p = {'id': id_p,
                'tags' : [{'Police' : tag_p, 'Market': tag_m,'MRT': tag_m1,"Bus": tag_b,'Park' : tag_p1, 'Temple': tag_t}]}

        result_p.append(js_p)
    for item in result_p:
        # print(item)
        print('{} start'.format(item))
        sql = """insert into distance_tag.dis_tag_obj (ID_obj, Police, Market, MRT, Bus, Park, Temple) values ('{}',{},{},{},{},{},{})""".format(item['id'], item['tags'][0]['Police'],item['tags'][0]['Market'],item['tags'][0]['MRT'],item['tags'][0]['Bus'],item['tags'][0]['Park'],item['tags'][0]['Temple'])
        cursor.execute(sql)
        db.commit()
    # db.close()

if __name__ == '__main__':
    main()
