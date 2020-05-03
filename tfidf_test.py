import csv
import math
def open_file():
    total = []
    with open("C:/ckip-learning/mobile01_output_mo02.csv", 'r', encoding='utf-8', newline='') as f:
        rows = csv.reader(f)
        content = []
        for row in rows:
            sentence = row[3].replace(',', ' ')
            content.append(sentence)
        total.append(content)
    return total

def idf(corpus):
    idfs = {}
    d = 0.0
    for doc in corpus:
        d += 1
        counted = []
        for word in doc:
            if not word in counted:
                counted.append(word)
                if word in idfs:
                    idfs[word] += 1
                else:
                    idfs[word] = 1
    for word in idfs:
        idfs[word] = math.log(d/float(idfs[word]))
    return idfs
def tf_idf(re_read):
    corpus = re_read # 此處獲取的語料庫是每篇文章的分詞結果列表的列表
    idfs = idf(corpus)
    all_words = []
    for doc in corpus:
        tfidfs = {}
        for word in doc:
            if word in tfidfs:
                tfidfs[word] += 1
            else:
                tfidfs[word] = 1
        for word in tfidfs:
            tfidfs[word] *= idfs[word]
        all_words.append(tfidfs)
    return all_words

if __name__ == "__main__":
    a = open_file()
    b = tf_idf(a)
    print(b)

