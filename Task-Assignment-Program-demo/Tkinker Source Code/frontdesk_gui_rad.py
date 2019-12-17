# Info class: advisor, count
class advisor:
    def __init__(self, name, count, switch, weight):
        self.name = name
        self.count = count
        self.switch = switch  # Vacation: ON/OFF
        self.weight = weight


class task:
    def __init__(self, name, num, requirement, weight, list=[]):
        self.t_task_name = name
        self.t_task_num = num
        self.t_task_requirement = requirement
        self.t_task_weight = weight
        self.t_task_advisor_list = list


from pathlib import Path
import os
import datetime
import _tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from tkinter import messagebox as tkMessageBox
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import random

# Initialize advisor list
advisorList = []
cc = open('config_advisorList.txt')
dd = cc.readlines()
for item in dd:
    advisorList.append( advisor(item.replace("\n", ""), 0, "ON", 0) )

# Initialize task list
taskList = []
l_list = []
aa = open('config_taskList.txt')
bb = aa.readlines()
for item in bb:
    spliter = item.split('.')
    for i in spliter[1].split(','):
        for adv in advisorList:
            if adv.name == i.strip():
                l_list.append(adv)
    taskList.append( task(spliter[0], 0, spliter[2].strip(), spliter[3].strip(), l_list) )
    l_list = []


# Initialize group list
group1 = []
group2 = []
group3 = []
group4 = []
groupList = []
tt = []  # Temp list
ee = open('config_groupList.txt')
ff = ee.readlines()
for item in ff:
    tt.append(item)
# Group 1
spliter1 = tt[0].split('.')
for eachAdvisor in spliter1:
    eachAdvisor = eachAdvisor.strip()
    for i in advisorList:
        if eachAdvisor == i.name:
            group1.append(i)
# Group 2
spliter2 = tt[1].split('.')
for eachAdvisor in spliter2:
    eachAdvisor = eachAdvisor.strip()
    for i in advisorList:
        if eachAdvisor == i.name:
            group2.append(i)
# Group 3
spliter3 = tt[2].split('.')
for eachAdvisor in spliter3:
    eachAdvisor = eachAdvisor.strip()
    for i in advisorList:
        if eachAdvisor == i.name:
            group3.append(i)

# Group 4
spliter4 = tt[3].split('.')
for eachAdvisor in spliter4:
    eachAdvisor = eachAdvisor.strip()
    for i in advisorList:
        if eachAdvisor == i.name:
            group4.append(i)

# Shuffle order of advisors in groups
random.shuffle(group1)
random.shuffle(group2)
random.shuffle(group3)
random.shuffle(group4)
groupList = [group1, group2, group3, group4]


# Count ratios, return a group
def getGroup():
    global count_group1
    count_group1 = 0
    global count_group2
    count_group2 = 0
    global count_group3
    count_group3 = 0

    for a in group1:
        count_group1 += a.weight
    for a in group2:
        count_group2 += a.weight
    for a in group3:
        count_group3 += a.weight


    print(count_group1)
    print(count_group2)
    print(count_group3)


    if count_group1 == 0:
        return group1
    elif count_group1 != 0 and count_group2 == 0:
        return group2
    elif count_group1 != 0 and count_group2 != 0 and count_group3 == 0:
        return group3
    else:
        # 80%:45%:20% is actually 4:2.25:1
        if count_group1 / count_group2 == (4 / 2.25):
            if count_group2 / count_group3 == 2.25:
                return group1
            elif count_group2 / count_group3 < 2.25:
                return group2
            elif count_group2 / count_group3 > 2.25:
                return group3
        elif count_group1 / count_group2 < (4 / 2.25):
            return group1
        elif count_group1 / count_group2 > (4 / 2.25):
            if count_group2 / count_group3 > 2.25:
                return group3
            else:
                return group2


# Handle multiple cases
# Return taskVariable
def caseHandler(taskName):
    global notFound
    notFound = True
    try:
        for a in taskList:
            if a.t_task_name == taskName:
                notFound = False
                return a
    except:
        messagebox.showerror(title="Error", message="Please handle this error manually. Error code 1")


# writeFile -- log_all
# writeFile2 -- log_(date)
# writeFile3 -- Frontdesk_Log_()
# writeFile3 -- log_crash
writeFile = open('log_all.txt', 'a+')

tempStr = "log_" + str(datetime.datetime.now().strftime("%Y_%m_%d")) + ".txt"
writeFile2 = open(tempStr, 'a+')

frontdeskLog = "Frontdesk_Log_" + str(datetime.datetime.now().strftime("%Y_%m_%d")) + ".txt"
writeFile3 = open(frontdeskLog, 'w')

writeFile_taskList = open('config_taskList.txt', 'w')
writeFile_advisorList = open('config_advisorList.txt', 'w')
writeFile_groupList = open('config_groupList.txt', 'w')

global group2JustHandle
group2JustHandle = False
global firstTaskAssigned
firstTaskAssigned = False

# Start here
class Feedback:

    def __init__(self, master):
        self.master = master
        master.geometry('495x460')
        #master.wm_iconbitmap('icon.ico')
        master.title('Frontdesk Helper')
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()

        self.frame_mid = ttk.Frame(master)
        self.frame_mid.pack()

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()
        font1 = font.Font(family='Arial', size=10, slant='italic')

        ll_taskList = []
        for a in taskList:
            ll_taskList.append(a.t_task_name)

        ll_advisorList = []
        for a in advisorList:
            ll_advisorList.append(a.name)

        ttk.Label(self.frame_header, text='Frontdesk  Helper', style='Header.TLabel').grid(row=0, column=2, padx=0, pady=5)

        ttk.Label(self.frame_header, text='', style='TLabel').grid(row=1, column=0)    # Line break


        # First task
        ttk.Label(self.frame_header, text='Select (first) task', font=font1, style='TLabel').grid(row=2, column=1, padx=0, pady=5, sticky='E')
        self.chooseTask = ttk.Combobox(self.frame_header, width=20)
        self.chooseTask['values'] = (ll_taskList)
        self.chooseTask.grid(row=2, column=2, padx=0, pady=5)
        ttk.Button(self.frame_header, text='Submit', command=self.tk_submit).grid(row=2, column=3, padx=0, pady=5)

        # Line segment
        ttk.Label(self.frame_header, text='-'*100, font=font1,
                  style='TLabel'). grid(row=3, column=1, columnspan=3, padx=0, pady=5)

        # Prompt to second task
        ttk.Label(self.frame_header, text='You can assign multiple tasks to the same advisor below', font=font1, style='TLabel').\
                                                                    grid(row=4, column=1, columnspan=3, padx=0,pady=5)

        # Second task
        ttk.Label(self.frame_header, text='Select second task', font=font1, style='TLabel').grid(row=5, column=1, padx=0, pady=5, sticky='E')
        self.chooseTask2 = ttk.Combobox(self.frame_header, width=20)
        self.chooseTask2['values'] = (ll_taskList)
        self.chooseTask2.grid(row=5, column=2, padx=0, pady=5)
        ttk.Button(self.frame_header, text='Submit', command=self.tk_secondTask).grid(row=5, column=3, padx=0, pady=5)

        # Third task
        ttk.Label(self.frame_header, text='Select third task', font=font1, style='TLabel').grid(row=6, column=1, padx=0, pady=5, sticky='E')
        self.chooseTask3 = ttk.Combobox(self.frame_header, width=20)
        self.chooseTask3['values'] = (ll_taskList)
        self.chooseTask3.grid(row=6, column=2, padx=0, pady=5)
        ttk.Button(self.frame_header, text='Submit', command=self.tk_thirdTask).grid(row=6, column=3, padx=0, pady=5)

        # Line segment
        ttk.Label(self.frame_header, text='-' * 100, font=font1,
                  style='TLabel').grid(row=7, column=1, columnspan=3, padx=0, pady=5)


        # Prompt to manually assignment
        ttk.Label(self.frame_header, text='You can manually assign task to advisor below', font=font1,
                             style='TLabel'). grid(row=8, column=1, columnspan=3, padx=0, pady=5)

        # Manually
        ttk.Label(self.frame_header, text='Select advisor', font=font1, style='TLabel').grid(row=9, column=1, padx=0, pady=5, sticky='E')
        ttk.Label(self.frame_header, text='Select task', font=font1, style='TLabel').grid(row=10, column=1, padx=0, pady=5, sticky='E')
        self.manually_advisor = ttk.Combobox(self.frame_header, width=20)
        self.manually_advisor['values'] = (ll_advisorList)
        self.manually_advisor.grid(row=9, column=2, padx=0, pady=5)
        self.manually_task = ttk.Combobox(self.frame_header, width=20)
        self.manually_task['values'] = (ll_taskList)
        self.manually_task.grid(row=10, column=2, padx=0, pady=5)
        ttk.Button(self.frame_header, text='Submit', command=self.tk_manually).grid(row=10, column=3, padx=0, pady=5)

        self.counter = IntVar()
        ttk.Label(self.frame_content, text='Files processed: ', font=font1, style='TLabel').grid(row=11, column=1, padx=0, pady=5)
        ttk.Label(self.frame_content, textvariable=self.counter, style='TLabel').grid(row=11, column=2, padx=0, pady=5)

        ttk.Label(self.frame_header, text='', style='TLabel').grid(row=12, column=0)    # Line break

        ttk.Button(self.frame_content, text='Log', command=self.tk_log).grid(row=13, column=1 , padx=10, pady=5)
        ttk.Button(self.frame_content, text='Options', command=self.tk_options).grid(row=13, column=2 , padx=10, pady=5)

        self.tk_detectLog()

        # log_all
        writeFile.write("-" * 32 + "\nLog\t" + str(datetime.datetime.now().strftime("%Y-%m-%d")) + "\n")

        # log_(date)
        writeFile2.write("-" * 32 + "\nLog today\t" + str(datetime.datetime.now().strftime("%Y-%m-%d")) + "\n")



    def tk_quit(self):
        # Quit confirmation
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?\n\n" +
                                            "Log will be saved and opened after you hit 'OK'."
                                            "\nYou can also open it manually. File name: " + tempStr
                                    ):
            try:
                print("Exited.")
                print("*" * 32 + "\n" + "Summary of today".center(32, ' ') + "\n" + "*" * 32)
                writeFile.write("\n" + str("*" * 32 + "\n" + "Summary of today".center(32, ' ') + "\n" + "*" * 32))
                writeFile2.write("\n" + str("*" * 32 + "\n" + "Summary of today".center(32, ' ') + "\n" + "*" * 32))

                # Print out advisors
                for a in advisorList:
                    print(str(a.name).ljust(24) + str(a.count) + " files")
                    writeFile.write("\n" + str(a.name).ljust(24, ".") + str(a.count))
                    writeFile2.write("\n" + str(a.name).ljust(24, ".") + str(a.count) + " files")
                print("*" * 32)
                writeFile.write("\n" + str("*" * 32 + "\n"))
                writeFile2.write("\n" + str("*" * 32) + "\n")

                # Print out tasks
                total = 0
                for t in taskList:
                    print(str(t.t_task_name).ljust(24) + str(t.t_task_num) + " tasks")
                    writeFile.write(str(t.t_task_name).replace(" ","").upper().ljust(24, ".") + str(t.t_task_num) + "\n")
                    writeFile2.write(str(t.t_task_name).replace(" ","").upper().ljust(24, ".") + str(t.t_task_num) + " tasks\n")
                    total += t.t_task_num
                print("*" * 32 + "\nTotal".ljust(25) + str(total) + " tasks\n" + "*" * 32 + "\n")
                writeFile.write("*" * 32 + "\nTotal".ljust(25, ".") + str(total) + "\n" + "*" * 32 + "\n\n\n")
                writeFile2.write("*" * 32 + "\nTotal".ljust(25, ".") + str(total) + " tasks\n" + "*" * 32 + "\n")
                writeFile.flush()
                os.fsync(writeFile.fileno())
                writeFile2.flush()
                os.fsync(writeFile2.fileno())
                self.updateInfo()
                writeFile3.close()
                if (Path(frontdeskLog).is_file()):
                    os.remove(frontdeskLog)
                os.startfile(tempStr)

            except:
                messagebox.showerror(title="Error", message="Fatal error. Error code 5")
            finally:
                sys.exit(0)


    def tk_submit(self):
        taskName = self.chooseTask.get()
        group = getGroup()
        personToAssign_name = []
        personToAssign_count = []
        index = 0
        stopSign = False
        global group2JustHandle
        global task2ToSameAdvisor
        global firstTaskAssigned

        try:
            tempTask = caseHandler(taskName)
            for person in group:
                if person in tempTask.t_task_advisor_list and person.switch == "ON":
                    personToAssign_name.append(person.name)
                    personToAssign_count.append(person.count)

            print(str(group[0].name))
            print()
            print(str(len(personToAssign_count)))
            print(str(len(personToAssign_name)))


            # Make sure to find a group to handle this task
            if len(personToAssign_name) == 0:
                index = groupList.index(group)
                group = groupList[(index+1)%3]
                # Go to second group if first group cannot do this task
                for person in group:
                    tempTask = caseHandler(taskName)
                    if person in tempTask.t_task_advisor_list and person.switch == "ON":
                        if taskName != "COM":
                            personToAssign_name.append(person.name)
                            personToAssign_count.append(person.count)
                        else:
                            if group2JustHandle == False:
                                personToAssign_name.append(person.name)
                                personToAssign_count.append(person.count)
                                group2JustHandle = True
                            else:
                                break

                # Go to group3 if group1 and group2 cannot do this task
                if len(personToAssign_name) == 0:
                    group = groupList[(index+2)%3]
                    # Go to third group if first and second cannot do this task
                    for person in group:
                        tempTask = caseHandler(taskName)
                        if person in tempTask.t_task_advisor_list and person.switch == "ON":
                            if taskName != "COM":
                                personToAssign_name.append(person.name)
                                personToAssign_count.append(person.count)
                            else:
                                if group2JustHandle == True:
                                    personToAssign_name.append(person.name)
                                    personToAssign_count.append(person.count)
                                    group2JustHandle = False

                    # Go to group4 if group1 and group2 and group3 cannot do this task
                    if len(personToAssign_name) == 0:
                        group = groupList[3]
                        # Go to fourth group if first and second and third cannot do this task
                        for person in group:
                            tempTask = caseHandler(taskName)
                            if person in tempTask.t_task_advisor_list and person.switch == "ON":
                                # Give the task to CM(group4)
                                personToAssign_name.append(person.name)
                                personToAssign_count.append(person.count)

                        if len(personToAssign_name) == 0:
                            messagebox.showerror(title="Error", message="No advisor can handle this task.\n")
                            stopSign = True
                            # If no advisor can handle this task, then stop here, happens when on vacation

            # Special case when task involved CM, add CM to list
            for specialAdv in caseHandler(taskName).t_task_advisor_list:
                if specialAdv.name == "CM":
                    personToAssign_name.append("CM")
                    personToAssign_count.append(specialAdv.count)
                    break

            print()
            print(str(len(personToAssign_count)))
            print(str(len(personToAssign_name)))

            if stopSign == False:

                min = personToAssign_count[0]
                idx = 0
                for i in personToAssign_count:
                    if i < min:
                        idx = personToAssign_count.index(i)

                for ea in advisorList:
                    if ea.name == str(personToAssign_name[idx]):
                        task2ToSameAdvisor = ea
                        break

                print("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                      + "\n" + str(taskName) + " is assigned to " + str(personToAssign_name[idx]))
                print(caseHandler(taskName).t_task_requirement)
                print()

                messagebox.showinfo(title="Assign to",
                                    message="\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                    + "\n" + str(taskName) + " is assigned to " + str(personToAssign_name[idx])
                                            + "\n" + str(caseHandler(taskName).t_task_requirement))

                # Log it in case program crashes
                writeFile.write("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                + "\n" + str(taskName) + " is assigned to " + str(personToAssign_name[idx]) + "\n")
                writeFile2.write("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                 + "\n" + str(taskName) + " is assigned to " + str(personToAssign_name[idx]) + "\n")
                writeFile.flush()
                os.fsync(writeFile.fileno())
                writeFile2.flush()
                os.fsync(writeFile2.fileno())

                for person in group:
                    if person.name == personToAssign_name[idx]:
                        person.count += 1
                        tempTask.t_task_num += 1
                        person.weight += int(tempTask.t_task_weight)
                        self.counter.set(self.counter.get() + 1)
                        self.chooseTask.set('')
                        firstTaskAssigned = True

                # Special case to increase counters for CM
                if personToAssign_name[idx] == "CM":
                    for tttt in caseHandler(taskName).t_task_advisor_list:
                        if tttt.name == "CM":
                            tttt.count += 1
                            tempTask.t_task_num += 1
                            tttt.weight += int(tempTask.t_task_weight)
                            self.counter.set(self.counter.get() + 1)
                            self.chooseTask.set('')
                            firstTaskAssigned = True



        except AttributeError:
            firstTaskAssigned = False
            print("Wrong input. Please try it again.\n")
            messagebox.showerror(title="Error",
                                message="Wrong input. Please try it again.\n")
        except Exception:
            firstTaskAssigned = False
            print("Something wrong. Handle manually.\n")
            # Save to log_crash
            writeFile4 = open('log_crash.txt', 'a')
            writeFile4.write("Program crashes!\n\n" + str(datetime.datetime.now().strftime("%Y-%m-%-d-%H-%M"))
                                 + "\n" + str("*" * 32 + "\n" + "Summary of today".center(32, ' ') + "\n" + "*" * 32))

            # Print out advisors
            for a in advisorList:
                writeFile4.write("\n" + str(a.name).ljust(24) + str(a.count) + " files")
                writeFile4.write("\n" + str("*" * 32) + "\n")

            # Print out tasks
            total = 0
            for t in taskList:
                writeFile4.write(str(t.t_task_name).ljust(24) + str(t.t_task_num) + " tasks\n")
                total += t.t_task_num
            writeFile4.write("*" * 32 + "\nTotal".ljust(25) + str(total) + " tasks\n" + "*" * 32 + "\n")
            writeFile4.flush()
            os.fsync(writeFile4.fileno())
            self.updateInfo()


    def tk_secondTask(self):
        try:
            taskName2 = self.chooseTask2.get()
            global canDOThisTask

            if firstTaskAssigned == True:
                # Check to see if this advisor can do this task
                for a in taskList:
                    if taskName2 == a.t_task_name:
                        if task2ToSameAdvisor in a.t_task_advisor_list:
                            canDOThisTask = True
                        else:
                            canDOThisTask = False

            if firstTaskAssigned == True and canDOThisTask == True:
                task2ToSameAdvisor.count += 1
                tempTask2 = caseHandler(taskName2)
                tempTask2.t_task_num += 1
                self.counter.set(self.counter.get() + 1)
                task2ToSameAdvisor.weight += int(tempTask2.t_task_weight)

                print("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                      + "\n" + str(taskName2) + " is also assigned to " + str(task2ToSameAdvisor.name))
                print(caseHandler(taskName2).t_task_requirement)
                print()

                messagebox.showinfo(title="Assign to",
                                    message="\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                            + "\n" + str(taskName2) + " is also assigned to " + str(task2ToSameAdvisor.name)
                                            + "\n" + str(caseHandler(taskName2).t_task_requirement))

                # Log it in case program crashes
                writeFile.write("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                + "\n" + str(taskName2) + " is also assigned to " + str(task2ToSameAdvisor.name) + "\n")
                writeFile2.write("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                 + "\n" + str(taskName2) + " is also assigned to " + str(task2ToSameAdvisor.name) + "\n")
                writeFile.flush()
                os.fsync(writeFile.fileno())
                writeFile2.flush()
                os.fsync(writeFile2.fileno())
                self.chooseTask2.set('')
            else:
                self.chooseTask2.set('')
                messagebox.showerror(title="Error", message="This advisor is not trained to handle this task, \n"
                                                            "or something else is wrong.\n")

        except AttributeError:
            print("Wrong input. Please try it again.\n")
            messagebox.showerror(title="Error",
                                message="Wrong input. Please try it again.\n")
        except Exception:
            print("Something wrong. Handle manually.\n")
            # Save to log_crash
            writeFile4 = open('log_crash.txt', 'a')
            writeFile4.write("Program crashes!\n\n" + str(datetime.datetime.now().strftime("%Y-%m-%-d-%H-%M"))
                                 + "\n" + str("*" * 32 + "\n" + "Summary of today".center(32, ' ') + "\n" + "*" * 32))

            # Print out advisors
            for a in advisorList:
                writeFile4.write("\n" + str(a.name).ljust(24) + str(a.count) + " files")
                writeFile4.write("\n" + str("*" * 32) + "\n")

            # Print out tasks
            total = 0
            for t in taskList:
                writeFile4.write(str(t.t_task_name).ljust(24) + str(t.t_task_num) + " tasks\n")
                total += t.t_task_num
            writeFile4.write("*" * 32 + "\nTotal".ljust(25) + str(total) + " tasks\n" + "*" * 32 + "\n")
            writeFile4.flush()
            os.fsync(writeFile4.fileno())
            self.updateInfo()


    def tk_thirdTask(self):
        try:
            taskName3 = self.chooseTask3.get()

            global canDOThisTask

            if firstTaskAssigned == True:
                # Check to see if this advisor can do this task
                for a in taskList:
                    if taskName3 == a.t_task_name:
                        if task2ToSameAdvisor in a.t_task_advisor_list:
                            canDOThisTask = True
                        else:
                            canDOThisTask = False

            if firstTaskAssigned == True and canDOThisTask == True:
                task2ToSameAdvisor.count += 1
                tempTask2 = caseHandler(taskName3)
                tempTask2.t_task_num += 1
                self.counter.set(self.counter.get() + 1)
                task2ToSameAdvisor.weight += int(tempTask2.t_task_weight)

                print("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                      + "\n" + str(taskName3) + " is also assigned to " + str(task2ToSameAdvisor.name))
                print(caseHandler(taskName3).t_task_requirement)
                print()

                messagebox.showinfo(title="Assign to",
                                    message="\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                            + "\n" + str(taskName3) + " is also assigned to " + str(task2ToSameAdvisor.name)
                                            + "\n" + str(caseHandler(taskName3).t_task_requirement))

                # Log it in case program crashes
                writeFile.write("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                + "\n" + str(taskName3) + " is also assigned to " + str(task2ToSameAdvisor.name) + "\n")
                writeFile2.write("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                 + "\n" + str(taskName3) + " is also assigned to " + str(task2ToSameAdvisor.name) + "\n")
                writeFile.flush()
                os.fsync(writeFile.fileno())
                writeFile2.flush()
                os.fsync(writeFile2.fileno())
                self.chooseTask3.set('')

            else:
                self.chooseTask3.set('')
                messagebox.showerror(title="Error", message="This advisor is not trained to handle this task, \n"
                                                            "or something else is wrong.\n")

        except AttributeError:
            print("Wrong input. Please try it again.\n")
            messagebox.showerror(title="Error",
                                message="Wrong input. Please try it again.\n")
        except Exception:
            print("Something wrong. Handle manually.\n")
            # Save to log_crash
            writeFile4 = open('log_crash.txt', 'a')
            writeFile4.write("Program crashes!\n\n" + str(datetime.datetime.now().strftime("%Y-%m-%-d-%H-%M"))
                                 + "\n" + str("*" * 32 + "\n" + "Summary of today".center(32, ' ') + "\n" + "*" * 32))

            # Print out advisors
            for a in advisorList:
                writeFile4.write("\n" + str(a.name).ljust(24) + str(a.count) + " files")
                writeFile4.write("\n" + str("*" * 32) + "\n")

            # Print out tasks
            total = 0
            for t in taskList:
                writeFile4.write(str(t.t_task_name).ljust(24) + str(t.t_task_num) + " tasks\n")
                total += t.t_task_num
            writeFile4.write("*" * 32 + "\nTotal".ljust(25) + str(total) + " tasks\n" + "*" * 32 + "\n")
            writeFile4.flush()
            os.fsync(writeFile4.fileno())
            self.updateInfo()


    # Manually assign one task to one specific advisor
    def tk_manually(self):
        try:
            manually_task = self.manually_task.get()
            manually_advisor = self.manually_advisor.get()

            global carryOn1
            global carryOn2

            # Check input: task and advisor selection
            if manually_task != "" and manually_advisor != "":
                carryOn1 = True
            else:
                carryOn1 = False

            for ea in advisorList:
                if ea.name == manually_advisor and ea.switch == "ON":
                    manually_advisor_obj = ea
                    carryOn2 = True
                    break

            if carryOn1 and carryOn2:
                # Increment counters
                manually_advisor_obj.count += 1
                manually_task_obj = caseHandler(manually_task)
                manually_task_obj.t_task_num += 1
                self.counter.set(self.counter.get() + 1)
                manually_advisor_obj.weight += int(manually_task_obj.t_task_weight)

                print("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                      + "\n" + str(manually_task_obj.t_task_name) + " is assigned to " + str(manually_advisor_obj.name))
                print(manually_task_obj.t_task_requirement)
                print()

                messagebox.showinfo(title="Assign to",
                                    message="\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                            + "\n" + str(manually_task_obj.t_task_name) + " is assigned to " + str(manually_advisor_obj.name)
                                            + "\n" + str(manually_task_obj.t_task_requirement))

                # Log it in case program crashes
                writeFile.write("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                + "\n" + str(manually_task_obj.t_task_name) + " is assigned to " + str(manually_advisor_obj.name) + "\n")
                writeFile2.write("\n" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                                 + "\n" + str(manually_task_obj.t_task_name) + " is assigned to " + str(manually_advisor_obj.name) + "\n")
                writeFile.flush()
                os.fsync(writeFile.fileno())
                writeFile2.flush()
                os.fsync(writeFile2.fileno())
                self.manually_task.set('')
                self.manually_advisor.set('')
            else:
                messagebox.showerror(title="Error", message="This advisor is not trained to handle this task,\nor input is not complete.\n")

        except AttributeError:
            print("Wrong input. Please try it again.\n")
            messagebox.showerror(title="Error",
                                message="Wrong input. Please try it again.\n")
        except Exception:
            print("Something wrong. Handle manually.\n")
            # Save to log_crash
            writeFile4 = open('log_crash.txt', 'a')
            writeFile4.write("Program crashes!\n\n" + str(datetime.datetime.now().strftime("%Y-%m-%-d-%H-%M"))
                                 + "\n" + str("*" * 32 + "\n" + "Summary of today".center(32, ' ') + "\n" + "*" * 32))
        
            # Print out advisors
            for a in advisorList:
                writeFile4.write("\n" + str(a.name).ljust(24) + str(a.count) + " files")
                writeFile4.write("\n" + str("*" * 32) + "\n")

            # Print out tasks
            total = 0
            for t in taskList:
                writeFile4.write(str(t.t_task_name).ljust(24) + str(t.t_task_num) + " tasks\n")
                total += t.t_task_num
            writeFile4.write("*" * 32 + "\nTotal".ljust(25) + str(total) + " tasks\n" + "*" * 32 + "\n")
            writeFile4.flush()
            os.fsync(writeFile4.fileno())
            self.updateInfo()



    def tk_log(self):
        s1 = "*" * 28 + "\n\tCurrent log\n" + "*" * 28 + "\n"
        for a in advisorList:
            if a.switch == "ON":
                s1 += str(a.name).ljust(30,'·') + str(a.count).rjust(3) + "\n"
        s1 += "*" * 28 + "\n"

        total = 0
        for t in taskList:
            s1 += str(t.t_task_name).ljust(30,'·') + str(t.t_task_num).center(3) + "\n"
            total += t.t_task_num
        s1 += "*" * 28 + "\nTotal".ljust(30,'.') + str(total).rjust(2) + "\n" + "*" * 28 + "\n"
        messagebox.showinfo(title="Current log", message=s1)


    def tk_options(self):
        self.newWindow = Toplevel(self.master)
        Feedback2(self.newWindow)


    def updateInfo(self):
        # Save each changes in option (except View availbility, Vacation) to local file
        # Vacation is a case that an advisor is temporarily ignored from task list during this runtime.
        # The advisor will be back in task list once the program is restarted. If you restart the program
        # at the same day you set an advisor to Vacation, please set the advisor to Vacation again.

        # Clear file in case user wants to email twice
        writeFile_taskList.seek(0)
        writeFile_taskList.truncate()
        writeFile_advisorList.seek(0)
        writeFile_advisorList.truncate()
        writeFile_groupList.seek(0)
        writeFile_groupList.truncate()

        for a in taskList:
            writeFile_taskList.write(str(a.t_task_name) + ". ")
            for b in a.t_task_advisor_list:
                writeFile_taskList.write(("%s, " % b.name))

            writeFile_taskList.write(". " + str(a.t_task_requirement))
            writeFile_taskList.write(". " + str(a.t_task_weight) + "\n")
        writeFile_taskList.flush()
        os.fsync(writeFile_taskList.fileno())

        for b in advisorList:
            writeFile_advisorList.write(str(b.name) + "\n")
        writeFile_advisorList.flush()
        os.fsync(writeFile_advisorList.fileno())

        for c in groupList:
            for d in c:
                writeFile_groupList.write(str(d.name) + ". ")
            writeFile_groupList.write("\n")
        writeFile_groupList.flush()
        os.fsync(writeFile_groupList.fileno())


    # Detect from log_(date) file to see if there is any log ealier today
    # If yes, ask user if they want to merge; if no, pass
    def tk_detectLog(self):
        # Only keep history of log for a month or so
        # writeFile -- log_all
        writeFile.seek(0, 0)

        if len(writeFile.readlines()) > 1200:
            # If log_all is too long, clear the file
            writeFile.seek(0)
            writeFile.truncate()

        # writeFile2 -- log_(date)
        try:
            global haveLog
            haveLog = False
            global haveRecord
            haveRecord = False

            writeFile2.seek(0, 0)
            lines = writeFile2.readlines()

            if len(lines) != 0:
                haveLog = True

            for i in range(0, len(lines)):
                line = lines[i]
                if line.replace("\n", "") == ("-" * 32):
                    global logDate
                    if (i+1) < len(lines):
                        ne = lines[i+1]
                        logDate = (ne.split("\t")[1]).replace("\n", "")
                        lineNumber = i+1
                        print(str(logDate))
                        if logDate == str(datetime.datetime.now().strftime("%Y-%m-%d")):
                            haveRecord = True
                            break

            if haveLog == True and haveRecord == True:

                if tkMessageBox.askyesno(title="Today's log detected", message="Do you want to continue "
                                           "assignment on ealier logs?\nLogs will be merged if you hit 'Yes'."):
                    for i in range(lineNumber, len(lines)):
                        line2 = lines[i]
                        if line2.replace("\n", "").replace("\t", "").strip() == "Summary of today":
                            # Add num of tasks advisor handled to each advisor.count
                            for j in range((i+2), (i+2+len(advisorList))):
                                ne2 = lines[j]
                                divider = ne2.split(".")
                                l_name = divider[0]
                                l_num = int(divider[len(divider)-1].split(" ")[0])
                                for l_adv in advisorList:
                                    if l_adv.name == l_name:
                                        l_adv.count += l_num

                            # Add num of tasks to each task
                            for h in range((i+3+len(advisorList)), (i+3+len(advisorList)+len(taskList))):
                                ne3 = lines[h]
                                divider2 = ne3.split(".")
                                t_name = divider2[0]
                                t_num = int(divider2[len(divider2)-1].split(" ")[0])
                                for t_task in taskList:
                                    if t_task.t_task_name.replace(" ","").upper() == t_name.replace("\n", "").strip():
                                        t_task.t_task_num += t_num
                writeFile2.seek(0)
                writeFile2.truncate()
        except:
            messagebox.showerror(title="Error", message="Please handle this error manually. Error code 2")



# Child window
class Feedback2():

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12, 'bold'))
        master.title('Options')
        master.geometry('595x520')
        #master.wm_iconbitmap('icon.ico')
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        font1 = font.Font(family='Arial', size=10, slant='italic')

        # Add advisor
        l_groupList = ['Group1', 'Group2', 'Group3']
        ttk.Label(self.frame_header, text='Enter advisor', font=font1, style='TLabel').grid(row=0, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Select group', font=font1, style='TLabel').grid(row=1, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Add advisor', style='TLabel').grid(row=0, column=0, sticky='E', padx=10, pady=5)
        self.addAdvisor = ttk.Entry(self.frame_header, width=20, font=('Arial', 10))
        self.addAdvisor.grid(row=0, column=2, padx=10, pady=5)
        self.addADvisor_group = ttk.Combobox(self.frame_header, width=20)
        self.addADvisor_group['values'] = (l_groupList)
        self.addADvisor_group.grid(row=1, column=2, padx=10, pady=5)
        ttk.Button(self.frame_header, text='Add', command=self.m_addAdvisor).grid(row=1, column=3, padx=10, pady=5)

        # Add task
        ttk.Label(self.frame_header, text='Enter task', font=font1, style='TLabel').grid(row=2, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Requirement', font=font1, style='TLabel').grid(row=3, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Select weight', font=font1, style='TLabel').grid(row=4, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Add task', style='TLabel').grid(row=2, column=0, sticky='E', padx=10, pady=5)
        self.addTask = ttk.Entry(self.frame_header, width=20, font=('Arial', 10))
        self.addTask.grid(row=2, column=2, padx=10, pady=5)
        self.addTask_requirement = ttk.Entry(self.frame_header, width=20, font=('Arial', 10))
        self.addTask_requirement.grid(row=3, column=2, padx=10, pady=5)
        self.addTask_weight = ttk.Combobox(self.frame_header, width=20)
        l_task_weightList = ['1', '2', '3']
        self.addTask_weight['values'] = (l_task_weightList)
        self.addTask_weight.grid(row=4, column=2, padx=10, pady=5)
        ttk.Button(self.frame_header, text='Add', command=self.m_addTask).grid(row=4, column=3, padx=10, pady=5)

        # Delete advisor
        l_advisorList = []
        for a in advisorList:
            l_advisorList.append(a.name)
        ttk.Label(self.frame_header, text='Select advisor', font=font1, style='TLabel').grid(row=5, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Delete advisor', style='TLabel').grid(row=5, column=0, sticky='E', padx=10, pady=5)
        self.deleteAdvisor = ttk.Combobox(self.frame_header, width=20)
        self.deleteAdvisor['values'] = (l_advisorList)
        self.deleteAdvisor.grid(row=5, column=2, padx=10, pady=5)
        ttk.Button(self.frame_header, text='Delete', command=self.m_deleteAdvisor).grid(row=5, column=3, padx=10, pady=5)

        # Delete task
        l_taskList = []
        for a in taskList:
            l_taskList.append(a.t_task_name)
        ttk.Label(self.frame_header, text='Select task', font=font1, style='TLabel').grid(row=6, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Delete task', style='TLabel').grid(row=6, column=0, sticky='E', padx=10, pady=5)
        self.deleteTask = ttk.Combobox(self.frame_header, width=20)
        self.deleteTask['values'] = (l_taskList)
        self.deleteTask.grid(row=6, column=2, padx=10, pady=5)
        ttk.Button(self.frame_header, text='Delete', command=self.m_deleteTask).grid(row=6, column=3, padx=10, pady=5)

        # Train advisor
        ttk.Label(self.frame_header, text='Select advisor', font=font1, style='TLabel').grid(row=7, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Select task', font=font1, style='TLabel').grid(row=8, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Train advisor', style='TLabel').grid(row=7, column=0, sticky='E', padx=10, pady=5)
        self.trainAdvisor = ttk.Combobox(self.frame_header, width=20)
        self.trainAdvisor['values'] = (l_advisorList)
        self.trainAdvisor.grid(row=7, column=2, padx=10, pady=5)
        self.trainAdvisor_task = ttk.Combobox(self.frame_header, width=20)
        self.trainAdvisor_task['values'] = (l_taskList)
        self.trainAdvisor_task.grid(row=8, column=2, padx=10, pady=5)
        ttk.Button(self.frame_header, text='Train', command=self.m_trainAdvisor).grid(row=8, column=3, padx=10, pady=5)

        # Untrain advisor
        ttk.Label(self.frame_header, text='Select advisor', font=font1, style='TLabel').grid(row=9, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Select task', font=font1, style='TLabel').grid(row=10, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Untrain advisor', style='TLabel').grid(row=9, column=0, sticky='E', padx=10, pady=5)
        self.untrainAdvisor = ttk.Combobox(self.frame_header, width=20)
        self.untrainAdvisor['values'] = (l_advisorList)
        self.untrainAdvisor.grid(row=9, column=2, padx=10, pady=5)
        self.untrainAdvisor_task = ttk.Combobox(self.frame_header, width=20)
        self.untrainAdvisor_task['values'] = (l_taskList)
        self.untrainAdvisor_task.grid(row=10, column=2, padx=10, pady=5)
        ttk.Button(self.frame_header, text='Untrain', command=self.m_untrainAdvisor).grid(row=10, column=3, padx=10, pady=5)

        # Vacation
        ttk.Label(self.frame_header, text='Select advisor', font=font1, style='TLabel').grid(row=11, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Vacation', style='TLabel').grid(row=11, column=0, sticky='E', padx=10, pady=5)
        self.vacationAdvisor = ttk.Combobox(self.frame_header, width=20)
        self.vacationAdvisor['values'] = (l_advisorList)
        self.vacationAdvisor.grid(row=11, column=2, padx=10, pady=5)
        ttk.Button(self.frame_header, text='Submit', command=self.m_vacation).grid(row=11, column=3, padx=10, pady=5)

        # Back to work
        ttk.Label(self.frame_header, text='Select advisor', font=font1, style='TLabel').grid(row=12, column=1, sticky='E', padx=10, pady=5)
        ttk.Label(self.frame_header, text='Back to Work', style='TLabel').grid(row=12, column=0, sticky='E', padx=10, pady=5)
        self.backToWork = ttk.Combobox(self.frame_header, width=20)
        self.backToWork['values'] = (l_advisorList)
        self.backToWork.grid(row=12, column=2, padx=10, pady=5)
        ttk.Button(self.frame_header, text='Submit', command=self.m_backToWork).grid(row=12, column=3, padx=10, pady=5)

        # Line break
        ttk.Label(self.frame_header, text='', style='TLabel').grid(row=13, column=0, padx=20, pady=0)

        # View availbility
        ttk.Button(self.frame_header, text='View availbility', command=self.m_viewAvil).grid(row=14, column=1, padx=10, pady=5)

        # Email log
        ttk.Button(self.frame_header, text='Email log', command=self.tk_email).grid(row=14, column=2, padx=10, pady=5)



    def tk_email(self):
        if tkMessageBox.askyesno("Email log", "Do you want to email log to ISS admin account (unknown@outlook.com)?\n\n" +
                                            "Email will be sent if you hit 'Yes'."
                                    ):
            # Clear file in case user wants to email twice
            writeFile3.seek(0)
            writeFile3.truncate()

            writeFile3.write("Frontdesk Log   " + str(datetime.datetime.now().strftime("%Y-%m-%d")) + "\n")
            writeFile3.write("\n" + str("*" * 32 + "\n" + "Summary of today".center(32, ' ') + "\n" + "*" * 32))

            # Print out advisors
            for a in advisorList:
                writeFile3.write("\n" + str(a.name).ljust(24, ".") + str(a.count) + " files")
            writeFile3.write("\n" + str("*" * 32) + "\n")

            # Print out tasks
            total = 0
            for t in taskList:
                writeFile3.write(str(t.t_task_name).ljust(24, ".") + str(t.t_task_num) + " tasks\n")
                total += t.t_task_num
            writeFile3.write("*" * 32 + "\nTotal".ljust(25, ".") + str(total) + " tasks\n" + "*" * 32 + "\n")
            writeFile3.flush()
            os.fsync(writeFile3.fileno())

            try:
                # Send email after file is ready
                msg = MIMEMultipart()
                msg['From'] = 'unknown@outlook.com'
                msg['To'] = 'unknown@outlook.com'
                msg['Subject'] = 'Frontdesk Log'
                body = "Attached is log of " + str(datetime.datetime.now().strftime("%Y-%m-%d"))

                msg.attach(MIMEText(body, 'plain'))
                attachment = open(frontdeskLog, "rb")
                part = MIMEBase('application' ,'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % frontdeskLog)
                msg.attach(part)

                smtpobj = smtplib.SMTP('smtp-mail.outlook.com', 587)
                smtpobj.starttls()
                smtpobj.login('unknown@outlook.com', 'xxxx')
                smtpobj.sendmail('unknown@outlook.com', 'unknown@outlook.com', msg.as_string())
                smtpobj.quit()

                # Close the log and remove it
                attachment.close()
                writeFile3.close()
                os.remove(frontdeskLog)
                messagebox.showinfo(title="Email sent",
                                    message="Email is sent successfully to ISS email account (unknown@outlook.com).")
            except:
                messagebox.showerror(title="Error", message="Fail to sent the email ")


    def m_addAdvisor(self):
        addDone = False
        temp = advisor(self.addAdvisor.get(), 0, "ON", 0)
        needToAdd = True
        if self.addAdvisor.get() == "":
            messagebox.showerror(title="Add advisor", message="Please specify advisor.")
        if self.addADvisor_group.get() == "":
            messagebox.showerror(title="Add advisor", message="Please specify group.")
        if self.addAdvisor.get() != "" and self.addADvisor_group.get() != "":
            try:
                for a in advisorList:
                    if a.name == self.addAdvisor.get():
                        needToAdd = False
                if needToAdd:
                    advisorList.append(temp)
                    if self.addADvisor_group.get().lower() == "group1":
                        group1.append(temp)
                    elif self.addADvisor_group.get().lower() == "group2":
                        group2.append(temp)
                    elif self.addADvisor_group.get().lower() == "group3":
                        group3.append(temp)

                    for a in advisorList:
                        if a.name == self.addAdvisor.get():
                            messagebox.showinfo(title="Add advisor", message="Successfully added " + self.addAdvisor.get() + "."
                                                                             + "\nPlease restart the program for this change to work.")
                            self.addAdvisor.delete(0, 'end')
                            self.addADvisor_group.set('')
                            addDone = True
                            self.updateInfo()
                            break
                if addDone == False:
                    messagebox.showinfo(title="Add advisor", message="Fail to add " + self.addAdvisor.get() + ", or no need to.")
            except:
                messagebox.showinfo(title="Add advisor", message="Fail to add the advisor")


    def m_addTask(self):
        addDone = False
        temp = task(self.addTask.get(), 0, self.addTask_requirement.get(), self.addTask_weight.get())
        needToAdd = True
        notInRange = True
        errorPrompt = True

        print(self.addTask_weight.get())
        try:
            # Check if weight is in range of 1-3
            if int(self.addTask_weight.get()) >=1 and int(self.addTask_weight.get()) <= 3:
                notInRange = False
        except:
            errorPrompt = False
            messagebox.showerror(title="Add task", message="Please specify task weight. Choose from 1, 2, 3.")

        if self.addTask.get() == "":
            messagebox.showerror(title="Add task", message="Please specify task.")
        if self.addTask_requirement.get() == "":
            messagebox.showerror(title="Add task", message="Please specify task requirement.")
        if errorPrompt:
            if self.addTask_weight.get() == "" or notInRange:
                messagebox.showerror(title="Add task", message="Please specify task weight. Choose from 1, 2, 3.")
        if self.addTask.get() != "" and self.addTask_requirement.get() != "" and self.addTask_weight.get() != "" and notInRange == False:
            try:
                for a in taskList:
                    if a.t_task_name == self.addTask.get():
                        needToAdd = False
                if needToAdd:
                    taskList.append(temp)
                    for b in taskList:
                        if b.t_task_name == self.addTask.get():
                            messagebox.showinfo(title="Add task", message="Successfully added " + self.addTask.get() + "."
                                                                          + "\nPlease restart the program for this change to work.")
                            self.addTask.delete(0, 'end')
                            self.addTask_requirement.delete(0, 'end')
                            self.addTask_weight.delete(0, 'end')
                            addDone = True
                            self.updateInfo()
                            break
                if addDone == False:
                    messagebox.showerror(title="Add task", message="Fail to add " + self.addTask.get() + ", or no need to.")
            except:
                messagebox.showerror(title="Add task", message="Fail to add the task")


    def m_deleteAdvisor(self):
        if self.deleteAdvisor.get() == "":
            messagebox.showerror(title="Delete advisor", message="Please specify advisor.")
        else:
            try:
                if tkMessageBox.askokcancel("Delete advisor", "Do you really want to delete " + self.deleteAdvisor.get() + "?"):
                    deleteDone = False
                    # First to delete from each group
                    for groups in groupList:
                        for advisors in groups:
                            if advisors.name == self.deleteAdvisor.get():
                                groups.remove(advisors)
                                break

                    nameOfAdvForThatTask = []
                    # delete from each task
                    for b in taskList:
                        for a in b.t_task_advisor_list:
                            nameOfAdvForThatTask.append(a.name)
                        if self.deleteAdvisor.get() in nameOfAdvForThatTask:
                            for eachAdv in advisorList:
                                if eachAdv.name == self.deleteAdvisor.get():
                                    b.t_task_advisor_list.remove(eachAdv)
                        nameOfAdvForThatTask = []

                    # Remove from advisorList
                    for a in advisorList:
                        if a.name == self.deleteAdvisor.get():
                            advisorList.remove(a)

                    deleteDone = True
                    messagebox.showinfo(title="Delete advisor",
                                        message="Successfully deleted " + self.deleteAdvisor.get() + "."
                                                + "\nPlease restart the program for this change to work.")
                    self.deleteAdvisor.set('')
                    self.updateInfo()
                    if deleteDone == False:
                        messagebox.showinfo(title="Delete advisor",
                                            message="Fail to delete " + self.deleteAdvisor.get() + ".")
            except:
                messagebox.showerror(title="Delete advisor",
                                    message="Fail to delete " + self.deleteAdvisor.get() + ".")


    def m_deleteTask(self):
        if self.deleteTask.get() == "":
            messagebox.showerror(title="Delete task", message="Please specify task.")
        else:
            deleteDone = False
            try:
                if tkMessageBox.askokcancel("Delete task", "Do you really want to delete " + self.deleteTask.get() + "?"):
                    for a in taskList:
                        if a.t_task_name == self.deleteTask.get():
                            taskList.remove(a)
                            messagebox.showinfo(title="Delete task",
                                                message="Successfully deleted " + self.deleteTask.get() + "."
                                                        + "\nPlease restart the program for this change to work.")
                            self.deleteTask.set('')
                            deleteDone = True
                            self.updateInfo()
                            break
                    if deleteDone == False:
                        messagebox.showinfo(title="Delete task",
                                        message="Fail to delete " + self.deleteTask.get() + ".")
            except:
                messagebox.showerror(title="Delete task",
                                    message="Fail to delete " + self.deleteTask.get() + ".")


    def m_trainAdvisor(self):
        trainDone = False
        nameOfAdvForThatTask = []
        if self.trainAdvisor.get() == "":
            messagebox.showerror(title="Train advisor", message="Please specify advisor.")
        if self.trainAdvisor_task.get() == "":
            messagebox.showerror(title="Train advisor", message="Please specify task.")
        if self.trainAdvisor.get() != "" and self.trainAdvisor_task.get() != "":
            try:
                for b in taskList:
                    if b.t_task_name == self.trainAdvisor_task.get():
                        for a in b.t_task_advisor_list:
                            nameOfAdvForThatTask.append(a.name)
                        if self.trainAdvisor.get() not in nameOfAdvForThatTask:
                            for adv in advisorList:
                                if adv.name == self.trainAdvisor.get():
                                    b.t_task_advisor_list.append(adv)
                                    messagebox.showinfo(title="Train advisor",
                                                        message="Successfuly trained " + self.trainAdvisor.get() + " with " + self.trainAdvisor_task.get() + "."
                                                                + "\nPlease restart the program for this change to work.")
                                    self.trainAdvisor.set('')
                                    self.trainAdvisor_task.set('')
                                    trainDone = True
                                    self.updateInfo()
                                    break
                if trainDone == False:
                    messagebox.showerror(title="Train advisor",
                                        message="Fail to train " + self.trainAdvisor.get() + " with " + self.trainAdvisor_task.get() + ", or no need to train.")
            except:
                messagebox.showerror(title="Train advisor", message="Fail to train the advisor.")


    def m_untrainAdvisor(self):
        untrainDone = False
        nameOfAdvForThatTask = []
        if self.untrainAdvisor.get() == "":
            messagebox.showerror(title="Train advisor", message="Please specify advisor.")
        if self.untrainAdvisor_task.get() == "":
            messagebox.showerror(title="Train advisor", message="Please specify task.")
        if self.untrainAdvisor.get() != "" and self.untrainAdvisor_task.get() != "":
            try:
                for b in taskList:
                    if b.t_task_name == self.untrainAdvisor_task.get():
                        for a in b.t_task_advisor_list:
                            nameOfAdvForThatTask.append(a.name)
                        if self.untrainAdvisor.get() in nameOfAdvForThatTask:
                            for adv in advisorList:
                                if adv.name == self.untrainAdvisor.get():
                                    b.t_task_advisor_list.remove(adv)
                                    messagebox.showinfo(title="Untrain advisor",
                                                        message="Successfuly untrained " + self.untrainAdvisor.get() + " with " + self.untrainAdvisor_task.get() + "."
                                                                + "\nPlease restart the program for this change to work.")
                                    self.untrainAdvisor.set('')
                                    self.untrainAdvisor_task.set('')
                                    untrainDone = True
                                    self.updateInfo()
                                    break
                if untrainDone == False:
                    messagebox.showerror(title="Untrain advisor",
                                        message="Fail to untrain " + self.untrainAdvisor.get() + " with " + self.untrainAdvisor_task.get() + ", or no need to untrain.")
            except:
                messagebox.showerror(title="Untrain advisor", message="Fail to untrain the advisor.")


    def m_vacation(self):
        if self.vacationAdvisor.get() == "":
            messagebox.showerror(title="Vacation", message="Please specify advisor.")
        else:
            try:
                messagebox.showinfo(title="Vacation", message="Successfully set " + self.vacationAdvisor.get() + " on vacation.")
                for a in advisorList:
                    if a.name == self.vacationAdvisor.get():
                        a.switch = "OFF"
                self.vacationAdvisor.set('')
            except:
                messagebox.showerror(title="Vacation", message="Fail to set the advisor on vacation.")

    def m_backToWork(self):
        if self.backToWork.get() == "":
            messagebox.showerror(title="Vacation", message="Please specify advisor.")
        else:
            try:
                messagebox.showinfo(title="Back to work", message="Successfully set " + self.backToWork.get() + " back to work.")
                for a in advisorList:
                    if a.name == self.backToWork.get():
                        a.switch = "ON"
                self.backToWork.set('')
            except:
                messagebox.showerror(title="Back to work", message="Fail to set the advisor back to work.")


    def m_viewAvil(self):
        # Use a list to show current available advisors and their corresponding tasks
        try:
            s1 = "*" * 55 + "\n\t\tAvailable advisors\n" + "*" * 55 + "\n"
            counter = 0
            for a in advisorList:
                if a.switch == "ON":
                    s1 += str(a.name).center(80) + "\n"
                    counter += 1
            footer = "\n\t\tTotal: " + str(counter)
            s1 += footer + "\n"
            s1 += "*" * 55 + "\n"

            for a in taskList:
                s1 += str(a.t_task_name + ": ")
                for eachAdv in a.t_task_advisor_list:
                    if eachAdv.switch == "ON":
                        s1 += str(eachAdv.name) + " "
                s1 += "\n"
            s1 += "*" * 55 + "\n"
            messagebox.showinfo(title="View availability", message=s1)
        except:
            messagebox.showerror(title="Error", message="Please handle this error manually. Error code 3")


    def updateInfo(self):
        # Save each changes in option (except View availbility, Vacation) to local file
        # Vacation is a case that an advisor is temporarily ignored from task list during this runtime.
        # The advisor will be back in task list once the program is restarted. If you restart the program
        # at the same day you set an advisor to Vacation, please set the advisor to Vacation again.

        try:
            # Clear file in case user wants to email twice
            writeFile_taskList.seek(0)
            writeFile_taskList.truncate()
            writeFile_advisorList.seek(0)
            writeFile_advisorList.truncate()
            writeFile_groupList.seek(0)
            writeFile_groupList.truncate()

            for a in taskList:
                writeFile_taskList.write(str(a.t_task_name) + ". ")
                for b in a.t_task_advisor_list:
                    writeFile_taskList.write(("%s, " % b.name))

                writeFile_taskList.write(". " + str(a.t_task_requirement))
                writeFile_taskList.write(". " + str(a.t_task_weight) + "\n")
            writeFile_taskList.flush()
            os.fsync(writeFile_taskList.fileno())

            for b in advisorList:
                writeFile_advisorList.write(str(b.name) + "\n")
            writeFile_advisorList.flush()
            os.fsync(writeFile_advisorList.fileno())

            for c in groupList:
                for d in c:
                    writeFile_groupList.write(str(d.name) + ". ")
                writeFile_groupList.write("\n")
            writeFile_groupList.flush()
            os.fsync(writeFile_groupList.fileno())
        except:
            messagebox.showerror(title="Error", message="Please handle this error manually. Error code 4")

def app(environ, start_response):
    main()

def main():
    root = Tk()
    feedback = Feedback(root)
    root.update()
    root.protocol('WM_DELETE_WINDOW', feedback.tk_quit)
    root.mainloop()


if __name__ == "__main__": main()
