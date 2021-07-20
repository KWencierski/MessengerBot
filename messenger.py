from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

firstLogin = True
messageDelay = 0.5


def brokenButton(browser, searchElem):
    action = webdriver.common.action_chains.ActionChains(browser)
    action.move_to_element_with_offset(searchElem, 5, 5)
    action.click()
    action.perform()


def logging (browser):
    time.sleep(messageDelay)
    searchElem = browser.find_elements_by_class_name("_51sy")
    searchElem[-1].click()

    searchElem = browser.find_element_by_class_name("_4jy1")
    brokenButton(browser, searchElem)

    searchElem = browser.find_element_by_css_selector("#email")
    searchElem.send_keys("email")

    searchElem = browser.find_element_by_css_selector("#pass")
    searchElem.send_keys("password")

    searchElem = browser.find_element_by_css_selector("#loginbutton")
    searchElem.click()


def sendMessage(browser, message):
    print("sendMessage()")
    message = message.replace("ą", 'a')
    message = message.replace("ć", 'c')
    message = message.replace("ż", 'z')
    message = message.replace("ź", 'z')
    write = browser.find_elements_by_class_name("_1mj")
    write[0].send_keys(message)
    time.sleep(messageDelay)
    write = browser.find_elements_by_class_name("_1mj")
    write[0].send_keys(Keys.ENTER)


def mention1(browser, person):
    sum = "@" + person
    sendMessage(browser, sum)
    time.sleep(messageDelay)
    sendMessage(browser, Keys.ENTER)
    sendMessage(browser, Keys.ENTER)


def mention(browser, people):
    for person in people:
        mention1(browser, person)


def getLastMessage(browser):
    messages = []
    messagesText = []
    returnMessage = ""
    time.sleep(messageDelay * 2)
    while True:
        try:
            messages = browser.find_elements_by_class_name("oo9gr5id")
            for i in messages:
                messagesText.append(i.text)
        except:
            print("StaleElementReferenceException in getLastMessage")
            restart(browser)
        if messages:
            break

    lastMessageIndex = -1

    while lastMessageIndex == -1:
        for i, mes in enumerate(messagesText):
            if mes == "Aa":
                lastMessageIndex = i - 1
                returnMessage = messages[lastMessageIndex].text
                break
        browser.implicitly_wait(messageDelay)

    if lastMessageIndex == -1:
        for i in messagesText:
            print(i)
        print("ERROR: getLastMessage index -1!!!")
        exit(-1)

    return returnMessage


def sendPic(browser, picLocation):
    element = browser.find_element_by_xpath("//*[@id=\"mount_0_0\"]/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/form/div/div[3]/div[1]/div[1]/span/div")
    # element = browser.find_element_by_xpath("")
    # element = browser.find_element_by_xpath("")
    # browser.execute_script("arguments[0].click();", element)
    element.send_keys(picLocation)


def reactToLastMessage(browser, emoteNumber):
    if emoteNumber < 1 or emoteNumber > 7:
        print("Invalid emoteNumber value!")
        return
    print("reactToLastMessage")
    # 7 - serce, 1 - dislike
    emoteNumber = -emoteNumber

    buttons = browser.find_elements_by_class_name("rgmg9uty")
    buttons[-2].click()
    # otworzenie menu z emotkami (-1 - ...; -2 - odp; -3 - emotki)
    menu = browser.find_elements_by_class_name("i2p6rm4e")
    menu[-3].click()

    # wybieranie emotki (-7 --- -1)
    emote = browser.find_elements_by_class_name("bsnbvmp4")
    emote[emoteNumber].click()


def restart(browser):
    print("restarting...")
    global firstLogin

    browser.get("https://www.messenger.com/login")
    time.sleep(messageDelay)

    if firstLogin:
        logging(browser)
        firstLogin = False
    browser.get("https://www.messenger.com/t/933765696725842")

    time.sleep(messageDelay)
    while len(browser.find_elements_by_class_name("oo9gr5id")) < 15:
        time.sleep(messageDelay)
