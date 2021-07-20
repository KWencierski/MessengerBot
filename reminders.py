import datetime

reminders = []


def reminding(browser, content):
    print(content)
    sum = "PRZYPOMNIENIE: " + content
    sendMessage(browser, sum)


def reminder_check(browser):
    now = datetime.datetime.now()
    somethingToRemove = False
    linecopy = ""
    for line in reminders:
        linecopy = line
        line = line[1:-1]
        comma_index = line.find(',')
        year = int(line[:comma_index])
        line = line[comma_index + 2:]
        comma_index = line.find(',')
        month = int(line[:comma_index])
        line = line[comma_index + 2:]
        comma_index = line.find(',')
        day = int(line[:comma_index])
        line = line[comma_index + 2:]
        comma_index = line.find(',')
        hour = int(line[:comma_index])
        line = line[comma_index + 2:]
        comma_index = line.find(',')
        minute = int(line[:comma_index])
        line = line[comma_index + 2:]
        comma_index = line.find(']')
        second = int(line[:comma_index])
        content = line[comma_index + 1:]

        if year == now.year:
            if month == now.month:
                if day == now.day:
                    if hour == now.hour:
                        if minute == now.minute:
                            if second <= now.second:
                                reminding(browser, content)
                                somethingToRemove = True
                        elif minute < now.minute:
                            reminding(browser, content)
                            somethingToRemove = True
                    elif hour < now.hour:
                        reminding(browser, content)
                        somethingToRemove = True
                elif day < now.day:
                    reminding(browser, content)
                    somethingToRemove = True
            elif month < now.month:
                reminding(browser, content)
                somethingToRemove = True
        elif year < now.year:
            reminding(browser, content)
            somethingToRemove = True

    if somethingToRemove:
        reminders.remove(linecopy)

        file = open("C:\\Users\\kajte\\PycharmProjects\\reminder.txt", 'w', encoding='utf8')
        for line in reminders:
            file.write(line)
        file.close()


def time_converter(given):
    given = given.split(' ')
    now = datetime.datetime.now()
    result = [now.year, now.month, now.day, now.hour, now.minute, now.second]

    while len(given) > 0:
        number = int(given[0])
        print(number)
        if "sek" in given[1]:
            result[5] += number
        elif "min" in given[1]:
            result[4] += number
        elif "godzi" in given[1]:
            result[3] += number
        elif "dni" in given[1] or "dzie" in given[1]:
            result[2] += number
        elif "miesi" in given[1]:
            result[1] += number
        elif "rok" in given[1] or "lat" in given[1]:
            result[0] += number
        else:
            print("WTF is " + given[1])
        given = given[2:]

    while result[1] > 12 or result[2] > 31 or result[3] > 23 or result[4] > 59 or result[5] > 59:
        #60+ chceck
        if result[5] >= 60:
            result[5] -= 60
            result[4] += 1
        if result[4] >= 60:
            result[4] -= 60
            result[3] += 1
        if result[3] >= 24:
            result[3] -= 24
            result[2] += 1
        if result[1] == 2 and result[2] > 28:
            result[2] -= 28
            result[1] += 1
        if result[2] > 30 and (result[1] == 2 or result[1] == 4 or result[1] == 6 or result[1] == 9 or result[1] == 11):
            result[2] -= 30
            result[1] += 1
        if result[2] > 31 and (result[1] == 1 or result[1] == 3 or result[1] == 5 or result[1] == 7 or result[1] == 8 or result[1] == 10 or result[1] == 12):
            result[2] -= 31
            result[1] += 1
        if result[1] > 12:
            result[1] -= 12
            result[0] += 1
    return result


def addReminder(browser, remind_message):
    remind_message = remind_message.replace("!przypomnij ", "")

    if " za " in remind_message:
        content_max_index = remind_message.find(" za ")
        content = remind_message[:content_max_index]
        remind_time = remind_message[content_max_index + 1:]
        remind_time = remind_time.replace("za ", "")
        remind_time = time_converter(remind_time)

        reminders.append(str(remind_time) + content + '\n')

        file = open("C:\\Users\\kajte\\PycharmProjects\\reminder.txt", 'a', encoding='utf8')
        file.write(str(remind_time) + content + '\n')
        file.close()

        print("Dodano reminder!")
        sendMessage(browser, "Dodano przypomnienie!")
    else:
        print("Brak za!")
        sendMessage(browser, "Nieprawidłowy format!")


def loadReminders():
    print("loading reminders...")
    global reminders
    reminders = []
    file = open("C:\\Users\\kajte\\PycharmProjects\\reminder.txt", encoding='utf8')
    for line in file:
        reminders.append(line)
    file.close()


from messenger import sendMessage
