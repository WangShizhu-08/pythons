import asyncio
import aiohttp
import urllib.request
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re
import time
import multiprocessing as mp

base_url = 'https://morvanzhou.github.io/'

seen = set()
unseen = set([base_url,])

async def get_page(url, session):
    res = await session.get(url)
    html = await res.text()
    return html

def parse(html):
    soup = bs(html, 'lxml')
    urls = soup.find_all('a', {'href': re.compile(r'^/.+?/$')})
    
    title = soup.find('h1').get_text().strip()
    page_urls = set([urljoin(base_url, url['href']) for url in urls])
    url = soup.find('meta', {'property': 'og:url'})['content']
    return page_urls, title, url

async def main(loop):
    pool = mp.Pool()
    async with aiohttp.ClientSession() as session:
        count = 1
        while len(unseen) != 0:
            # 访问网站是I/O相关，使用异步效率更高，在访问某一URL的时候可以同时访问另一个URL
            print('Async Getting pages from unseen urls...')
            # create task, but not start task
            tasks = [loop.create_task(get_page(url, session)) for url in unseen]
            # run task and wait for all tasks 
            finished, unfinished = await asyncio.wait(tasks)
            # get all htmls in finished
            htmls = [f.result() for f in finished]
            
            # 分析网页获得相关信息是computing tasks,最好是利用多核计算机的multiprocessing功能
            print('Parsing...')
            # [pool.apply_async(func, args(arg,)) for arg in list] 生成器
            parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
            # type(pool.apply_async()) is generator, type(parse_jobs) is list
            results = [i.get() for i in parse_jobs]

            print('Updating Seen Urls')  
            seen.update(unseen)
            print('Clearing {} unseen urls'.format(len(unseen)))
            unseen.clear()

            for page_urls, title, url in results:
                print(count, title, url)
                count += 1
                unseen.update(page_urls - seen)

if __name__ == '__main__':
    t1 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
    print('Total time: %.1f s' % (time.time()-t1, ))