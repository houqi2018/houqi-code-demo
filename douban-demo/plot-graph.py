import matplotlib.pyplot as plt

aa = open('result.txt', 'r')
bb = aa.readlines()
N = len(bb)
x = []
y = []
colors = 'blue'
rr1, rr2, rr3, rr4, rr5, rr6, rr7, rr8 = 0,0,0,0,0,0,0,0

sum_y = 0
half_count = 0
first_half_sum_y = 0
second_half_sum_y = 0

for ea in bb:
    half_count = half_count + 1
    ea = ea.split()
    x.append(int(ea[2]))
    temp = float(ea[3])*100
    y.append(temp)
    sum_y = sum_y + float(ea[3])
    if half_count < (0.5*len(bb)):
        first_half_sum_y = first_half_sum_y + float(ea[3])
    else:
        second_half_sum_y = second_half_sum_y + float(ea[3])

    if 0 <= temp and temp < 5:
        rr1 = rr1 + 1
    elif 5 <= temp and temp < 10:
        rr2 = rr2 + 1
    elif 10 <= temp and temp < 15:
        rr3 = rr3 + 1
    elif 15 <= temp and temp < 20:
        rr4 = rr4 + 1
    elif 20 <= temp and temp < 25:
        rr5 = rr5 + 1
    elif 25 <= temp and temp < 30:
        rr6 = rr6 + 1
    elif 30 <= temp and temp < 35:
        rr7 = rr7 + 1
    elif 35 <= temp and temp < 40:
        rr8 = rr8 + 1
# Avg
temp_num = round(len(bb)/2)
first_half_print = 'first half average  (001' + '-' + str(temp_num) + '):'
second_half_print = 'second half average (' + str(temp_num+1) + '-' + str(len(bb)) + '):'
print('----------------- Stat -----------------')
print(first_half_print, str(round((first_half_sum_y/(0.5*len(bb))), 3)*100)[0:4], '%')
print(second_half_print, str(round((second_half_sum_y/(0.5*len(bb))), 3)*100)[0:4], '%')
print('average:', round((sum_y/len(bb)), 3)*100, '%')
print('total:  ', len(bb))

# Plot
plt.scatter(x, y, c=colors, alpha=0.5)
plt.title('Douban Rating')
plt.xlabel('Number of Films Watched')
plt.ylabel('5 Star Percentage')
plt.show()

# Bar Chart
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

range = ('0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40')
y_pos = np.arange(len(range))
rr_total = rr1 + rr2 + rr3 + rr4 + rr5 + rr6 + rr7 + rr8
rr1 = 100 * rr1/rr_total
rr2 = 100 * rr2/rr_total
rr3 = 100 * rr3/rr_total
rr4 = 100 * rr4/rr_total
rr5 = 100 * rr5/rr_total
rr6 = 100 * rr6/rr_total
rr7 = 100 * rr7/rr_total
rr8 = 100 * rr8/rr_total
performance = [rr1, rr2, rr3, rr4, rr5, rr6, rr7, rr8]

plt.bar(y_pos, performance, align='center', color=colors, alpha=0.5)
plt.xticks(y_pos, range)
plt.xlabel('Range')
plt.ylabel('Percentage')
plt.title('Douban Rating')
plt.show()