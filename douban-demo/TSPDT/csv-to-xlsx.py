import csv
import openpyxl
import os

wb = openpyxl.Workbook()
ws = wb.active

csv_name = input('Enter csv name including .csv:\n')
if os.path.isfile(csv_name) == False:
    print('The file is not detected in current directory. Bye bye.')
    exit()
with open(csv_name) as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        ws.append(row)

wb.save(csv_name[:-4] + '.xlsx')
print('Success')