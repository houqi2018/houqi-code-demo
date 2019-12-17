# Create a dictionary (English title, Chinese title) to avoid too many searches on Douban
import os
import csv
import xlwt
import xlrd
import requests
from bs4 import BeautifulSoup
import json

old_file = 'oldfile.xls'
old_file = input('Enter old xls file name including .xls:\n')
if os.path.isfile(old_file) == False:
    print('The file is not detected in current directory. Try again.')
    exit()
my_dict = {}

# Get English title from TSPDT
r = requests.get('http://www.theyshootpictures.com/gf1000_all1000films_table.php')
soup = BeautifulSoup(r.content, 'lxml')
movie_titles_temp = soup.find_all("td", {"class": "csv_column_3"})
movie_ranking_temp = soup.find_all("td", {"class": "csv_column_1"})
movie_titles, movie_years, movie_ranking = [], [], []
for i in range(1000):
    movie_titles.append(movie_titles_temp[i].text)
    movie_ranking.append(movie_ranking_temp[i].text)
print('Successfully got data from TSPDT')

# Get Chinese title from oldfile
saveeee = [[('', 64)] * 200 for _ in range(300)]
book = xlrd.open_workbook(old_file, formatting_info=True)
sheets = book.sheet_names()
for index, sh in enumerate(sheets):
    sheet = book.sheet_by_index(index)
    rows, cols = sheet.nrows, sheet.ncols
    for row in range(rows):
        for col in range(cols):
            # print("row", row+1, "col", col+1,)
            thecell = sheet.cell(row, col)
            # print(thecell.value)
            xfx = sheet.cell_xf_index(row, col)
            xf = book.xf_list[xfx]
            # If it is a film
            if '（' in str(thecell.value) and '）' in str(thecell.value):
                title_ranking = thecell.value
                idx_left_paren = str(thecell.value).index('（')
                title = title_ranking[0:idx_left_paren]
                ranking = title_ranking[idx_left_paren + 1:len(title_ranking) - 1]
                for i in range(1000):
                    if movie_ranking[i] == ranking:
                        my_dict[movie_titles[i]] = title
                        # print(my_dict)
            elif '(' in str(thecell.value) and ')' in str(thecell.value):
                title_ranking = thecell.value
                idx_left_paren = str(thecell.value).index('(')
                title = title_ranking[0:idx_left_paren]
                ranking = title_ranking[idx_left_paren+1:len(title_ranking)-1]
                for i in range(1000):
                    if movie_ranking[i] == ranking:
                        my_dict[movie_titles[i]] = title
                        # print(my_dict)

# Save to json file
with open('data.json', 'w') as outfile:
    json.dump(my_dict, outfile)
print('Successfully saved to json file')