from django.shortcuts import render, redirect
from .models import RecordedTask, advisor, task, counterModel
from .forms import newTaskForm, callOnce, newCounterForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
import random
import datetime
import urllib.request
import sendgrid
import os
from sendgrid.helpers.mail import *

import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Authorization system refer to:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication


def initGroup():
    '''
    This method is called when program runs for the first time or
    whenever advisor info is modified. It adds advisors into groups.
    :return: no return
    '''
    global group1
    global group2
    global group3
    group1 = []
    group2 = []
    group3 = []

    for eachAdvisor in advisor.objects.all():
        if eachAdvisor.advisor_group == 1:
            group1.append(eachAdvisor)
        elif eachAdvisor.advisor_group == 2:
            group2.append(eachAdvisor)
        elif eachAdvisor.advisor_group == 3:
            group3.append(eachAdvisor)
    # Shuffle order of advisors in groups
    random.shuffle(group1)
    random.shuffle(group2)
    random.shuffle(group3)


# Initialize groups
if callOnce:
    initGroup()
    print('call initGroup')
    callOnce = False


def taskHandler(taskName):
    '''
    This method turns a string taskName to a task object
    because other attributes of this task object are needed
    :param taskName: task name in string
    :return:
    '''
    # No need to check if there is no matched since already checked
    for eachTask in task.objects.all():
        if eachTask.task_name == str(taskName):
            return eachTask


def advisorHandler(advisorName):
    '''
    This method turns a string advisorName to an advisor object
    because other attributes of this advisor object are needed
    :param taskName: task name in string
    :return:
    '''
    # No need to check if there is no matched since already checked
    for eachAdvisor in advisor.objects.all():
        if eachAdvisor.advisor_name == advisorName:
            return eachAdvisor


def getGroupFromThreeGroups():
    '''
    This method counts the ratio among 3 groups and select one group.
    :return: a group that should handle the task
    '''
    count_group1 = 0
    count_group2 = 0
    count_group3 = 0

    t_group1 = []
    t_group2 = []
    t_group3 = []

    advisorObj = advisor.objects.all()
    for each in advisorObj:
        if each.advisor_group == 1:
            t_group1.append(each)
        elif each.advisor_group == 2:
            t_group2.append(each)
        elif each.advisor_group == 3:
            t_group3.append(each)


    for a in t_group1:
        print(a.advisor_weight)
        count_group1 += a.advisor_weight
    for a in t_group2:
        print(a.advisor_weight)
        count_group2 += a.advisor_weight
    for a in t_group3:
        print(a.advisor_weight)
        count_group3 += a.advisor_weight

    print('---------')
    print('count_group1 ' + str(count_group1))
    print('count_group2 ' + str(count_group2))
    print('count_group3 ' + str(count_group3))
    print('---------')

    if count_group1 == 0:
        return t_group1
    elif count_group1 != 0 and count_group2 == 0:
        return t_group2
    elif count_group1 != 0 and count_group2 != 0 and count_group3 == 0:
        return t_group3
    else:
        # 80%:45%:20% is actually 4:2.25:1
        if count_group1 / count_group2 == (4 / 2.25):
            if count_group2 / count_group3 == 2.25:
                print('select group 1')
                return t_group1
            elif count_group2 / count_group3 < 2.25:
                print('select group 2')
                return t_group2
            elif count_group2 / count_group3 > 2.25:
                print('select group 3')
                return t_group3
        elif count_group1 / count_group2 < (4 / 2.25):
            '''
            In case number of total tasks is small and A/B < ratio,
            if A/B > half ratio,
                if B/C < half ratio, return C
                else, return A
            else,
                return A
            '''
            if count_group1 / count_group2 > (3 / 2.25):
                if count_group2 / count_group3 < 1.125:
                    print('select group 3')
                    return t_group3
                else:
                    print('select group 1')
                    return t_group1
            else:
                print('select group 1')
                return t_group1
        elif count_group1 / count_group2 > (4 / 2.25):
            '''
            if A/B > ratio,
                if B/C < ratio, return B
                else, return C
            '''
            if count_group2 / count_group3 < 1.85:
                print('select group 2')
                return t_group2
            else:
                print('select group 3')
                return t_group3


def getGroupFromTwoGroups(num1, num2):
    '''
    This method counts the ratio between 2 groups and select one group.
    :return: a group that should handle the task
    '''
    count_group1_two = 0
    count_group2_two = 0
    count_group3_two = 0

    tt_group1 = []
    tt_group2 = []
    tt_group3 = []

    advisorObj = advisor.objects.all()
    for each in advisorObj:
        if each.advisor_group == 1:
            tt_group1.append(each)
        elif each.advisor_group == 2:
            # Hello Houqi, My name is Tik Tok...
            tt_group2.append(each)
        elif each.advisor_group == 3:
            tt_group3.append(each)

    for a in tt_group1:
        print(a.advisor_weight)
        count_group1_two += a.advisor_weight
    for a in tt_group2:
        print(a.advisor_weight)
        count_group2_two += a.advisor_weight
    for a in tt_group3:
        print(a.advisor_weight)
        count_group3_two += a.advisor_weight

    print('---------')
    print('count_group1 ' + str(count_group1_two))
    print('count_group2 ' + str(count_group2_two))
    print('count_group3 ' + str(count_group3_two))
    print('---------')
    print('groups: %d %d' %(num1, num2))

    # Ratio between group 1 and 2 is 80%:45% or 4:2.25
    if num1 == 1 and num2 == 2:
        if count_group1_two == 0:
            print('select group 1')
            return tt_group1
        elif count_group2_two == 0:
            print('select group 2')
            return tt_group2
        if count_group1_two / count_group2_two <= (4 / 2.25):
            print('select group 1')
            return tt_group1
        else:
            print('select group 2')
            return tt_group2
    # Ratio between group 1 and 3 is 80%:20% or 4:1
    elif num1 == 1 and num2 == 3:
        if count_group1_two == 0:
            print('select group 1')
            return tt_group1
        elif count_group3_two == 0:
            print('select group 3')
            return tt_group3
        if count_group1_two / count_group3_two <= 4:
            print('select group 1')
            return tt_group1
        else:
            print('select group 3')
            return tt_group3
    # Ratio between group 1 and 3 is 45%:20% or 2.25:1
    elif num1 == 2 and num2 == 3:
        if count_group2_two == 0:
            print('select group 2')
            return tt_group2
        elif count_group3_two == 0:
            print('select group 3')
            return tt_group3
        if count_group2_two / count_group3_two <= 2.25:
            print('select group 2')
            return tt_group2
        else:
            print('select group 3')
            return tt_group3


def selectAdvisor(taskName, group):
    '''
    This method calculates which advisor in the group to handle the task.
    This advisor is whoever has minimum weights in this group.
    :param taskName: task name to handle
    :param group: the group from which advisor is drew
    :return: an advisor
    '''

    list = turnStrToList(taskName.task_advisor_list)
    taskObjectList = []
    for each in list:
        taskObjectList.append(advisorHandler(each))

    min = 0
    for each in taskObjectList:
        min += each.advisor_weight
    selected = taskObjectList[0]

    for eachAdvisor in taskObjectList:
        if eachAdvisor in group and eachAdvisor.advisor_switch == "ON":
            if eachAdvisor.advisor_weight < min:
                selected = eachAdvisor
                min = eachAdvisor.advisor_weight
    print('selected last: ' + selected.advisor_name)
    thisTask = taskHandler(taskName)
    print('taskName ' + taskName.task_name)

    selected.advisor_weight += thisTask.task_weight
    selected.advisor_count += 1
    thisTask.task_num += 1
    selected.save()
    thisTask.save()
    return selected


@login_required
def newtask(request):
    context = {
        "form": newTaskForm
    }
    return render(request, "newtask.html", context)


def turnStrToList(str):
    '''
    This method turns a string to a list, splitted by comma
    :param str: input
    :return: tempList as output
    '''
    spliter = str.split(',')
    tempList = []
    for each in spliter:
        if each != '':
            tempList.append(each.strip())
    return tempList


@login_required
def calcAdvisor(request, taskName, advisorName):
    '''
    General method to find an advisor to handle the task. This method
    calls selectAdvisor, getGroupFromThreeGroups, and getGroupFromTwoGroups
    :param request: system request
    :param taskName: the task to handle
    :return:taskNotAssigned
    '''

    taskNotAssigned = True
    if advisorName == ' ' or advisorName == 'notspecified':
        hasGroup1 = False
        hasGroup2 = False
        hasGroup3 = False
        for eachTask in task.objects.all():
            if eachTask.task_name == taskName:
                # Use a loop to get groups that can handle the task
                for eachAdvisorName in turnStrToList(eachTask.task_advisor_list):
                    tempAdvisorObject = advisorHandler(eachAdvisorName)
                    if tempAdvisorObject.advisor_group == 1 and tempAdvisorObject.advisor_switch == "ON":
                        hasGroup1 = True
                    elif tempAdvisorObject.advisor_group == 2 and tempAdvisorObject.advisor_switch == "ON":
                        hasGroup2 = True
                    elif tempAdvisorObject.advisor_group == 3 and tempAdvisorObject.advisor_switch == "ON":
                        hasGroup3 = True

                '''
                4 Cases:
                    1. no one can handle
                    2. 3 groups can handle
                    3. 2 groups can handle
                    4. 1 group can handle
                '''
                # no one can handle
                if hasGroup1 == False and hasGroup2 == False and hasGroup3 == False:
                    print('no one can handle')
                    break

                # 3 groups can handle
                elif hasGroup1 == True and hasGroup2 == True and hasGroup3 == True:
                    temp_group = getGroupFromThreeGroups()
                    assignTo = selectAdvisor(eachTask, temp_group)


                # 2 groups can handle
                elif hasGroup1 == True and hasGroup2 == True and hasGroup3 == False:
                    assignTo = selectAdvisor(eachTask, getGroupFromTwoGroups(1, 2))
                elif hasGroup1 == True and hasGroup2 == False and hasGroup3 == True:
                    assignTo = selectAdvisor(eachTask, getGroupFromTwoGroups(1, 3))
                elif hasGroup1 == False and hasGroup2 == True and hasGroup3 == True:
                    assignTo = selectAdvisor(eachTask, getGroupFromTwoGroups(2, 3))

                # 1 groups can handle
                elif hasGroup1 == True and hasGroup2 == False and hasGroup3 == False:
                    assignTo = selectAdvisor(eachTask, group1)
                elif hasGroup1 == False and hasGroup2 == True and hasGroup3 == False:
                    assignTo = selectAdvisor(eachTask, group2)
                elif hasGroup1 == False and hasGroup2 == False and hasGroup3 == True:
                    assignTo = selectAdvisor(eachTask, group3)

                messages.add_message(request, messages.INFO, '%s is assigned to: %s. %s' % (
                    taskName, assignTo.advisor_name, taskHandler(taskName).task_requirement))
                taskNotAssigned = False
                break
    else:
        if taskNotAssigned != False:
            print('do not call getGroups, else case')
            assignTo = advisorHandler(advisorName)
            messages.add_message(request, messages.INFO, '%s is assigned to: %s. %s' % (
                    taskName, assignTo.advisor_name, taskHandler(taskName).task_requirement))
            taskNotAssigned = False
            # Increment advisor weight, count and task count
            thisTask = taskHandler(taskName)
            assignTo.advisor_weight += thisTask.task_weight
            assignTo.advisor_count += 1
            thisTask.task_num += 1
            assignTo.save()
            thisTask.save()

    if taskNotAssigned:
        messages.add_message(request, messages.WARNING, "This task is not assigned.")



@login_required
def addTask(request):
    bool_taskNotAssigned = True
    form = newTaskForm(request.POST)
    if form.is_valid():
        register = RecordedTask(taskName = form.cleaned_data['taskName'],
                                advisorName = form.cleaned_data['advisorName'],
                                updatedTime = timezone.now(),
                                )
        register.save()

        # Get last edited task time, compare it with today's date, if not same, clear data
        secondLastAddedTask = RecordedTask.objects.order_by('-pk')[1]
        last_edited_time = str(secondLastAddedTask.updatedTime)
        last_edited_time = last_edited_time[0:10]
        current_time = datetime.datetime.now().strftime("%Y-%m-%d")
        if last_edited_time < current_time:
            messages.add_message(request, messages.WARNING,
                                 '[IMPORTANT] Past data is cleared! Please refresh the page.')
            dailyClearData(request)
            removeHistoryData()
        else:
            # Calculate which advisor to handle this task and print it out
            calcAdvisor(request, register.taskName, register.advisorName)

        # TEST: clear all data, please comment it in production code
        #dailyClearData(request)
        #email(request)

    else:
        messages.add_message(request, messages.WARNING, 'Please select a task.')
    return redirect('newtask')


@login_required
def dailyClearData(request):
    ''' This method clears data everyday '''
    # Clear advisor info
    advisorObject = advisor.objects.all()
    for each in advisorObject:
        each.advisor_count = 0
        each.advisor_weight = 0
        each.save()

    # Clear task info
    taskObject = task.objects.all()
    for each in taskObject:
        each.task_num = 0
        each.save()

    # Clear Daily Traffic
    modelData = counterModel.objects.all()[0]
    modelData.counter = 0
    modelData.save()

    # Send out email to ISS admin
    #email(request)


def removeHistoryData():
    ''' Remove history data (ie RecordedTask in sqlite db)
    '''

    tempT = RecordedTask.objects.all()[:1].values_list("id", flat=True)
    RecordedTask.objects.exclude(pk__in=list(tempT)).delete()
    tempT2 = RecordedTask.objects.order_by('-pk')[0]
    tempT2.updatedTime = timezone.now()
    tempT2.save()
    print('Finish removing most history data')


@login_required
def email(request):
    ''' This methods sends out the email to admin '''

    try:
        link = 'https://uwiss.herokuapp.com/summary'

        html_content = urllib.request.urlopen(link).read().decode('ASCII')

        API_KEY = 'xxxx'

        sg = sendgrid.SendGridAPIClient(API_KEY)
        from_email = Email("unknown@outlook.com")
        to_email = Email("unknown@outlook.com")
        subject = 'Frontdesk Log ' + str(datetime.datetime.now().strftime("%Y-%m-%d"))
        content = Content("text/html", html_content)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())

        print(response.status_code)
        print(response.body)
        print(response.headers)

        messages.add_message(request, messages.SUCCESS, 'Email sent successfully.')
        print('Email sent successfully.')

    except:
        messages.add_message(request, messages.WARNING, 'Fail to sent the email.')


def summary(request):
    advisor_list = advisor.objects.all()
    task_list = task.objects.all()
    sum1 = 0
    sum2 = 0
    dailytraffic = counterModel.objects.all()[0].counter
    for eachAdvisor in advisor_list:
        sum1 += eachAdvisor.advisor_count
    for eachTask in task_list:
        sum2 += eachTask.task_num
    context = {
        "advisor_list": advisor_list,
        "task_list":task_list,
        "sum1": sum1,
        "sum2": sum2,
        "dailytraffic": dailytraffic,
    }
    return render(request, "summary.html", context)


@login_required
def newCounter(request):
    context = {
        "form": newCounterForm
    }
    return render(request, "counter.html", context)


@login_required
def addCounter(request):
    form = newCounterForm(request.POST)

    if form.is_valid():
        register = counterModel(counter = form.cleaned_data['counter'],
                                    )
        register.save()
        modelData = counterModel.objects.all()[0]
        modelData.counter = str(register.counter)
        modelData.save()
        print('counter is now: ' + str(register.counter))
        messages.add_message(request, messages.SUCCESS, "Counter added successfully.")
    return redirect('newCounter')