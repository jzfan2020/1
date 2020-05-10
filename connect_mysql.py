import pymysql
import json
from math import radians, cos, sin, asin, sqrt
import mercantile

db = pymysql.connect(host='35.189.186.41', user='root', password='1234', charset='utf8mb4')

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
    cursor.execute('''select name, longtitude, latitude from distance_tag.{}'''.format(table_name))
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
#讀取重度土壤液化檔案
def soil_hi():
    with open('E:/project_use/geodata/soil_liq_hi.txt', 'r',encoding='utf-8') as f:
        t = json.load(f)
    '''把所有的物件只挑要的撈出來，另存成item'''
    item1 = []
    for iii, it in enumerate(t['features']):
        area = it['properties']['area']
        grade = it['properties']['分級']
        codi = []
        for jjj, it1 in enumerate(it['geometry']['coordinates']):
            for kkk, it2 in enumerate(it1):
                long = it2[0]
                lat = it2[1]
                codi.append((long,lat))
        js = {'area': area,'grade': grade, 'coodinates': codi}
        item1.append(js)
    # print(item)
    '''將經緯度轉換成quadkey值並存進原本的dict'''
    for mmm, each in enumerate(item1):
        each_tiles = []
        for nnn, each_pt in enumerate(each['coodinates']):
            zoom_num = 16
            aaa = mercantile.tile(each_pt[0], each_pt[1], zoom_num)
            each_tiles.append(aaa)
    #     print(list(set(each_tiles)))
        each_tile = list(set(each_tiles))
        each_quad = []
        for o in range(len(each_tile)):
            b = mercantile.quadkey(each_tile[o])
            each_quad.append(b)
        each['quad']=each_quad
    '''把最終高潛勢的quadkey值append成一個list'''
    level_hi_quad = []
    for ppp in range(len(item1)):
        each_quads = item1[ppp]['quad']
        for rrr in range(len(each_quads)):
            ccc = each_quads[rrr]
            level_hi_quad.append(ccc)
    set(level_hi_quad)
    return list(set(level_hi_quad))

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

    cursor = db.cursor()
    data_complete = check_completed('distance_tag.dis_tag_obj')
    data_o1 = get_total('realestate')
    data_o = []
    for each in data_o1:
        if each[0] in data_complete:
            pass
        else:
            data_o.append(each)
    # print(len(data_o))

    # print(data_o)
    soil_hi_level = soil_hi()
    tag_soil = []
    for aa, latlng in enumerate(data_o):
        # print(latlng)
        quad_o = mercantile.quadkey(mercantile.tile(latlng[3], latlng[4], 16))
        js_o = {'id': latlng[0], 'quad_o':quad_o}
        tag_soil.append(js_o)
    # print(len(tag_soil))
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
        # tag_p = ''
        # tag_m = ''
        # tag_m1 = ''
        # tag_b = ''
        # tag_p1 = ''
        # tag_t = ''
        # tag_s = ''
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
        if id_p == tag_soil[z]['id'] and tag_soil[z]['quad_o'] in soil_hi_level:
            tag_s = 1
        else:
            tag_s =0

        js_p = {'id': id_p,
                'tags' : [{'Police' : tag_p, 'Market': tag_m,'MRT': tag_m1,"Bus": tag_b,'Park' : tag_p1, 'Temple': tag_t, 'Soil_liq':tag_s}]}

        result_p.append(js_p)
    for item in result_p:
        # print(item)
        print('{} start'.format(item))
        sql = """insert into distance_tag.dis_tag_obj (ID_obj, Police, Market, MRT, Bus, Park, Temple, Soil_liq) values ('{}',{},{},{},{},{},{}, {})""".format(item['id'], item['tags'][0]['Police'],item['tags'][0]['Market'],item['tags'][0]['MRT'],item['tags'][0]['Bus'],item['tags'][0]['Park'],item['tags'][0]['Temple'], item['tags'][0]['Soil_liq'])
        # print(sql)
        cursor.execute(sql)
        db.commit()
    db.close()

if __name__ == '__main__':
    main()
