# csv to xls
import os
import csv
import glob
import xlwt

csv_name = input('Enter csv name including .csv:\n')
if os.path.isfile(csv_name) == False:
    print('The file is not detected in current directory. Bye bye.')
    exit()
for csvfile in glob.glob(os.path.join('.', csv_name)):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('data')
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, val in enumerate(row):
                ws.write(r, c, val)
    wb.save(csvfile[:-4] + '.xls')
print('Success')