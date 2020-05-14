import requests
import re
from bs4 import BeautifulSoup
import os


url0 = 'http://syds.ngchina.cn/prize/jsp'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }

def get_page(url):
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def store_img(url):
    r = requests.get(url, stream = True)
    filename = url.split('/')[-1]

    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 32):
            f.write(chunk)

def main():
    os.chdir('/Users/wangshizhu/Desktop')
    os.mkdir('ng')
    os.chdir('/Users/wangshizhu/Desktop/ng')

    main_page = get_page(url0)
    sub_page_urls = []
    for a in main_page.find_all(href = re.compile(r'/match/cotton/opus')):
        sub_page_urls.append('http://syds.ngchina.cn' + a['href'])
    
    print(sub_page_urls)
    
    for url in sub_page_urls:
        sub_page = get_page(url)
        print(url)
        for img in sub_page.find_all('img', src=re.compile(r'/resc/picture/2018\d+.jpg')):
            img_url = 'http://syds.ngchina.cn' + img['src']
            store_img(img_url)
            print(img_url)

if __name__ == '__main__':
    main()
    
