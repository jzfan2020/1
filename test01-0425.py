import requests as ss
from bs4 import BeautifulSoup as bs
import json
import re
import os

path = r'./mobile_01'
if not os.path.exists(path):
    os.mkdir(path)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}

#過濾特殊字元
def filter_str(disstr, restr=''):
    res = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
    return res.sub(restr,disstr)
#找出討論版的最終頁碼
def find_total_page(url1):
    res_total = ss.get(url=url1, headers=headers)
    soup_total = bs(res_total.text, 'html.parser')
    page_num = soup_total.select('div[class="l-tabulate__action"] li')
    for p in range(len(page_num)):
        last_num = max(page_num[p])['data-page']
    last_num = int(last_num)
    return last_num
#找出討論主題的最終頁碼
def find_final_page(url2):
    res_final = ss.get(url=url2, headers=headers)
    soup_final = bs(res_final.text, 'html.parser')
    page_final = soup_final.select('ul[class="l-pagination"] li')
    if len(page_final) == 0:
        last_page = 1
    else:
        for j in range(len(page_final)):
            last_page = max(page_final[j])['data-page']
            last_page = int(last_page)
    return last_page
#存成json檔
def save_file(name, sentence):
    sentence = json.dumps(sentence, ensure_ascii=False)
    with open('./mobile_01/'+ name +'.txt', 'w', encoding='utf-8') as s:
        s.write(sentence)


def main():
    pages = find_total_page('https://www.mobile01.com/topiclist.php?f=455')
    #換頁
    for page in range(1, pages):
        url = 'https://www.mobile01.com/topiclist.php?f=455&p=%s' % page
        # print(url)
        res = ss.get(url=url, headers=headers)
        soup = bs(res.text, 'html.parser')
        title = soup.select('div[class="c-listTableTd__title"] a')
        print('第{}頁'.format(page))
        for each_title in title:
            try:
                int(each_title.text)
            except ValueError as e:
                #進入每篇討論文
                url_title = 'https://www.mobile01.com/' + each_title['href']
                id = each_title['href'].split('t=')[1]
                print(url_title)
                res2 = ss.get(url=url_title, headers=headers)
                soup2 = bs(res2.text, 'html.parser')
                post_date = soup2.select('li[class="l-toolBar__item"] span[class="o-fNotes o-fSubMini"]')[0].text
                #主文
                main_content = soup2.select('div[itemprop="articleBody"]')[0].text.strip()
                main_content = filter_str(main_content)
                post_date = soup2.select('li[class="l-toolBar__item"] span[class="o-fNotes o-fSubMini"]')[0].text
                content = {"id" : id,
                           "post_date" : post_date,
                           "content" : main_content}
                # save_file(id, id, main_content)
                title_pages = find_final_page(url_title)
                for k in range(1, title_pages + 1):
                    url_each = url_title + '&p=%s' % k
                    res3 = ss.get(url=url_each, headers=headers)
                    soup3 = bs(res3.text, 'html.parser')
                    comments = soup3.select('div[class="u-gapBottom--max c-articleLimit"]')
                    post = soup3.select('span[class="o-fNotes o-fSubMini"]')
                    # 把每則評論找出來並且刪掉wrote、恕刪該行
                    for i in range(len(comments)):
                        comments_list = comments[i].text.strip().split('\n')
                        c_list = []
                        for m in range(len(comments_list)):
                            #         print(comments_list[j])
                            if comments_list[m].find('wrote') != -1:
                                pass
                            elif comments_list[m].find('恕刪') != -1:
                                pass
                            else:
                                c_list.append(filter_str(comments_list[m]))
                        comment = ''.join(c_list)
                        if k == 1:
                            for n in range(len(post)):
                                if n == i:
                                    post_time = post[2*(n+1)+2].text
                                else:
                                    pass
                        else:
                            for n in range(len(post)):
                                if n == i:
                                    post_time = post[2*n+2].text
                                else:
                                    pass
                        result = {'id' : id+'_'+str(k)+'_'+str(i),
                                  "post_date": post_time,
                                 "comment": comment
                                 }
                        save_file(id+'_'+str(k)+'_'+str(i), result)
if __name__ == "__main__":
    main()
