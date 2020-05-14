import requests
import asyncio
import aiohttp
import time

URL = 'https://morvanzhou.github.io/'

def normal():
    for i in range(2):
        r = requests.get(URL)
        url = r.url
        print(url)

async def job(session):                             #async def
    response = await session.get(URL)               #while requesting, start another task
    return str(response.url)

async def main(loop):
    async with aiohttp.ClientSession() as session:
        tasks = [loop.create_task(job(session)) for _ in range(2)]  #create job, but not start
        finished, unfinished = await asyncio.wait(tasks)            #run jobs and wait for all results
        all_results = [r.result() for r in finished]                #get results from all finished ones
        print(all_results)

t1 = time.time()
normal()
print('In normal case, it takes ', time.time()-t1, 's')

t2 = time.time()
loop = asyncio.get_event_loop()                     #create loop
loop.run_until_complete(main(loop))                 #run loop until all complete
loop.close()                                        #close loop
print("Async total time:", time.time() - t2)
