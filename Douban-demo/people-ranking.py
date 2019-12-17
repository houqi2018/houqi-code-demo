# Get 5-star percentage in ranking of each user
# Assuming users are ordered by number of films watched
import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import datetime

aa = open('people-filter-3000.txt', 'rb')
cc = open('people-ranking.txt', 'ab')
csv_file = open('result.csv', mode='a+', newline='')
csv_writer = csv.writer(csv_file, delimiter=',')
csv_writer.writerow(['UID', '5 Star', 'Total', 'Percentage'])
person_count = 0

for eachLine in aa.readlines():
    person_count = person_count + 1
    if len(eachLine.split()) != 3:
        print('error at line ', person_count)
        continue
    user_id = eachLine.split()[0].decode('utf-8')
    user_watch = eachLine.split()[2].decode('utf-8')
    star_5 = 0
    url_first_page = "https://movie.douban.com/people/" + str(user_id) \
                     + "/collect?start=0&sort=rating&rating=all&filter=all&mode=list"
    # Visit first page to see how many pages in total
    r = requests.get(url_first_page)
    soup = BeautifulSoup(r.content, 'lxml')
    paginator = soup.find("div", {"class": "paginator"})
    if paginator == None:
        print('ip blocked')
        exit()
    pages_num = int(soup.find("div", {"class": "paginator"}).contents[-4].text)
    url_general_start = "https://movie.douban.com/people/" + str(user_id) + "/collect?start="
    url_general_end = "&sort=rating&rating=all&filter=all&mode=list"
    urls = [url_first_page]

    for i in range(30, pages_num*30, 30):  # Note since we use mode=list, 30 items every page
        urls.append(url_general_start + str(i) + url_general_end)
    try:
        for eachUrl in urls:  # For every user
            r = requests.get(eachUrl)
            time.sleep(random.randint(0, 3))
            soup = BeautifulSoup(r.content, 'lxml')
            g_data = soup.find("div", {"class": "article"})
            g_lst = g_data.contents[-6].find_all("div", {"class": "date"})
            # The next line may through an arrayOutOfBound exception due to no rating
            ranking = int(g_lst[len(g_lst)-1].contents[1].attrs["class"][0][6:7])  # Get ranking of the last one of this page
            if ranking == 5:
                star_5 = star_5 + len(g_lst)  # The case that all titles on this page are 5 star
            else:
                # Traverse all titles in this page, and find num of 5 stars in this page
                page_data = soup.find_all("div", {"class": "item-show"})
                for item in page_data:
                    ranking = item.contents[3].find("span")
                    if ranking != None:  # It is possible that some films have no ranking
                        name = item.contents[1].find("a").text.strip()
                        ranking = int(ranking.attrs["class"][0][6:7])
                        if ranking == 5:
                            star_5 = star_5 + 1
                        else:
                            break
                break
    except:
        print('some error: the user may have no rating ', person_count)
        continue

    star_5_percent = round(star_5/int(user_watch), 3)
    ttime = datetime.datetime.now().strftime("%H:%M:%S")
    print(user_id, star_5, user_watch, star_5_percent, ttime, person_count)
    draft = str(user_id) + ' ' + str(star_5) + ' ' + str(user_watch) + ' ' + str(star_5_percent) + '\n'
    cc.write(draft.encode('utf-8'))
    csv_writer.writerow([str(user_id), str(star_5), str(user_watch), str(star_5_percent)])
    time.sleep(random.randint(0,3))
