import requests
from lxml import etree
HEADERS={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
def get_detail_url(url):
    resp=requests.get(url,headers=HEADERS)
    text=resp.text
    html=etree.HTML(text)
    detail_urls=html.xpath("//ol[@class='grid_view']//div[@class='pic']//a//@href")
    # for detail_url in detail_urls:
    #     print(detail_url)
    return detail_urls
def handle_detai_url(url):
    movie={}
    resp=requests.get(url,headers=HEADERS)
    text=resp.text
    html=etree.HTML(text)
    ranking=html.xpath("//div[@class='top250']//span[@class='top250-no']//text()")[0]
    movie["ranking"]=ranking
    title=html.xpath("//span[@property='v:itemreviewed']//text()")[0]
    movie["title"]=title
    year=html.xpath("//span[@class='year']//text()")[0].replace("(","").replace(")","")
    movie["year"]=year
    poster=html.xpath("//a[@class='nbgnbg']//img/@src")[0]
    movie["poster"]=poster
    infos=html.xpath("//div[@id='info']")
    for info in infos:
        director=info.xpath(".//a[@rel='v:directedBy']//text()")[0]
        movie['director']=director
        actors=info.xpath(".//a[@rel='v:starring']//text()")
        movie['actors']=actors
    return movie
def spider():
    base_url="https://movie.douban.com/top250?start={}&filter="
    movies=[]
    for i in range(0,226,25):
        url=base_url.format(i)
        detail_urls=get_detail_url(url)
        for detail_url in detail_urls:
            movie=handle_detai_url(detail_url)
            movies.append(movie)
    with open("数据.txt",'w',encoding="utf-8") as fp:
        fp.write(str(movies))
if __name__ == '__main__':
    spider()
