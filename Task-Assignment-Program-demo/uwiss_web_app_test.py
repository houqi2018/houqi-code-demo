import os
from selenium import webdriver
from random import *
from time import sleep

# Log in
browser = webdriver.Chrome()
browser.get('http://127.0.0.1:8000')
emailElem = browser.find_element_by_name('username')
emailElem.send_keys('xxxx')
passwordElem = browser.find_element_by_name('password')
passwordElem.send_keys('xxxx')
passwordElem.submit()


taskName = ['Cap Gap', 'CoS from F-1/J-1', 'CoS to F/J',
            'CoL', 'CoM', 'Correction of Status', 'SEVIS Corr Request',
            'CPT', 'CPT Extension', 'Dependent', 'Financial', 'Letter',
            'LoA', 'New I-20', 'New DS-2019', 'OPT', 'Other', 'Program Extension',
            'RCL', 'Record Completion', 'Reprint I-20 DS-2019', 'Stem Extension',
            'J-1 Transfer In', 'J-1 Transfer Out', 'F-1 Transfer In', 'F-1 Transfer Out',
            'J-1 On-Campus Work Authorization', 'J-1 AT', 'Name Change'
            ]

'''
count = 0
# Test tasks one by one with random numbers
for eachTask in taskName:
    assignTime = randint(5, 10)
    count += 1
    print('Random time for No.' + str(count) + ' task is ' + str(assignTime))
    
    for i in range(0, assignTime):
        taskNameElem = browser.find_element_by_id('id_taskName')
        taskNameElem.send_keys(eachTask)
        taskNameElem.submit()
    browser.get('http://127.0.0.1:8000/summary/')
    sleep(5)
    browser.get('http://127.0.0.1:8000')
'''

# Test 2
count = 0
totalTestRun = 50
for i in range(0, totalTestRun):
    randomTask = taskName[randint(1, 28)]
    assignTime = randint(1, 3)
    count += 1

    for j in range(0, assignTime):
        taskNameElem = browser.find_element_by_id('id_taskName')
        taskNameElem.send_keys(randomTask)
        taskNameElem.submit()

browser.quit()