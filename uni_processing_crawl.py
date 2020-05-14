import urllib.request
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re
import time

base_url = 'https://morvanzhou.github.io/'

def get_page(url):
    res = urllib.request.urlopen(url)
    return res.read().decode('utf-8')

def parse(html):
    soup = bs(html, 'lxml')
    urls = soup.find_all('a', {'href': re.compile(r'^/.+?/$')})
    
    title = soup.find('h1').get_text().strip()
    page_urls = set([urljoin(base_url, url['href']) for url in urls])
    url = soup.find('meta', {'property': 'og:url'})['content']
    return page_urls, title, url

seen = set()
unseen = set([base_url,])
count, t1 = 1, time.time()


while unseen != set():
    htmls = []
    results = []
    
    print('Getting pages from unseen urls...')
    htmls = [get_page(url) for url in unseen]
        
    print('Parsing...')
    results = [parse(html) for html in htmls]

    print('Updating Seen Urls')  
    seen.update(unseen)
    print('Clearing {} unseen urls'.format(len(unseen)))
    unseen.clear()

    for page_urls, title, url in results:
        print(count, title, url)
        count += 1
        unseen.update(page_urls - seen)
        
print('Total time: %.1f s' % (time.time()-t1, ))
