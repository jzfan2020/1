import re
import json


def remove_punctuation(line, strip_all=True):
    if strip_all:
        rule = re.compile("[^a-zA-Z0-9\u4e00-\u9fa5]")
        line = rule.sub("|", line)
    else:

        line = re.sub("[\s+\.\!\/_,$%^*(+\"\']+", "|", line)
    return line

def main():
    text = input()
    txt = remove_punctuation(text).split('|')
    t1 = []
    t2 = []
    t3 = []
    t4 = []
    t5 = []
    t6 = []
    t7 = []
    t8 = []
    t9 = []
    t10 = []
    for ii in range(len(txt)):
        try:
            message = txt[ii] + txt[ii + 1]
        except IndexError as e:
            pass
        if len(message) == 0:
            pass
        else:
            re_n1 = re.compile("小孩|小朋友|小天使|小寶寶|孩子|懷孕|生產|同住|兒子|女兒|弟弟|妹妹|兒童|父母|公婆|結婚|未婚妻|女朋友|老婆|內人")
            re_1 = re.compile("不打算|不要|不喜歡|不想|沒有|單身")  # 適用於非一房(這是要一個房間的)

            non1 = ''
            a = re.search(re_n1, message);
            b = re.search(re_1, message)
            if a.__class__.__name__ == 'NoneType':
                non1 = int(0)
            elif a.__class__.__name__ != 'NoneType' and b.__class__.__name__ != 'NoneType':
                non1 = int(-1)
            else:
                non1 = int(1)
            t1.append(non1)

            re_pa = re.compile("開車|交通|通勤|停車|車位|機車|汽車|機械式|平面坡道|露天|車")
            re_2 = re.compile("找不到|沒有|不方便|太少|租車位|難找|需要|不好找")  # 喜歡的部分適用車位
            re_3 = re.compile("不需要|沒必要")  # 不喜歡的部分適用車位

            parking = ''
            c = re.search(re_pa, message);
            d = re.search(re_2, message);
            e = re.search(re_3, message)
            if c.__class__.__name__ == 'NoneType':
                parking = int(0)
            elif c.__class__.__name__ != 'NoneType' and d.__class__.__name__ != 'NoneType':
                parking = int(1)
            elif c.__class__.__name__ != 'NoneType' and e.__class__.__name__ != 'NoneType':
                parking = int(-1)
            else:
                parking = int(1)
            t2.append(parking)

            re_ele = re.compile("老人|父|母|長輩|樓梯|電梯|爸|媽|公公|婆婆|公婆|梯|懷孕|孕婦|行動不便")
            re_4 = re.compile("爬樓梯|沒電梯|走樓梯|累|沒有")  # 想要電梯

            ele = ''
            f = re.search(re_ele, message);
            g = re.search(re_4, message)
            if f.__class__.__name__ == 'NoneType':
                ele = int(0)
            elif f.__class__.__name__ != 'NoneType' and g.__class__.__name__ != 'NoneType':
                ele = int(1)
            else:
                ele = int(1)
            t3.append(ele)

            re_mrt = re.compile("捷運|交通|通勤|沿線|車站")
            re_bus = re.compile("公車|交通|通勤|老人|父|母|長輩|爸|媽|公公|婆婆|公婆|站牌")
            re_5 = re.compile("沒有|遠|近|需要|旁邊|走路|不用|路線|班次多|發達|方便")  # 想要捷運、公車
            re_6 = re.compile("震動|噪音|吵|人潮|擠")  # 不想要捷運、公車

            mrt = ''
            h = re.search(re_mrt, message);
            i = re.search(re_5, message);
            j = re.search(re_6, message)
            if h.__class__.__name__ == 'NoneType':
                mrt = int(0)
            elif h.__class__.__name__ != 'NoneType' and i.__class__.__name__ != 'NoneType':
                mrt = int(1)
            elif h.__class__.__name__ != 'NoneType' and j.__class__.__name__ != 'NoneType':
                mrt = int(-1)
            else:
                mrt = int(1)
            t4.append(mrt)

            re_bus = re.compile("公車|交通|通勤|老人|父|母|長輩|爸|媽|公公|婆婆|公婆|站牌")
            re_5 = re.compile("沒有|遠|近|需要|旁邊|走路|不用|路線|班次多|發達|方便")  # 想要捷運、公車
            re_6 = re.compile("震動|噪音|吵|人潮|擠")  # 不想要捷運、公車

            bus = ''
            k = re.search(re_bus, message);
            ii = re.search(re_5, message);
            jj = re.search(re_6, message)
            if k.__class__.__name__ == 'NoneType':
                bus = int(0)
            elif k.__class__.__name__ != 'NoneType' and ii.__class__.__name__ != 'NoneType':
                bus = int(1)
            elif k.__class__.__name__ != 'NoneType' and jj.__class__.__name__ != 'NoneType':
                bus = int(-1)
            else:
                bus = int(1)
            t5.append(bus)

            re_park = re.compile("公園|綠地|休憩|兒童|綠化|學區|寵物|狗|毛小孩|毛孩")
            re_conv_st = re.compile("機能|生活|便利|吃|外食|商店|店面|超商|全家|萊爾富|小七|7-11|seven|購物|全聯|愛買|頂好|家樂福|大潤發")
            re_7 = re.compile("遠|近|不方便|不佳|方便|尚可|不錯|距離|缺乏|很棒|熱鬧")  # 喜歡的部分適用生活機能、公園
            re_8 = re.compile("吵|人潮|暗|黑|老人家|早起|流浪漢|遊民|音樂|廣播|塞車|塞|人多|髒|擠|沒必要|熱鬧")  # 不喜歡的部分適用生活機能、公園

            park = ''
            n = re.search(re_park, message);
            l = re.search(re_7, message);
            m = re.search(re_8, message)

            if n.__class__.__name__ == 'NoneType':
                park = int(0)
            elif n.__class__.__name__ != 'NoneType' and l.__class__.__name__ != 'NoneType':
                park = int(1)
            elif n.__class__.__name__ != 'NoneType' and m.__class__.__name__ != 'NoneType':
                park = int(-1)
            else:
                park = int(1)
            t6.append(park)

            re_conv_st = re.compile("機能|生活|便利|吃|外食|商店|店面|超商|全家|萊爾富|小七|7-11|seven|購物|全聯|愛買|頂好|家樂福|大潤發")
            re_7 = re.compile("遠|近|不方便|不佳|方便|尚可|不錯|距離|缺乏|很棒|熱鬧")  # 喜歡的部分適用生活機能、公園
            re_8 = re.compile("吵|人潮|暗|黑|老人家|早起|流浪漢|遊民|音樂|廣播|塞車|塞|人多|髒|擠|沒必要|熱鬧")  # 不喜歡的部分適用生活機能、公園

            st = ''
            o = re.search(re_conv_st, message);
            ll = re.search(re_7, message);
            mm = re.search(re_8, message)
            if o.__class__.__name__ == 'NoneType':
                st = int(0)
            elif o.__class__.__name__ != 'NoneType' and ll.__class__.__name__ != 'NoneType':
                st = int(1)
            elif o.__class__.__name__ != 'NoneType' and mm.__class__.__name__ != 'NoneType':
                park = int(-1)
            else:
                st = int(1)
            t7.append(st)

            re_annoy = re.compile("寺廟|吵|鬧|噪音|異味|煙|廟|鞭炮|金紙|燒香|消防隊")
            re_9 = re.compile("商圈|小吃|好吃|方便")  # 想要廟
            re_0 = re.compile("屁孩|吵|鞭炮|廟會|擁擠|阻礙交通|塞車")  # 不想要廟

            tp = ''
            p = re.search(re_annoy, message);
            q = re.search(re_9, message);
            r = re.search(re_0, message)
            if p.__class__.__name__ == 'NoneType':
                tp = int(0)
            elif p.__class__.__name__ != 'NoneType' and q.__class__.__name__ != 'NoneType':
                tp = int(1)
            elif p.__class__.__name__ != 'NoneType' and r.__class__.__name__ != 'NoneType':
                tp = int(-1)
            else:
                tp = int(1)
            t8.append(tp)

            re_police_st = re.compile("派出所|治安|警察|亂|分隊|分局|混混|大隊")
            re_11 = re.compile("不好|飆車|屁孩|聚集|改車|消音器|安心")  # 想要警察局在附近
            re_12 = re.compile("警笛|很吵")  # 不想要警察局在附近

            pt = ''
            s = re.search(re_police_st, message);
            t = re.search(re_11, message);
            u = re.search(re_12, message)
            if s.__class__.__name__ == 'NoneType':
                pt = int(0)
            elif s.__class__.__name__ != 'NoneType' and t.__class__.__name__ != 'NoneType':
                pt = int(1)
            elif s.__class__.__name__ != 'NoneType' and u.__class__.__name__ != 'NoneType':
                pt = int(-1)
            else:
                pt = int(1)
            t9.append(pt)

            re_manage = re.compile("管委會|垃圾|管理|維護|維修|警衛|保全|乾淨|清潔|整齊|保潔|雜物|社區|公設比高")
            re_13 = re.compile("不用|追垃圾車|保全|打掃|公共設施|舒適")  # 喜歡管委會
            re_14 = re.compile("公設比高|管理費高|麻煩")  # 不要管委會

            mn = ''
            v = re.search(re_manage, message);
            w = re.search(re_13, message);
            x = re.search(re_14, message)
            if v.__class__.__name__ == 'NoneType':
                mn = int(0)
            elif v.__class__.__name__ != 'NoneType' and w.__class__.__name__ != 'NoneType':
                mn = int(1)
            elif v.__class__.__name__ != 'NoneType' and x.__class__.__name__ != 'NoneType':
                mn = int(-1)
            else:
                mn = int(1)
            t10.append(mn)
    '''分析想要一房格局'''
    if 1 in t1 and -1 in t1:  # [-1,1], [-1,0,1]
        Non_1 = min(t1)
    elif not -1 in t1:  # [0,1],[0],[1]
        Non_1 = max(t1)  # 0,1
    else:  # [-1],[-1,0]
        Non_1 = min(t1)  # -1
    '''分析需不需要車位'''
    if min(t2) - max(t2) == -2:
        Parking = min(t2)
    elif min(t2) - max(t2) == -1:
        Parking = max(t2)
    else:
        Parking = max(t2)
    '''分析需不需要電梯'''
    if min(t3) - max(t3) == -2:
        Elevator = min(t3)
    elif min(t3) - max(t3) == -1:
        Elevator = max(t3)
    else:
        Elevator = max(t3)
    '''分析喜不喜歡在捷運站、公車站牌附近'''
    if min(t4) - max(t4) == -2:
        MRT = min(t4)
    elif min(t4) - max(t4) == -1:
        MRT = max(t4)
    else:
        MRT = max(t4)
    '''分析喜不喜歡在捷運站、公車站牌附近'''
    if min(t5) - max(t5) == -2:
        Bus = min(t5)
    elif min(t5) - max(t5) == -1:
        Bus = max(t5)
    else:
        Bus = max(t5)
    '''分析喜不喜歡在公園、賣場旁邊'''
    if min(t6) - max(t6) == -2:
        Park = min(t6)
    elif min(t6) - max(t6) == -1:
        Park = max(t6)
    else:
        Park = max(t6)
    '''分析喜不喜歡在公園、賣場旁邊'''
    if min(t7) - max(t7) == -2:
        Market = min(t7)
    elif min(t7) - max(t7) == -1:
        Market = max(t7)
    else:
        Market = max(t7)
    '''分析喜不喜歡在廟宇附近'''
    if min(t8) - max(t8) == -2:
        Noise = min(t8)
    elif min(t8) - max(t8) == -1:
        Noise = max(t8)
    else:
        Noise = max(t8)
    '''分析喜不喜歡在派出所(警局)附近'''

    if min(t9) - max(t9) == -2:
        Police_station = min(t9)
    elif min(t9) - max(t9) == -1:
        Police_station = max(t9)
    else:
        Police_station = max(t9)

    '''分析喜不喜歡有管委會附近'''

    if min(t10) - max(t10) == -2:
        Management = min(t10)
    elif min(t10) - max(t10) == -1:
        Management = max(t10)
    else:
        Management = max(t10)

    js = {'Non_1': Non_1, "Parking": Parking,
          "Elevator": Elevator, "MRT": MRT,
          "Bus": Bus, "Park": Park, "Market": Market,
          "Noise": Noise, "Police_station": Police_station, "Management": Management}
    print(js)


if __name__ == "__main__":
    main()