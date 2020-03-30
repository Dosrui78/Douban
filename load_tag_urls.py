import requests,redis
from pyquery import PyQuery as pq 

def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    res = requests.get(url,headers=headers)
    print("status:%d"%res.status_code)

    html = res.text
    doc = pq(html)
    #设置redis数据库信息
    link = redis.Redis(host='localhost',port=6379)
    items = doc('table.tagCol tr td a')
    for a in items.items():
        tag = a.attr('href')
        link.lpush('book:tag_urls',tag)
    print("共计%d条标签"%len(items))

if __name__ == '__main__':
    main()