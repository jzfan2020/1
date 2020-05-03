import pandas as pd
import os.path
import json
import requests as ss
from bs4 import  BeautifulSoup as bs
#先把要丟進去的地址撈出來
def market_data():
    path = r'C:/ckip-learning/geodata/mart/'
    files = os.listdir(path)
    mart_data = []
    for file in files:
        data = pd.read_excel(path +'/' +file)
        for i in range(len(data)):
            name = data.loc[i,"門市"]
            add = data.loc[i, "地址"]
            obj = {
                'name' : name,
                'address' : add
            }
            mart_data.append(obj)
    return mart_data
def police_data():
    data_p = pd.read_excel('C:/ckip-learning/geodata/police_station_ntpe.xlsx')
    police_data = []
    for j in range(len(data_p)):
        name = data_p.loc[j, '單位']
        add = data_p.loc[j, '地址']
        obj_p ={
            'name' : name,
            'address' : add
        }
        police_data.append(obj_p)
    return police_data
#讀取kw:
def kw():
    with open('C:/ckip-learning/jz.txt', 'r') as f:
        code = f.read()
    return code

def get_location(data):
    code = kw()
    final_result = []
    for k in range(len(data)):
        name = data[k]['name']
        add = data[k]['address']
        url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(add, code)
        res = ss.get(url=url)
        soup = bs(res.text, 'html.parser')
        for m in soup:
            got = json.loads(m)
            location = got['results'][0]['geometry']['location']
            obj = {
                'name' : name,
                'location' : [location]
            }
            final_result.append(obj)
    return final_result
#存檔
def save_to_txt(content_list, file_name):
    c = []
    for a in content_list:
        b = json.dumps(a, ensure_ascii=False)
        c.append(b)
    final = ','.join(c)

    with open('C:/ckip-learning/{}.txt'.format(file_name),'w', encoding='utf-8') as sv:
        sv.write(final)


if __name__ == "__main__":
    data_police = police_data()
    dp = get_location(data_police)
    save_to_txt(dp, 'data_police_ntpe')
    data_market = market_data()
    dm= get_location(data_market)
    save_to_txt(dm, 'data_market_ntpe')


