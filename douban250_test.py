import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup as bs
import multiprocessing as mp
import re
import time
import random

urls = ["https://movie.douban.com/top250?start={}&filter=".format(str(i*25)) for i in range(0,10)]
headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}
count = 1

async def get_page(url, session):
    res = await session.get(url, headers = headers)
    html = await res.text()
    return html

def parse(html):
    soup = bs(html, 'lxml')
    titles = [s.string for s in soup.find_all('span', class_= 'title')]
    ratings = [s.string for s in soup.find_all('span', class_='rating_num')]
    return titles, ratings

async def main(loop):
    pool = mp.Pool()
    async with aiohttp.ClientSession() as session:
        print('Getting htmls from Douban')
        # 建立tasks 但不运行
        tasks = [loop.create_task(get_page(url, session)) for url in urls]
        # 运行tasks 等待所有tasks完成 并放入finished里
        finished, unfinished = await asyncio.wait(tasks)
        # 从finished 里拿出结果 返回到htmls里
        htmls = [h.result() for h in finished]

        print('Start Parsing...')
        parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
        results = [i.get() for i in parse_jobs]

if __name__ == '__main__':
    t1 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
    print('Time Consumed: ', time.time()- t1)





