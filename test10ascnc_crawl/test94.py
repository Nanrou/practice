# coding:utf-8
"""
写一个独立resquest的方法

"""


import asyncio
from asyncio import Queue
import time
from urllib import parse
import re
import os
import csv
import codecs

import redis
import aiohttp
import lxml
from lxml import etree

from testlogging import MyLogger
from my_bloom_filter import MyBloomFilter

STROEPATH = os.path.abspath('/') + 'op'

logger = MyLogger('op.out')

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0 '}


def is_redirect(response):
    return response.status in (300, 301, 302, 303, 307)


class OpCrawler:
    def __init__(self, urls=None,
                 exclude=None, strict=True,
                 max_redirect=4, max_tries=4,
                 max_tasks=10, redis_db=0, *, loop=None):

        self.loop = loop or asyncio.get_event_loop()
        self.urls = urls
        self.exclude = exclude
        self.strict = strict
        self.max_redirect = max_redirect
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.q = Queue(loop=self.loop)
        self.done = []
        self.session = aiohttp.ClientSession(loop=self.loop, headers=HEADERS)

        self.redis_db = redis_db
        self.rcon = redis.StrictRedis(db=self.redis_db)
        self.bfcon = MyBloomFilter(db=self.redis_db, bit_size=1 << 23)
        if self.rcon.scard('buff_urls'):
            uncompleted_urls = self.rcon.smembers('buff_urls')
            for uncompleted_url in uncompleted_urls:
                self.add_url(uncompleted_url)
        if isinstance(urls, list):
            for url in self.urls:
                self.add_url(url)
        else:
            if urls:
                self.add_url(urls)

    def add_url(self, url, max_redirect=None):
        if not url:
            return
        if isinstance(url, bytes):  # 从redis里取出来的值是bytes类，需转换
            url = str(url, encoding='utf-8')
        if max_redirect is None:
            max_redirect = self.max_redirect

        if self.bfcon.is_contains(url, 'bf_seen_urls'):
            if not self.bfcon.is_contains(url, 'bf_done_urls'):
                self.q.put_nowait((url, max_redirect))
        else:
            self.bfcon.insert(url, 'bf_seen_urls')
            self.rcon.sadd('buff_urls', url)  # 创建一个缓存的set，在完成时去掉该url
            self.rcon.lpush('list_seen_urls', url)  # 用redis去存目标url
            self.q.put_nowait((url, max_redirect))

    async def crawl(self):  # 产生worker去做事
        workers = [asyncio.Task(self.work(), loop=self.loop)
                   for _ in range(self.max_tasks)]
        await self.q.join()
        for w in workers:
            w.cancel()

    async def work(self):  # 从queue中拿目标url来爬取
        try:
            while True:
                url, max_redirect = await self.q.get()
                print('work {}'.format(self.q))
                if url.endswith('html'):
                    await self.fetch_by_next(url)  # 这里逻辑需要改
                else:
                    await self.download_img(url)
                self.q.task_done()
                # logger.debug('done with {}'.format(url))

                self.bfcon.insert(url, 'bf_done_urls')
                self.rcon.srem('buff_urls', url)
                self.rcon.lpush('list_done_urls', url)

        except asyncio.CancelledError:
            pass

    async def my_request(self, url):  # 要把异常往上抛，或者减少嵌套层数
        exception = None
        tries = 0
        asyncio.sleep(0.5)  # 延时设置

        while tries < self.max_tries:  # 尝试连接
            try:
                async with self.session.get(url, allow_redirects=False, headers=HEADERS, timeout=5) as page_response:
                    page_body = await page_response.read()
                logger.debug('body {}'.format(url))
                break
            except aiohttp.ClientError as client_error:  # 捕捉异常
                exception = client_error
            except asyncio.TimeoutError:  # 捕捉超时
                exception = 'timeout_error in request {}'.format(url)
            tries += 1
        else:
            logger.info('{} is out try, because {}.'.format(url, exception))
            return None
        return page_body

    async def fetch(self, url):  # 将请求这个步骤封装起来,构造url，获取章节名，图片url
        page_body = await self.my_request(url)
        if page_body:
            page_body = etree.HTML(page_body)
            img_url = page_body.xpath('//div[@id="pictureContent"]/p/img/@src')[0]
            folder_name = re.findall(r'_\d+_\d+', img_url)[0].split('_')[1]
            folder_name = os.path.join(STROEPATH, folder_name)
            if not os.path.exists(folder_name):  # 如果不存目标文件夹，就创建文件夹，并且构造url
                os.makedirs(folder_name)  # 多层目录的创建
                items = page_body.xpath('//div[@class="mhTit"]/h3/code/text()')[0]
                items = re.findall(r'\d+', items)[-1]  # 找总页数，然后构造url
                for item in range(1, int(items)):  # 注意页数的构造。要从1开始，和要少1
                    self.add_url(img_url[:-7] + str(item).rjust(3, '0') + img_url[-4:])  # add_url
            self.add_url(img_url)
        else:
            print('wrong in {}'.format(url))
            return

    async def fetch_by_next(self, url):  # 将请求这个步骤封装起来,构造url，获取章节名，图片url
        page_body = await self.my_request(url)
        if page_body:
            page_body = etree.HTML(page_body)

            folder_name = page_body.xpath('//div[@class="mhTit"]/h3/text()')[0]
            folder_name = re.findall(r'\d+', folder_name)[0]
            folder_name = os.path.join(STROEPATH, folder_name)
            if not os.path.exists(folder_name):  # 如果不存目标文件夹，就创建文件夹，并且构造url
                os.makedirs(folder_name)  # 多层目录的创建
            img_url = page_body.xpath('//div[@id="pictureContent"]/p/img/@src')[0]
            if '_' in url:
                number = url.split('_')[-1].split('.')[0]
            else:
                number = '1'
            filename = number + '.' + img_url.split('.')[-1]
            filename = os.path.join(folder_name, filename)
            await self.download_img(img_url, filename)
            try:
                next_url = page_body.xpath('//li[@id="page__next"]/a/@href')[0]  # 这里是有序号异常的，但是ide不抛出
                self.add_url(next_url)
            except IndexError:
                pass
        else:
            print('wrong in {}'.format(url))
            return

    async def download_img(self, img_url, filename=None):  # 只做下载处理
        if filename is None:  # 重新命名
            folder_name = re.findall(r'_\d+_\d+', img_url)[0].split('_')[1]
            folder_name = os.path.join(STROEPATH, folder_name)
            filename = img_url.split('/')[-1].split('_')[-1]
            filename = os.path.join(folder_name, filename)

        img_response = await self.my_request(img_url)  # 只有session.get才能用with，response不是上下文管理
        if img_response:
            with open(filename, 'wb') as f:
                f.write(img_response)
            print('download {}'.format(img_url))
        else:
            print('wrong in {}'.format(img_url))
            return

    def close(self):
        self.session.close()


if __name__ == '__main__':
    import redis
    import codecs
    import csv

    r = redis.StrictRedis(db=1)
    Flag = True

    # with codecs.open('op_all_urls.txt', 'r', encoding='utf-8') as f:
    #     rows = csv.reader(f)
    #     for row in rows:
    #         r.lpush('all_urls', row[0])

    loop = asyncio.get_event_loop()
    while Flag:
        us = []
        starttime = time.time()
        for _ in range(5):
            u = r.lpop('all_urls')
            if not u:
                Flag = False
                break
            if isinstance(u, bytes):
                u = str(u, encoding='utf-8')
            if u:
                us.append(u)
        us.append('http://www.hanhande.com/manhua/op/26103.shtml')
        print('uncomplete:{}'.format(r.llen('all_urls')))
        print('start:{}'.format(us))
        crawler = OpCrawler(urls=us, max_tasks=20, max_tries=3, redis_db=1)
        loop.run_until_complete(crawler.crawl())
        crawler.close()
        print('complete')
        endtime = time.time()
        print('cost:{}'.format(round(endtime - starttime, 3)))
        print('-' * 20)

    loop.close()

