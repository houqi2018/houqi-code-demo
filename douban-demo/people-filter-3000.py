# Only keep users who watch more than 3000 films
from string import digits
import requests
from bs4 import BeautifulSoup
import time
import random

lowerBound = 3000

aa = open('people-link-list.txt', 'rb')
urls = aa.readlines()
lst = []
cc = open('people-filter-3000.txt', 'wb')

for url in urls:
    url = url.rstrip()
    user_id = url[29:-1].decode('utf-8')
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    g_data = soup.find_all("div", {"id": "movie"})

    for item in g_data:
        try:
            user_name = item.contents[1].text.split()[0][:-3]
            user_collect = item.contents[1].find("span").contents[-2].text
            user_collect = ''.join(c for c in user_collect if c in digits)
            print(url.decode('ascii'), user_name, user_collect)
            lst.append((user_id, user_name, user_collect))
        except:
            print('error')
    time.sleep(random.randint(0,3))

lst = sorted(lst, key=lambda tup: int(tup[2]), reverse=True)
for ea in lst:
    if int(ea[2]) >= lowerBound:
        ea = ' '.join(list(ea)) + '\n'
        cc.write(ea.encode('utf-8'))