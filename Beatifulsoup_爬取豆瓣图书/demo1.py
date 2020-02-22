import requests
import csv
from bs4 import BeautifulSoup
header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
}
headers=['书名','相关信息','评分']
def spdier(url):
    resp=requests.get(url,headers=header)
    text=resp.text
    html=BeautifulSoup(text,"lxml")
    # print(html.prettify())
    alist=html.find_all('a',class_='title')
    titles=[]
    for a in alist:
        title=list(a.stripped_strings)[0]
        titles.append(title)
    infolist=html.find_all('div',class_='desc')
    infos=[]
    for info in infolist:
        info1=list(info.stripped_strings)[0]
        infos.append(info1)
    ratelist=html.find_all('span',class_='rating_nums')
    rates=[]
    for i in ratelist:
        rate=list(i.stripped_strings)[0]
        rates.append(rate)
    books=[]
    for i in range(len(rates)):
        book={
            '书名':titles[i],
            '相关信息':infos[i],
            '评分':rates[i]
        }
        books.append(book)
    return books
def csv_storage(list_books,filename):
    with open(filename,'w',encoding='utf-8',newline='') as fp:
        writer=csv.DictWriter(fp,headers)
        writer.writeheader()
        writer.writerows(list_books)
def main():
    base_url="https://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/book?start={}"
    books=[]
    for i in range(0,136,15):
        url=base_url.format(i)
        book=spdier(url)
        books +=book
    csv_storage(books,'豆瓣图片.csv')
if __name__ == '__main__':
    main()