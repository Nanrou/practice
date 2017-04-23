from crwal_novel import crwal
import re
import codecs

url = 'http://www.xxbiquge.com/5_5422/1068297.html'

c, t = crwal(url)
while True:
    if t.startswith(' '):
        break
    t = t[1:]


with codecs.open('testsplit.txt', 'w', encoding='utf-8') as nf:
    nf.write(t)


if __name__ == '__main__':
#     s = ' '
#     print(s.encode(), ' '.encode())
    s = '一次机会，紧紧地握着石头不\<br /><br />    2000<br /><br />    u80af放手，马上被'
    # s = re.search(r'\\[<br /> \w\s]*', s)
    print('\\'in s)