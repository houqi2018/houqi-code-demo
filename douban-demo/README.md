# Douban
豆瓣，计算在3000以上观影量影迷的5星比例
1. people-filter.py --> Parse input files
2. people-filter-3000.py --> Filter data, only keep users with views greater than 3000
3. people-ranking.py --> Main file, count ratio of 5 stars
4. plot-graph.py --> Plot two graphs showing the result

## Dependency
requests, beautifulsoup  
Notice it is possible ip address is blocked after too many requests.

## Result
First half average  (001-193): 8.7 %  
Second half average (194-386): 10.8 %  
Average: 9.8 %  
Total:   386  

![alt text](https://github.com/houqi2018/douban/blob/master/result1.png?raw=true)
![alt text](https://github.com/houqi2018/douban/blob/master/result2.png?raw=true)
