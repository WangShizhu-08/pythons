import urllib.request
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re
import time
import multiprocessing as mp

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
pool = mp.Pool()


while len(unseen) != 0:
    print('Getting pages from unseen urls...')
    #htmls = [get_page(url) for url in unseen] normal_deed
    # htmls = pool.map(get_page, unseen) also works, but slower. Guessing:"It blocks until the result is ready."
    crawl_jobs = [pool.apply_async(get_page, args=(url,)) for url in unseen]
    htmls = [j.get() for j in crawl_jobs]
    
    print('Parsing...')
    #results = [parse(html) for html in htmls] normal_deed
    parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
    #type(pool.apply_async()) is generator, type(parse_jobs) is list
    results = [i.get() for i in parse_jobs]

    print('Updating Seen Urls')  
    seen.update(unseen)
    print('Clearing {} unseen urls'.format(len(unseen)))
    unseen.clear()

    for page_urls, title, url in results:
        print(count, title, url)
        count += 1
        unseen.update(page_urls - seen)
        
print('Total time: %.1f s' % (time.time()-t1, ))
