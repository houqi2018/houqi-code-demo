# For each user, get a link like this "http://www.douban.com/people/<id>/"
aa = open('people-list.txt', 'rb')
bb = aa.readlines()
cc = open('people-link-list.txt', 'w')
lst = []
counte_error = 0
line_num = 0
error_lines = []
for eachLine in bb:
    line_num = line_num + 1
    eachLine = eachLine.decode('utf-8')
    temp_arr = eachLine.split()
    length = len(temp_arr)
    if length == 4:
        lst.append(temp_arr[2])
    elif length == 3:
        lst.append(temp_arr[1])
    else:
        counte_error = counte_error + 1
        error_lines.append(line_num)
for ea in lst:
    if ea[0:12] == 'http://movie':
        ea = 'http://www' + ea[12:]
    print(ea)
    ea = ea + '\n'
    cc.write(ea)

if counte_error > 0:
    print("error number: " + str(counte_error))
    print(error_lines)