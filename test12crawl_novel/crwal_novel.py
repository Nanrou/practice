# -*- coding:utf-8 -*-

import requests
from lxml import etree
import codecs
from transfrom import del_extra


HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0 '}
URL = 'http://www.xxbiquge.com/5_5422/'


def crawl_urls(u):
    response = requests.get(u, headers=HEADER)
    body = etree.HTML(response.content)
    content_urls = body.xpath('//div[@class="box_con"]/div/dl//dd/a/@href')
    for pk_id, u in enumerate(content_urls):
        content_url = 'http://www.xxbiquge.com' + u
        yield pk_id, content_url


def crwal(content_url):
    content_response = requests.get(content_url, headers=HEADER)
    content_body = etree.HTML(content_response.content)
    try:
        chapter = content_body.xpath('//div[@class="bookname"]/h1/text()')[0]
        content = content_body.xpath('//div[@id="content"]')[0]
    except IndexError:
        raise IndexError('rules haved change in %s' % content_url)
    # with codecs.open('text.txt', 'w', encoding='utf-8') as f:
    #     f.write(etree.tounicode(content).split('<div id="content">')[-1].split('</div>')[0])
    final_content, need_confirm = transform_content(etree.tounicode(content))

    return chapter, final_content, need_confirm


def transform_content(txt):
    need_confirm = 0
    if 'div' in txt:
        txt = txt.split('<div id="content">')[-1].split('</div>')[0]
    while True:
        if txt.startswith(' '):
            break
        txt = txt[1:]
    txt = del_extra(txt)
    if '\\' in txt:
        need_confirm = 1
    return txt, need_confirm

if __name__ == '__main__':
    # crwal(URL)
    # with codecs.open('test.html', 'r', encoding='utf-8') as f:
    #     body = etree.HTML(f.read())
    #     content = body.xpath('//div[@id="content"]')[0]
    #     print(type(content))
    #     print(etree.tounicode(content).split('<div id="content">')[-1].split('</div>')[0])

    from orm import insert

    urls = crawl_urls(URL)
    i = 0
    for pk_id, url in urls:
        if pk_id < 10:
            continue
        c, t, n = crwal(url)
        insert(pk_id=str(pk_id), chapter=c, content=t, need_confirm=n)
        print('finish: {}'.format(url) + '\n')
        i += 1
        if i > 10:
            break


