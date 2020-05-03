##先把東西丟進來分詞
from ckiptagger import WS
import json
import os.path
import os
import csv

#輸入停用詞
stopwords = []
with open('C:/ckip-learning/stopwords.txt', 'r', encoding='utf-8') as st:
    s = st.readlines()
    for std in s:
        stopwords.append(std.replace('\n',''))


#打開所有檔案並讀出要讀出來的內容供後續分詞用
def main():
    files = os.listdir('C:/ckip-learning/mobile_01/')
    for file in files:
        with open('C:/ckip-learning/mobile_01/'+file, 'r', encoding='utf-8') as f:
            t = f.read()
            t1 = json.loads(t)
            print('start {}'.format(t1['id']))
            txt = t1['comment']
            po = t1['post_date']
            sep = seg(txt)
            result = {"id" : t1['id'], "post_time" : po, "seg_result" : sep}
            save_csv(result)
            del result
#斷詞
def seg(content):
    ws = WS('C:/ckip-learning/data')
    temp = []
    words = ws([content])
    for word in words[0]:
        if word in stopwords:
            pass
        else:
            temp.append(word)

    ws_result = ' '.join(temp)

    return ws_result
#存成csv檔
def save_csv(dic):
    with open('C:/ckip-learning/output.csv', 'a+', newline='',encoding='utf-8') as csvfile:
        fieldnames=["id", "post_time", "seg_result"]
        # 將 dictionary 寫入 CSV 檔
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 寫入第一列的欄位名稱
        # writer.writeheader()
        # 寫入資料
        writer.writerow(dic)
if __name__ == "__main__":
    main()