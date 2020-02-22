import re
import requests
HEADERS={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
}
def get_detail_page(url):
    resp=requests.get(url,headers=HEADERS)
    text=resp.text
    detail_pages=re.findall(r'<div\sclass="main-bd">.*?<a\shref="(.*?)">.*?</a>',text,re.DOTALL)
    return detail_pages
def handle_detail_page(url):
    book={}
    resp=requests.get(url,headers=HEADERS)
    text=resp.text
    titles=re.findall(r'<div\sclass="article">.*?<span.*?>(.*?)</span>',text,re.DOTALL)
    articles_tmp=re.findall(r'<div\sid="link-report">.*?<p>.*</p>',text,re.DOTALL)
    articles=[]
    for a in articles_tmp:
        x=re.sub(r'<.*?>','',a)
        y=x.replace('\r','').replace('\n','')
        a=re.sub(r'<div\s.*?>','',y)
        b=a.replace(' ','')
        articles.append(b)
    # print(articles)
    # print(titles)
    book={
        'title':titles,
        'article':articles
    }
    print(book)
def main():
    urls=[]
    base_url="https://book.douban.com/review/best/?start={}"
    for i in range(0,41,20):
        url=base_url.format(i)
        urls.append(url)
    for a in urls:
        detail_urls=get_detail_page(a)
        for f in detail_urls:
            handle_detail_page(f)
if __name__ == '__main__':
    main()