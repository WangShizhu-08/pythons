import asyncio
import time

def job(t):
    print('start job', t)
    time.sleep(t)
    print('Job', t, 'takes', t, 's')

def main_normal():
    [job(t) for t in range(1,3)]


async def job_a(t):
    print('start job', t)
    await asyncio.sleep(t)    #等待t秒，期间切换其他任务
    print('Job', t, 'takes', t, 's')

async def main_async(loop):
    tasks = [loop.create_task(job_a(t)) for t in range(1,3)]  # 创建任务，但不执行
    await asyncio.wait(tasks) # 执行并等待所有任务完成

print('No asyncio Start:')
t1 = time.time()
main_normal()
print('No asyncio time: ', time.time() - t1)


print('Asyncio Start:')
t2 = time.time()
loop = asyncio.get_event_loop()            #建立loop
loop.run_until_complete(main_async(loop))  #执行loop
loop.close()                               #关闭loop
print("Async total time : ", time.time() - t2)
