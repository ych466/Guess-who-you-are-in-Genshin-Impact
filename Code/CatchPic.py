import aiohttp
import asyncio
from fake_useragent import UserAgent
import os
import json
import sys
import aiofiles
ua = UserAgent()
urls=[]
headers_str = {'User-Agent':ua.random,'Cookie':''} #请自行配置Cookie
async def geturl(name,session,num_max):
    url=f"https://www.pixiv.net/ajax/search/artworks/{name}"
    params={
        'word':name,
        'order':'popular_d',
        'mode':'all',
        'p':1,
        's_mode':'s_tag',
        'type':'all',
        'lang':'zh',
        'version':'0a3aef14e017e59001029824585666bfde1612b9'
    }
    headers = headers_str
    num=0
    while True:
        try:
            async with session.get(url,params=params,headers=headers) as res:
                text=await res.text()
                l=[(name,x['url']) for x in json.loads(text)['body']['illustManga']['data']]
                if len(l)+num>=num_max:
                    urls.extend(l[:num_max-num])
                    break
                else:
                    urls.extend(l)
                    num+=len(l)
            params['p']+=1
        except:
            await asyncio.sleep(1)

async def download(session):
    async with aiohttp.ClientSession() as session:
        while True:
            if len(urls)==0:
                await asyncio.sleep(1)
                continue
            (name,url)=urls.pop(0)
            if not os.path.exists('dataset/'+name):
                os.makedirs(f'dataset/{name}')
                print(f'新建文件夹：dataset/{name}')
            headers = headers_str
            while True:
                try:
                    async with session.get(url,headers=headers) as res:
                        content=await res.content.read()
                        async with aiofiles.open(f'dataset/{name}/{url.split("/")[-1].split("_")[0]}.jpg', 'wb') as f:
                            await f.write(content)
                            global total
                            total+=1
                    break
                except:
                    await asyncio.sleep(1)
                
        
total=0
async def output(totalmax):
    old=0
    speed=0
    while True:
        await asyncio.sleep(1)
        sys.stdout.flush()
        speed=speed*0.8+0.2*(total-old)
        print(f'\r{total}/{totalmax} {format(speed, ".2f")}it/s leave {len(urls)}it',end='')
        old=total
        if total==totalmax:return   

async def main(namelist,n_worker,num_max):
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            for name in namelist:
                tg.create_task(geturl(name,session,num_max))
            for _ in range(n_worker):
                tg.create_task(download(session))
            tg.create_task(output(num_max*len(namelist)))


namelist=['丘丘人'] #需要拉取的内容
n_worker=30 #开启线程数
num_max=25000 #每个关键字抓取图片数量
asyncio.run(main(namelist,n_worker,num_max))



