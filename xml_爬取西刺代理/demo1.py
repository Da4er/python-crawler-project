import requests
from lxml import etree
import csv
header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
}
def spider(url):
    proxy_ips=[]
    resp=requests.get(url,headers=header)
    text=resp.text
    html=etree.HTML(text)
    ips=html.xpath("//table[@id='ip_list']//tr[@class='odd']//td[2]//text()")
    ports=html.xpath("//table[@id='ip_list']//tr[@class='odd']//td[3]//text()")
    type_https=html.xpath("//table[@id='ip_list']//tr[@class='odd']//td[6]//text()")
    for i in range(len(ips)):
        proxy_ip={
            'ip':ips[i],
            'port':ports[i],
            'type_http':type_https[i]
        }
        proxy_ips.append(proxy_ip)
    return proxy_ips
def main():
    base_url="https://www.xicidaili.com/nn/{}"
    headers = {"ip", 'port', 'type_http'}
    proxy_ips=[]
    for i in range(1,10):
        url=base_url.format(i)
        proxy_ip=spider(url)
        proxy_ips +=proxy_ip
    print(proxy_ips)    
    with open('proxy_ip.csv','w',encoding='utf-8',newline='') as fp:
         writer=csv.DictWriter(fp,headers)
         writer.writeheader()
         writer.writerows(proxy_ips)
if __name__ == '__main__':
    main()