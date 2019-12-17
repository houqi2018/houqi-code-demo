# Highlight watched films by comparing csv with old file
import os
import csv
import xlwt
import xlrd

# csv_name = input('Enter csv name including .csv:\n')
csv_name = 'TSPDT_1000_films_2019.csv'  #debug
if os.path.isfile(csv_name) == False:
    print('The file is not detected in current directory. Bye bye.')
    exit()
# old_file = input('Enter old file name including .xls\n')
old_file = 'oldfile.xls'  #debug
if os.path.isfile(old_file) == False:
    print('The file is not detected in current directory. Bye bye.')
    exit()

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
            bgx = xf.background.pattern_colour_index
            saveeee[row][col] = (thecell.value, bgx)

# Method used to check if a film is watched before or not
def highlight_in_saveeee_yellow(value):
    for row_index in range(len(saveeee)):
        for col_index in range(len(saveeee[row_index])):
            if '（' in str(saveeee[row_index][col_index][0]):
                idx = str(saveeee[row_index][col_index][0]).index('（')
                prep = saveeee[row_index][col_index][0][:idx]
                if prep == value and saveeee[row_index][col_index][1] == 13:
                    return True
            elif '(' in str(saveeee[row_index][col_index][0]):
                idx = str(saveeee[row_index][col_index][0]).index('(')
                prep = saveeee[row_index][col_index][0][:idx]
                if prep == value and saveeee[row_index][col_index][1] == 13:
                    return True

# Method used to check if a film is watched before or not
def highlight_in_saveeee_green(value):
    for row_index in range(len(saveeee)):
        for col_index in range(len(saveeee[row_index])):
            if '（' in str(saveeee[row_index][col_index][0]):
                idx = str(saveeee[row_index][col_index][0]).index('（')
                prep = saveeee[row_index][col_index][0][:idx]
                if prep == value and saveeee[row_index][col_index][1] != 13 and saveeee[row_index][col_index][1] != 64:
                    return True
            elif '(' in str(saveeee[row_index][col_index][0]):
                idx = str(saveeee[row_index][col_index][0]).index('(')
                prep = saveeee[row_index][col_index][0][:idx]
                if prep == value and saveeee[row_index][col_index][1] == 13 and saveeee[row_index][col_index][1] != 64:
                    return True

csv_file = open(csv_name, 'r')
csv_reader = csv.reader(csv_file, delimiter=',')
book = xlwt.Workbook()
sheet1 = book.add_sheet('Sheet 1')
yellow = xlwt.easyxf('pattern: pattern solid;')
yellow.pattern.pattern_fore_colour = 13  # 13-yellow color
white = xlwt.easyxf('pattern: pattern solid;')
white.pattern.pattern_fore_colour = 1  # 64-white color
green = xlwt.easyxf('pattern: pattern solid, fore_colour green;')
# green.pattern.pattern_fore_colour = 2

i = 0
for row in csv_reader:
    i = i + 1
    for j in range(len(row)):
        if row[j] == '':
            continue
        # Highlight film already watched if exists
        if '（' in row[j]:
            if highlight_in_saveeee_yellow(row[j][:row[j].index('（')]) == True:
                sheet1.write(i, j, row[j], yellow)
            elif highlight_in_saveeee_green(row[j][:row[j].index('（')]) == True:
                sheet1.write(i, j, row[j], green)
            else:
                sheet1.write(i, j, row[j], white)
        elif '(' in row[j]:
            if highlight_in_saveeee_yellow(row[j][:row[j].index('(')]) == True:
                sheet1.write(i, j, row[j], yellow)
            elif highlight_in_saveeee_green(row[j][:row[j].index('(')]) == True:
                sheet1.write(i, j, row[j], green)
            else:
                sheet1.write(i, j, row[j], white)
        else:
            sheet1.write(i, j, row[j], white)
new_name = csv_name[:-4] + '.xls'
book.save(new_name)
print('Comparison finished. New file:', new_name)