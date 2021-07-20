from selenium.webdriver.chrome.options import Options
from selenium import webdriver

option = Options()
availableCommands = "!panmaruda, !mury, !cytat, !komendy, !zmiany, @gt, !przypomnij, !helpPrzypomnij, " \
                    "@all, @rataje, !covid, !dodajCytat, !helpDodajCytat, !koleda, !źle"
changes = "BOT Kajtek 0.5.0     Rozłożono cały kod na oddzielne pliki, poprawiono " \
         "komendę !komendy, wprowadzono 2 rodzaje pracy bota: czas bezczynności i czas pracy, " \
          "przez co bot będzie pracował szybciej, kiedy pojawiają się wiadomości, ale może też " \
          "wolniej reagować na pierwszą wiadomość. And last but not least: Bot od teraz uczy się " \
          "reagować na wiadomości skierowane do niego. Niestety, na razie jego baza wiedzy jest " \
          "bardzo mała, ale z każdą kolejną wiadomością będzie coraz mądrzejszy! Przez to wprowadzo " \
          "dodatkową komendę !źle, która informuje bota, że jego ostatnia reakcja była nieprawidłowa " \
          "i dzięki temu będzie się uczył."

idleDelay = 5
workingDelay = 0.5
delay = workingDelay
maxIdle = 2 * 60 / workingDelay

option.add_argument("--disable-infobars")
option.add_argument("--disable-extensions")
option.add_argument("--headless")

option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})

browser = webdriver.Chrome("C:\\Users\\kajte\\OneDrive\\Pulpit\\chromedriver.exe", options=option)
browserBurgers = webdriver.Chrome("C:\\Users\\kajte\\OneDrive\\Pulpit\\chromedriver.exe", options=option)
browserCovid = webdriver.Chrome("C:\\Users\\kajte\\OneDrive\\Pulpit\\chromedriver.exe", options=option)


from messenger import *
from quotes import *
from reminders import *
from covid import *
from burgers import *
from birthdays import *
from reacting import *

loadQuotes()
loadReminders()
loadCovidData()
loadLastReaction()
restart(browser)
prevMessage = ""
idleCounter = 0
quoted = False
covided = False

while True:
    browser.implicitly_wait(delay)
    senders = browser.find_elements_by_class_name("dkr8dfph")

    reminder_check(browser)
    now = datetime.datetime.now()
    if now.hour == 20 and now.minute == 30 and not quoted:
        print("quote TIME")
        quoted = True
        sendQuote(browser)

    if now.hour == 10 and now.minute == 50 and not covided:
        print("covid TIME")
        covided = True
        sendCovidUpdate(browser, browserCovid)

    lastMessage = getLastMessage(browser)
    if delay == workingDelay and idleCounter >= maxIdle:
        print("idle mode on")
        delay = idleDelay
    if lastMessage == prevMessage:
        idleCounter += 1
        browser.implicitly_wait(delay)
        continue
    delay = workingDelay
    idleCounter = 0
    prevMessage = lastMessage
    print(senders[-1].text)
    print(lastMessage)
    chceckBirthdays(browser, now, senders[-1].text)

    if "!covid" in lastMessage.lower():
        print("covid")
        sendCovidUpdate(browser, browserCovid)

    elif "!panmaruda" in lastMessage.lower() or "!pan maruda" in lastMessage.lower():
        print("PAN MARUDA!")
        sendMessage(browser, "imgur.com//DQiqmp3")

    elif "!mury" in lastMessage.lower():
        print("mury")
        getLastBurgersInfo(browser, browserBurgers)

    elif "!cytat" in lastMessage.lower():
        print("cytat")
        sendQuote(browser)

    elif "!komendy" in lastMessage.lower():
        print("komendy")
        sendMessage(browser, availableCommands)

    elif "!zmiany" in lastMessage.lower():
        print("zmiany")
        sendMessage(browser, changes)

    elif "@gt" in lastMessage.lower():
        print("GT")
        mention(browser, ["Szymon"])

    elif "@all" in lastMessage.lower():
        print("Mention all")
        mention(browser, ["Kajetan", "Szymon", "Gracjan", "Piotrek", "Krzy"])

    elif "@rataje" in lastMessage.lower():
        print("Mention rataje")
        mention(browser, ["Kajetan", "Szymon", "Gracjan"])

    elif "xiaomi" in lastMessage.lower():
        print("xiaomi")
        mention1(browser, "Piotrek")

    elif "anime" in lastMessage.lower():
        print("anime")
        mention1(browser, "Gra")

    elif "!przypomnij" in lastMessage.lower():
        print("remindme")
        addReminder(browser, lastMessage)

    elif "!helpprzypomnij" in lastMessage.lower():
        print("helpPrzypomnij")
        sendMessage(browser, "Komenda przypomnij, jak sama nazwa wskazuje, umożliwia tworzenie "
                    "customowych przypomnien. Po komendzie należy wpisać nazwę przypomnienia, "
                    "a następnie słowo \"za\" i podać interesujący nas czas oczekiwania, np "
                    "wyłączyć piekarnik za 5 minut. Uwaga! Należy używać jedostek niewykraczających "
                    "poza dany zakre, np. zamiast 48 godzin należy wpisać 2 dni.")

    elif "!koleda" in lastMessage.lower():
        text = []
        text.append("Last Christmas")
        text.append("I gave you my heart")
        text.append("But the very next day")
        text.append("you gave it away")
        text.append("Thiiiis year")
        text.append("to save me from tears")
        text.append("I'll give it to someone...")

        for i in text:
            sendMessage(browser, i)

    elif "bot" in lastMessage.lower():
        print("Bot in message")
        # reactToLastMessage(browser, random.randint(1, 7))
        loadReactions()
        if clasificateMessage(lastMessage) >= 0:
            reactToLastMessage(browser, 7)
        else:
            reactToLastMessage(browser, 3)
        saveNewReaction(lastMessage)

    elif "!dodajCytat" in lastMessage or "!dodajcytat" in lastMessage:
        addQuote(lastMessage)
        sendMessage(browser, "Dodano cytat!")

    elif "!helpdodajcytat" in lastMessage.lower() or "!helpcytat" in lastMessage.lower():
        sendMessage(browser, "Po komendzie !dodajCytat należy wpisać cytat (bez cudzysłowu!), a "
                             "następnie po myślniku wpisać autora cytatu")

    elif "!źle" in lastMessage.lower() or "!zle" in lastMessage.lower() or "!zly" in lastMessage.lower()  or "!zły" in lastMessage.lower():
        reactToLastMessage(browser, 4)
        changeLastSavedReaction()

    else:
        print(".")
