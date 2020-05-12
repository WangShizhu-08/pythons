import urllib.request as request
import urllib.parse as parse
import os
import re

url = 'http://jandan.net/ooxx/MjAyMDA1MDctMjA'

def open_url(url):
    req = request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36')
    response = request.urlopen(req)
    html = response.read()
    return html

def get_img(html):
    img_addrs = re.findall(r'w[xw][a-zA-Z0-9/\.]+\.jpg',html)
    return img_addrs

def img_save(img_addrs):
    for each in img_addrs:
        filename = each.split('/')[-1]
        print(filename) 
        with open(filename, 'wb') as f:
            img = open_url('http://' + each)
            f.write(img)

os.chdir('/Users/wangshizhu/Desktop')
os.mkdir('XXOO')
os.chdir('/Users/wangshizhu/Desktop/XXOO')

for i in range(0,6):
    #form page urls
    page_url = url + str(i) + '#comments'
    
    print(page_url)

    html = open_url(page_url).decode('utf-8')

    img_addrs = get_img(html)

    img_save(img_addrs)


