# TSPDT
TSPDT for Jackie  
### Functions:
1. Download 1000-film-list from TSPDT  
2. Translate English title to corresponding Chinese title via json and Douban
3. Compare new csv with old xls, highlight watched films

## Files
### Main files:
1. main.py --> Just run it, do function 1 and 2 above  
2. highlight-watched-films.py --> Optional, do function 3 above  
   Notice this file supports 2 colors: yellow and green. It may take about 1.5 minutes to run.
### Helper files:
*  create_json.py --> Generate json file if not exists  
*  csv-to-xls.py  --> Convert csv to plain xls  
*  csv-to-xlsx.py  --> Convert csv to plain xlsx  
### Example generated files:
*  TSPDT_1000_films_2019.csv (result of main.py)  
*  TSPDT_1000_films_2019.xls (result of highlight-watched-films.py, **with highlights**)  
*  data.json  (result of create_json.py)  
*  TSPDT_1000_films_2019.xls (result of csv-to-xls.py, **without highlights**)  
*  TSPDT_1000_films_2019.xlsx (result of csv-to-xlsx.py, **without highlights**)  

## Dependency
requests, beautifulsoup, selenium,csv, xlwt, xlrd
