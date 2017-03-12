# -*- coding:utf-8 -*-

import logging
from logging import Logger
import asyncio


class MyLogger(Logger):
    def __init__(self, name='logger'):
        super(MyLogger, self).__init__(name)
        # self.setLevel = logging.DEBUG

        self.fh = logging.FileHandler(name if '.' in name else name+'.out')
        self.fh.setLevel(logging.DEBUG)

        self.fh_i = logging.FileHandler('info_'+name if '.' in name else name+'.out')
        self.fh_i.setLevel(logging.INFO)

        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)

        self.datefmt = '%Y-%m-%d %H:%M:%S'
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', self.datefmt)
        self.fh.setFormatter(self.formatter)
        self.ch.setFormatter(self.formatter)
        self.fh_i.setFormatter(self.formatter)

        self.addHandler(self.fh)
        self.addHandler(self.ch)
        self.addHandler(self.fh_i)

if __name__ == '__main__':
    # row = '2017-03-08 22:58:01 - mezitu3.0.out - INFO - http://www.mzitu.com/75821/22 is out try, because timeout_error.'
    # if 'INFO' in row:
    #     print(True)

    import time
    start = time.time()
    with open('mezitu3.0.out', 'r') as f:
        for row in f.readlines():
            if 'INFO' in row:
                print(row)
                # with open('beifen1.out', 'a') as bf:
                #     bf.write(row)

    end = time.time()
    print('cost:{}'.format(round(end-start, 2)))
    # import aiohttp
    # from lxml import etree
    #
    # logger = MyLogger('testlog')
    #
    # async def get_some_response(urls):
    #     session = aiohttp.ClientSession()
    #     for url in urls:
    #         logger.info('get {}'.format(url))
    #         async with session.get(url) as r:
    #             data = await r.text()
    #             body = etree.HTML(data)
    #             titles = body.xpath('//ul[@id="pins"]/li//span/a/text()')
    #             for title in titles:
    #                 logger.debug(title)
    #             r.release()
    #         logger.info('complete {}'.format(url))
    #     session.close()
    #
    # urls = ['http://www.mzitu.com/best', 'http://www.mzitu.com/', 'http://www.mzitu.com/page/2']
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(get_some_response(urls))
    # loop.close()

