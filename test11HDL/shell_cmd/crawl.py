# -*- coding:utf-8 -*-

import datetime
import time
import requests
from lxml import etree
from selenium import webdriver
import logging


def phantomjs_selenium_crawl(url):
    browser = webdriver.PhantomJS(executable_path=r'phantomjs.exe')
    browser.get(url)
    time.sleep(5)

    m_name = etree.XPath('//div[@class="futures-title"]/h1/text()')
    m_price = etree.XPath('//div[@id="box-futures-hq-wrap"]//tbody/tr/td/div/span/text()')
    # m_time = etree.XPath('//div[@id="box-futures-hq-wrap"]//tbody/tr/td/p/text()')
    m_range = etree.XPath('//div[@id="box-futures-hq-wrap"]//tbody/tr/td/div//p/span/text()')
    # html = browser.execute_script('return document.documentElement.outerHTML')
    html = browser.page_source
    doc = etree.HTML(html)
    m_list = [m_name, m_price, m_range]
    result_list = []
    for m in m_list:
        result = m(doc)
        result_list.append(result[0])
    return result_list


def transfrom(c):
    if '+' in c:
        c = '升' + c[1:]
    else:
        c = '降' + c[1:]
    return c


def main():

    urls = ['http://finance.sina.com.cn/futures/quotes/CL.shtml',
            'http://finance.sina.com.cn/futures/quotes/OIL.shtml']
    FLAG = True
    while FLAG:
        price_list = []
        for url in urls:
            r_list = phantomjs_selenium_crawl(url)
            price_list.append(r_list)
        if '-' in price_list[0][1]:
            time.sleep(60)
            continue
        FLAG = False
        today = datetime.datetime.now()
        msg = '{m}月{d}日，{h}时{mi}分，{n1}：{p1}({r1})；{n2}：{p2}({r2})。【关爱小提琴成长协会】' \
            .format(m=today.month, d=today.day, h=today.hour, mi=today.minute,
                    n1=price_list[0][0], p1=price_list[0][1], n2=price_list[1][0], p2=price_list[1][1],
                    r1=transfrom(price_list[0][2]), r2=transfrom(price_list[0][2]))
    # print(msg)
    send_url = 'https://imlaixin.cn/Api/send/data/json?accesskey=5619&secretkey=f409e0738cb556306245c09a88637b70388c604a&mobile=13226273649&content={}'.format(msg)
    response = requests.get(send_url)
    with open('record.txt', 'a') as f:
        f.write(msg+'\n')
    logging.debug(msg)
    logging.debug(response.text)

if __name__ == '__main__':
    main()