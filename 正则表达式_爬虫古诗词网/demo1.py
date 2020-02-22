import re
import requests

def handler_url(url):
    header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
    }
    reponse=requests.get(url,header)
    text=reponse.text
    titles=re.findall(r'<div\sclass="cont">.*?<b>(.*?)</b>',text,re.DOTALL)
    years=re.findall(r'<p\sclass="source"><a.*?>(.*?)</a>',text,re.DOTALL)
    autors=re.findall(r'<p\sclass="source">.*?<a.*?>.*?<a.*?>(.*?)</a>',text,re.DOTALL)
    contents_tmp=re.findall(r'<p\sclass="source">.*?<div\sclass="contson"\s.*?>(.*?)</div>',text,re.DOTALL)
    contents=[]
    for c in contents_tmp:
        x=re.sub(r'<.*?>','',c)
        contents.append(x.strip())
    poems=[]
    for value in zip(titles,years,autors,contents):
        title,year,autor,content=value
        poem={
            "title":title,
            "year":year,
            "autor":autor,
            "content":content
        }
        poems.append(poem)
    for a in poems:
        print(a)

def main():
    base_url="https://www.gushiwen.org/default_{}.aspx"
    for i in range(1,7):
        url=base_url.format(i)
        handler_url(url)

if __name__ == '__main__':
    main()