# -*- coding:utf-8 -*-

import requests
from lxml import etree
import codecs


HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0 '}
URL = 'http://www.xxbiquge.com/5_5422/'


def crwal(url):
    response = requests.get(url, headers=HEADER)
    body = etree.HTML(response.content)
    content_url = body.xpath('//div[@class="box_con"]/div/dl//dd/a/@href')[0]
    content_url = 'http://www.xxbiquge.com' + content_url

    content_response = requests.get(content_url, headers=HEADER)
    content_body = etree.HTML(content_response.content)
    chapter = content_body.xpath('//div[@class="bookname"]/h1/text()')[0]
    content = content_body.xpath('//div[@id="content"]')[0]
    # with codecs.open('text.txt', 'w', encoding='utf-8') as f:
    #     f.write(etree.tounicode(content).split('<div id="content">')[-1].split('</div>')[0])
    final_content = (etree.tounicode(content).split('<div id="content">')[-1].split('</div>')[0])
    return chapter, final_content

if __name__ == '__main__':
    # crwal(URL)
    # with codecs.open('test.html', 'r', encoding='utf-8') as f:
    #     body = etree.HTML(f.read())
    #     content = body.xpath('//div[@id="content"]')[0]
    #     print(type(content))
    #     print(etree.tounicode(content).split('<div id="content">')[-1].split('</div>')[0])
    import sqlite3


