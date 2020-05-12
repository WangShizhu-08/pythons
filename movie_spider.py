import urllib.request
import re
import os

def get_page(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    return html

def find_title(html):
    pat_title = re.compile(r'<span class="title">(\w+)</span>')
    result = pat_title.findall(html)
    return result

def find_rating(html):
    pat_rating = re.compile(r'<span class="rating_num" property="v:average">(\d\.\d)</span>')
    result = pat_rating.findall(html)
    return result

fin_result = {}

for i in range(0,10):
    url = "https://movie.douban.com/top250?start={}&filter=".format(str(i*25))

    html = get_page(url)
    
    titles = find_title(html)
    ratings = find_rating(html)

    toplist = list(zip(titles, ratings))


    for item in toplist:
        fin_result[item[0]] = item[1]


os.chdir('/Users/wangshizhu/Desktop/python')

with open('DoubanTop250.txt','w') as f:
    for k,v in fin_result.items():
        line = k + ' ' + v + '\n'
        f.write(line)
	

    
