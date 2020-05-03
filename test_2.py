# test for emotion (CSV格式檔按適用)
import csv
import os.path
import re
from ckiptagger import WS, construct_dictionary
import json


# 刪掉標點符號
def remove_punctuation(line):
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('', line)
    return line


# 移除小寫英文字元、數字等等(大寫的可能會是機場捷運站名，故先保留)
def word_filter(word):
    pattern = '[^a-z0-9\+\-\*\/]+'
    #     print(re.findall(pattern, word))
    return re.findall(pattern, word)


# 先把random 出來的檔案id、內容找出來
def random_file_collection(path):
    total = []
    selected_files = os.listdir(path)
    for selected_file in selected_files:
        with open(path + selected_file, newline='', encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                js = {"id": row[0],
                      "title": row[1],
                      "post_date": row[2],
                      "content": row[3]
                      }
                total.append(js)
                # print(js)
    return total
#檢查是否已經斷詞:
def check_func():
    complete_list = []
    with open('C:/ckip-learning/mobile01_output_mo04.csv', 'r' , newline='', encoding='utf-8') as cs:
        rows1 = csv.reader(cs)
        for row1 in rows1:
            complete_list.append(row1[0])
    return complete_list


# 匯入停用詞再執行斷字斷詞(刪掉小寫、數字，保留大寫是因為有可能是捷運站名)
def word_seg(text):
    userdic = []
    userDic = {}
    with open('C:/ckip-learning/project/Dict/userDict.txt', 'r', encoding='utf-8') as f1:
        us = f1.readlines()
        for t in us:
            t1 = t.replace('\n', '')
            if len(t1) == 1:
                pass
            else:
                userdic.append(t1)
        for t2 in userdic:
            userDic[t2] = 1
    dictionary = construct_dictionary(userDic)
    stopWords = []
    ws_result = []
    with open('C:/ckip-learning/project/Dict/stopDict.txt', 'r', encoding='utf-8') as s:
        st = s.readlines()
        for std in st:
            stopWords.append(std.replace('\n', ''))
    ws = WS('C:/ckip-learning/data')
    words = ws([text], recommend_dictionary=dictionary)
    for word in words[0]:
        if word in stopWords:
            pass
        elif len(word_filter(word)) == 0:
            pass
        else:
            ws_result.append(word)
    res = ','.join(ws_result)
    return res


# 將斷完詞的結果存檔
# def save_result(name, result):
#     result1 = json.dumps(result, ensure_ascii=False)
#     with open('E:/DMtest/emotion_test/' + name + '.txt', 'w', encoding='utf-8') as sv:
#         sv.write(result1)

def save_csv(dic):
    with open('C:/ckip-learning/project/result/mobile01_output_mo04.csv', 'a+', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["id", "title", "post_time", "seg_result"]
        # 將 dictionary 寫入 CSV 檔
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 寫入第一列的欄位名稱
        # writer.writeheader()
        # 寫入資料
        writer.writerow(dic)

    # 把評論找出來


def main():
    completed = check_func()
    t = random_file_collection('C:/ckip-learning/project/mo04/')
    for t1 in t:
        id_each = t1['id']
        title_each = t1['title']
        post = t1['post_date']
        if id_each == 'id':
            pass
        elif id_each in completed:
            pass
        else:
            print("開始執行 {}".format(id_each))
            txt = t1['content'].split(';')[0]
            comments = t1['content'].split(';')[1:]

            content_seg = word_seg(remove_punctuation(txt))
            content_result = {"id": id_each,
                              "title": title_each,
                              "post_time": post,
                              "seg_result": content_seg
                              }

            save_csv(content_result)
            temp = []
            for i in range(len(comments)):
                if len(comments[i]) == 0:
                    pass
                else:
                    comment_seg = word_seg(remove_punctuation(comments[i]))
                    # print(comment_seg)
                    comment_result = {"id": str(id_each) + '_' + str(i),
                                      "title": title_each,
                                      "post_time": post,
                                      "seg_result": comment_seg}

                    save_csv(comment_result)

    print('完成~')


if __name__ == "__main__":
    main()