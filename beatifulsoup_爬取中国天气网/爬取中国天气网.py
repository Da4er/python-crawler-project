import requests
from bs4 import BeautifulSoup
from pyecharts.charts.bar import Bar
ALL_DATA=[]
def parse_page(url):
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    resp=requests.get(url,headers=headers)
    #print(resp.text)
    text=resp.content.decode("utf-8")
    # print(text)
    #这里使用的解析器是html5lib，因为在使用常用的lxml解析器容错率不好，港澳台天气这个页面html书写不规范，从而无法正常爬取。
    #pip install html5lib
    soup=BeautifulSoup(text,"html5lib")
    divs=soup.find("div",class_="conMidtab") #获取第一个div标签
    tables=divs.find_all("table")
    for table in tables:
        trs=table.find_all("tr")[2:]
        for index,tr in enumerate(trs):
            # print(tr)
            # print("="*30)
            tds=tr.find_all("td")
            if(index==0):
                city_td=tds[1]
            else:
                city_td=tds[0]
            city=list(city_td.stripped_strings)[0]
            # print(city)
            temp_td=tds[-2]
            temp=list(temp_td.stripped_strings)[0]
            # print({'city':city,'temp':temp})
            data={'city':city,'temp':int(temp)}
            ALL_DATA.append(data)
def spider():
    base_url="http://www.weather.com.cn/textFC/{}.shtml"
    params=["hb","db","hd","hz","hn","xb","xn","gat"]
    for param in params:
        url=base_url.format(param)
        parse_page(url)
    ALL_DATA.sort(key=lambda x:x['temp'])
    # print(ALL_DATA)
    data=ALL_DATA[0:10]
    cicties=list(map(lambda x:x['city'],data))
    temps=list(map(lambda x:x['temp'],data))
    chart=Bar("中国天气排行榜")
    chart.add("",cicties,temps)
    chart.render('temp.html')
if __name__ == '__main__':
    spider()