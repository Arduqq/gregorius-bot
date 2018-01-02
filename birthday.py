
import calendar
from datetime import datetime

birthdays = []

month = datetime.now().month
year = datetime.now().year


calendar.setfirstweekday(calendar.MONDAY)
cal = calendar.monthcalendar(year, month)

if len(str(month)) == 1:
    month = '0%s' % month
else:
    month = '%s' % month

def initBirthdays():
    global birthdays
    birthdays = []
    try:
        with open('birthdays') as f:
            lines = f.readlines()
        for line in lines:
            if not line.strip():
                continue
            data = line.split()
            birthdays.append((data[0],(int(data[1]),data[2]),int(data[3])))
    except FileNotFoundError:
        print("No birthdays file found.")

def addBirthday(name, day, month, year):
    global birthdays
    try:
        with open('birthdays','a') as f:
            f.write('\n' + name + ' ' + day + ' ' + month + ' ' + year + '\n')
    except FileNotFoundError:
        print("No birtdays file found.")

def birthday(day, month):
    global birthdays
    for birthday in birthdays:
        if (day,month) in birthday:
            return True
    return False

def getBirthdays():
    return '\n'.join('{} - '.format(*k[1][0:]) + '{}.{}.'.format(*k[1][1]) + ' (wird ' + str(year-k[1][2]) + ' Jahre alt)' for k in enumerate(birthdays) if k[1][1][1] == month)

def createCalendar():
    output = ''
    output += '|++++++ %s-%s +++++|\n' % (month, year)
    output += '|Mo Di Mi Do Fr Sa So|\n'
    output += '|--------------------|\n'
     
    # draw calendar views
    border = '|'
    for week in cal:
        line = border
        
        for day in week:
            if birthday(day,month):
                line += ' X '
            else:
                if day == 0:
                    line += '   '  # 3 spaces for blank days
                elif len(str(day)) == 1:
                    line += ' %d ' % day
                else:
                    line += '%d ' % day
     
        line = line[0:len(line) - 1]  # remove space in last column
        line += border
        output += line + '\n'
 
    output += '|--------------------|\n'

    return output
