# TSPDT 1000 movies (yearly)
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import datetime
import json

# TODO: Need to set environment path to where chromedriver.exe exists
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Python36\Scripts';
csv_name = 'TSPDT_1000_films_' + datetime.datetime.now().strftime("%Y") + '.csv'
csv_file = open(csv_name, mode='w+', newline='')
csv_writer = csv.writer(csv_file, delimiter=',')
if os.path.isfile('data.json') == False:
    print('data.json is not detected in current directory. Try again.')
    print('If you do not know where the json file is, run create_json.py to create a json file')
    exit()
json_file = open('data.json', 'r')  # json file stores (English, Chinese) of last year
json_data = json.load(json_file)
new_json_data = {}


# Get data from TSPDT
r = requests.get('http://www.theyshootpictures.com/gf1000_all1000films_table.php')
soup = BeautifulSoup(r.content, 'lxml')
movie_titles_temp = soup.find_all("td", {"class": "csv_column_3"})
movie_years_temp = soup.find_all("td", {"class": "csv_column_5"})
movie_ranking_temp = soup.find_all("td", {"class": "csv_column_1"})
movie_titles, movie_years, movie_ranking = [], [], []
for i in range(1000):
    movie_titles.append(movie_titles_temp[i].text)
    movie_years.append(int(movie_years_temp[i].text))
    movie_ranking.append(movie_ranking_temp[i].text)
print('Successfully got data from TSPDT')

# Search on Douban
browser = webdriver.Chrome()
result_to_csv = [ [] for _ in range(300) ]  # Assume 300 years (1800-2100)
json_search_count = 0
douban_search_count = 0
for i in range(1000):
    # If we already know Chinese title, skip Douban search
    if movie_titles[i] in json_data:
        entry = json_data[movie_titles[i]] + '(' + movie_ranking[i] + ')'
        json_search_count = json_search_count + 1
        result_to_csv[movie_years[i] - 1801].append(entry)
        continue
    browser.get('https://movie.douban.com/subject_search')
    search_text = browser.find_element_by_name('search_text')
    search_text.send_keys(movie_titles[i])
    search_text.submit()
    soup = BeautifulSoup(browser.page_source, 'lxml')
    search_result = soup.find_all("div", {"class": "title"})
    for item in search_result:
        result_lst = str(item.text).split()
        chinese_title = result_lst[0]
        year = ''
        for ea in result_lst:
            if '(' in ea and ')' in ea and result_lst.index(ea) > 1:  # Douban use English parens
                year = int(ea[ea.index('(')+1:ea.index(')')])
        if year == movie_years[i]:  # Assuming only one year will match in Douban
            entry = chinese_title + '(' + movie_ranking[i] + ')'
            douban_search_count = douban_search_count + 1
            result_to_csv[year-1801].append(entry)
            json_data[movie_titles[i]] = chinese_title
browser.close()

# Store new films to json file, easier for the next time
json_file.close()
os.remove('data.json')
with open('data.json', 'w') as f:
    json.dump(json_data, f, indent=4)

print('Successfully translated titles to Chinese via Douban')
print('Successfully searched in json:',json_search_count)
print('Successfully searched in Douban:', douban_search_count)

# Write data to csv
for eachYear in result_to_csv:
    if len(eachYear) == 0:
        csv_writer.writerow([0])
    else:
        write_list = [len(eachYear)]
        for xa in eachYear:
            write_list.append(xa)
        csv_writer.writerow(write_list)
print('Successfully saved to file:', csv_name)