import pandas as pd
import csv
import re
import os.path
import pandas as pd
import re


# 把標記完情緒的檔案匯入並刪除情緒為中性的資料
def read_data():
    path = r'C:/ckip-learning/mobile01_emo/'
    files = os.listdir(path)
    total = []
    for file in files:
        data = pd.read_excel(path + file)
        for i in range(len(data)):
            id = data.loc[i, 'id']
            content = str(data.loc[i, 'seg_result'])
            try:
                score = int(data.loc[i, 'score'])
            except ValueError as e:
                pass

            post_time = data.loc[i, 'post_time']
            js = {
                'id': id,
                'post_time': post_time,
                'content': content,
                'score': score
            }

            if len(content) < 1:
                pass
            elif score == 2:
                pass
            elif score == 0:
                pass

            else:
                total.append(js)
    return total
    # 找出tag 並與情緒相乘
def tag_with_emo(total):
    re_n1 = re.compile("小孩|小朋友|小天使|小寶寶|孩子|懷孕|生產|同住|兒子|女兒|弟弟|妹妹|兒童|父母|公婆")
    re_pa = re.compile("開車|交通|通勤|停車|車位|機車|汽車|高速公路|機械式|平面坡道|露天|車")
    re_ele = re.compile("老人|父|母|長輩|樓梯|電梯|爸|媽|公公|婆婆|公婆|梯|懷孕")
    re_mrt = re.compile("捷運|交通|通勤|沿線|車站")
    re_bus = re.compile("公車|交通|通勤|老人|父|母|長輩|爸|媽|公公|婆婆|公婆|站牌")
    re_park = re.compile("公園|綠地|休憩|兒童|綠化|學區|寵物|狗|毛小孩|毛孩")
    re_conv_st = re.compile("機能|生活|便利|吃|外食|商店|店面|超商|全家|萊爾富|小七|7-11|seven|購物|全聯|愛買|頂好|家樂福|大潤發")
    re_annoy = re.compile("寺廟|吵|鬧|噪音|異味|煙|廟|鞭炮|金紙|燒香|消防隊")
    re_police_st = re.compile("派出所|治安|警察|亂|分隊|分局|混混|大隊")
    re_manage = re.compile("管委會|垃圾|管理|維護|維修|警衛|保全|乾淨|清潔|整齊|保潔|雜物|社區|公設比高")
    data_f = []
    for item in total:
        sc = int(item['score'])
        # print(sc)
        if re.search(re_n1, item['content']):
            item['Non_1'] = 1*sc
        else:
            item['Non_1'] = 0
        if re.search(re_pa, item['content']):
            item['Parking'] = 1*sc
        else:
            item['Parking'] = 0
        if re.search(re_ele, item['content']):
            item['Elevator'] = 1*sc
        else:
            item['Elevator'] = 0
        if re.search(re_mrt, item['content']):
            item['MRT'] = 1*sc
        else:
            item['MRT'] = 0
        if re.search(re_bus, item['content']):
            item['Bus'] = 1*sc
        else:
            item['Bus'] = 0
        if re.search(re_park, item['content']):
            item['Park'] = 1*sc
        else:
            item['Park'] = 0
        if re.search(re_conv_st, item['content']):
            item['Convenience'] = 1*sc
        else:
            item['Convenience'] = 0
        if re.search(re_annoy, item['content']):
            item['Noise'] = 1*sc
        else:
            item['Noise'] = 0
        if re.search(re_police_st, item['content']):
            item['Police_station'] = 1*sc
        else:
            item['Police_station'] =0
        if re.search(re_manage, item['content']):
            item['Management'] = 1*sc
        else:
            item['Management'] = 0

        a = int(item['Non_1']) + int(item['Parking']) + int(item['Elevator'])+ int(item['MRT']) + int(item['Bus']) + int(item['Park'])+int(item['Convenience']) + int(item['Noise'])+ int(item['Police_station'])+int(item['Management'])
        if a/int(sc) <2:
            pass
        else:

            data_f.append(item)
    return data_f


# 主程式
def main():
    total = read_data()
    data_f = tag_with_emo(total)
    df_f = pd.DataFrame(data_f)
    df_f.to_csv('C:/ckip-learning/project/dataframe_emo.csv',sep='|')
if __name__ == "__main__":
    main()
