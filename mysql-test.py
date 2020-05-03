import pymysql
import json

# with open('C:/ckip-learning/data_police_ntpe', 'r', encoding='utf-8') as f:
#     t = f.read().replace('},{', '}|{')
#     t1 = t.split('|')

db = pymysql.connect(host="localhost", user="root", password="tibame10", charset='utf8mb4')
cursor = db.cursor()
# sql = """create table lat_lng.latnlng(
# ID int NOT NULL ,
# Name varchar(50) NOT NULL,
# Latitude double NOT NULL,
# Longtitude double NOT NULL)
# """
# cursor.execute('''use lat_lng''')
# for i in range(len(t1)):
#     item = json.loads(t1[i])
#     id = int(i)
#     Name = item['name']
#     # Address = item['address']
#     Latitude = item['location']['lat']
#     Longtitude = item['location']['lng']
#     detail = """insert into `latnlng` (ID, Name,Latitude, Longtitude)
#      values ({},'{}',{},{})""".format(id, Name, Latitude, Longtitude)
#     cursor.execute(detail)
#     db.commit()
#選取警局的經緯度
police_location = """select name, latitude, longtitude from lat_lng.latnlng"""
cursor.execute(police_location)
data = cursor.fetchall()
print(data)
house_location = """select id, latitude, longitude from lat_lng.chungsin"""
cursor.execute(house_location)
house_data = cursor.fetchall()
print(house_data)
for i in house_data:
    for j in data:

# print(type(data))
# for i in data:
#     print(i)