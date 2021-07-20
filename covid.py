import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

covidNewInfections = []
covidNewDeaths = []
covidVacinatedFirst = []
covidVacinatedSecond = []
covidDelay = 0.5


def getCovidInfo(browserCovid):
    browserCovid.get("https://twitter.com/mz_gov_pl")
    found = 0
    covidMessage = ""
    covidMessage2 = ""
    covidMessage3 = ""
    time.sleep(covidDelay)

    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, "r-kzbkwu"))
        WebDriverWait(browserCovid, 20).until(element_present)
    except:
        print("Timed out waiting for page to load")
    for i in range(30):
        searchElems = browserCovid.find_elements_by_class_name("r-kzbkwu")

        for i in searchElems:
            if ("W ciągu doby wykonano" in i.text):
                covidMessage3 = i.text
            if ("Z powodu" in i.text and "współistnie" in i.text):
                covidMessage2 = i.text
            if ("nowych i potwierdzonych" in i.text or "nowe i potwierdzone" in i.text):
                covidMessage = i.text
                if covidMessage2 == '':
                    time.sleep(covidDelay * 3)
                    i.click()
                found = True
                break

        if found:
            time.sleep(covidDelay)
            if covidMessage2 == '':
                searchElems = browserCovid.find_elements_by_css_selector(
                    "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(2) > div > section > div > div > div:nth-child(4) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu > div:nth-child(2) > div:nth-child(1) > div")
                for i in searchElems:
                    if ("Z powodu" in i.text and "współistnie" in i.text):
                        covidMessage2 = i.text
                        break

            covidMessage = covidMessage[covidMessage.find("Mamy") + 5: covidMessage.find("now") - 1]
            died = covidMessage2[covidMessage2.find("zmarł") + 7 : covidMessage2.find("os") - 1]
            died2 = covidMessage2[covidMessage2.find("os") + 5:]
            died2 = died2[died2.find("zmar") + 7: died2.find("os") - 1]
            died = int(died.replace(" ", "")) + int(died2.replace(" ", ""))
            covidMessage2 = str(died)

            covidMessage3 = covidMessage3[covidMessage3.find("ponad") + 6 : covidMessage3.find("tys") - 1]
            covidMessage3 = covidMessage3.replace(',', '.')

            break

        browserCovid.execute_script("window.scrollTo(0, window.scrollY + 300)")
        time.sleep(covidDelay)

    if covidMessage.replace(' ', '') == covidNewInfections[-1] and covidMessage2 == covidNewDeaths[-1]:
        print("Ktos uzywa update jak nie ma potrzeby!")
        return ["", "", ""]

    covidNewInfections.append(covidMessage.replace(' ', ''))

    file = open("C:\\Users\\kajte\\PycharmProjects\\covidData.txt", "a", encoding='utf8')
    file.write(covidMessage.replace(' ', ''))
    file.write("\n")
    file.close()

    covidNewDeaths.append(covidMessage2)

    file = open("C:\\Users\\kajte\\PycharmProjects\\covidData2.txt", "a", encoding='utf8')
    file.write(covidMessage2)
    file.write("\n")
    file.close()

    return [covidMessage, covidMessage2, covidMessage3]


def cmpLast2(tab):
    tabLen = len(tab)
    if tabLen < 2:
        print("ERROR: do funkcji cmpLast2 podano za mala tablice!")
        return "ERROR"
    else:
        if int(tab[tabLen - 1]) > int(tab[tabLen - 2]):
            percent = round((int(tab[tabLen - 1]) - int(tab[tabLen - 2])) / float(tab[tabLen - 2]) * 100, 2)
            return str(percent) + "% " + "\u2191" + "\u2191" + "\u2191"

        else:
            percent = round((int(tab[tabLen - 2]) - int(tab[tabLen - 1])) / float(tab[tabLen - 2]) * 100, 2)
            return str(percent) + "% " + "\u2193" + "\u2193" + "\u2193"


def getCovidVaccinateInfo(browserCovid):
    browserCovid.get("https://twitter.com/szczepimysie")

    found = False
    firstDose = ""
    secondDose = ""
    message = ""
    browserCovid.implicitly_wait(covidDelay)

    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, "r-kzbkwu"))
        WebDriverWait(browserCovid, 20).until(element_present)
    except:
        print("Timed out waiting for page to load")
    for i in range(50):
        searchElems = browserCovid.find_elements_by_class_name("r-kzbkwu")
        for i in searchElems:
            if ("Wykonaliśmy" in i.text and "szczepi" in i.text):
                message = i.text
                found = True
                break

        if found:
            firstTo = 0
            for j in range(3):
                firstTo = message.find("szczepi", firstTo + 1)
            firstDose = message[message.find("wykonano") + len("wykonano") + 1 : firstTo - 1]

            secFrom = 0
            for j in range(2):
                secFrom = message.find("jest")
            secFrom += len("jest") + 1
            secTo = message.find("os")

            secondDose = message[secFrom: secTo - 1]
            break

        browserCovid.execute_script("window.scrollTo(0, window.scrollY + 300)")
        time.sleep(covidDelay)

    covidVacinatedFirst.append(firstDose.replace(" ", ""))

    file = open("C:\\Users\\kajte\\PycharmProjects\\covidVacinationData.txt", "a", encoding='utf8')
    file.write(firstDose.replace(' ', ''))
    file.write("\n")
    file.close()

    covidVacinatedSecond.append(secondDose.replace(" ", ""))

    file = open("C:\\Users\\kajte\\PycharmProjects\\covidVacinationData2.txt", "a", encoding='utf8')
    file.write(secondDose.replace(' ', ''))
    file.write("\n")
    file.close()

    return [firstDose, secondDose]


def cmpToPop(elem):
    print("cmpToPop")
    popSize = 37643375

    percent = round(int(elem) / float(popSize) * 100, 2)
    return str(percent) + "%"


def loadCovidData():
    file = open("C:\\Users\\kajte\\PycharmProjects\\covidData.txt", encoding='utf8')
    for line in file:
        covidNewInfections.append(line.replace('\n', ''))
    file.close()

    file = open("C:\\Users\\kajte\\PycharmProjects\\covidData2.txt", encoding='utf8')
    for line in file:
        covidNewDeaths.append(line.replace('\n', ''))
    file.close()

    file = open("C:\\Users\\kajte\\PycharmProjects\\covidVacinationData.txt", encoding='utf8')
    for line in file:
        covidVacinatedFirst.append(line.replace('\n', ''))
    file.close()

    file = open("C:\\Users\\kajte\\PycharmProjects\\covidVacinationData2.txt", encoding='utf8')
    for line in file:
        covidVacinatedSecond.append(line.replace('\n', ''))
    file.close()


def sendCovidUpdate(browser, browserCovid):
    covidInfo = getCovidInfo(browserCovid)
    covidMessage = covidInfo[0]
    covidMessage2 = covidInfo[1]
    covidMessage3 = covidInfo[2]

    covidVaccinatedInfo = getCovidVaccinateInfo(browserCovid)

    if covidMessage != "":
        sendMessage(browser, "Dzień dobry! Koronawirus dopadł wczoraj " + covidMessage + " osób" + "(" + cmpLast2(
            covidNewInfections) + ")")
        sendMessage(browser, "Wykonano " + covidMessage3 + " tys. testów (" + str(
            round(float(covidMessage.replace(' ', '')) / float(covidMessage3) / 10, 2)) + "% pozytywnych)")
        sendMessage(browser, "Zmarło " + covidMessage2 + " osób" + "(" + cmpLast2(covidNewDeaths) + ")")

        if covidVaccinatedInfo[0] != "":
            sendMessage(browser, "Pierwszą dawką zostało już zaszczepionych " + covidVaccinatedInfo[
                0] + " osób" + "(" + cmpToPop(covidVaccinatedInfo[0].replace(' ', '')) + ")")
            sendMessage(browser,
                        "W pełni zostało już zaszczepionych " + covidVaccinatedInfo[1] + " osób" + "(" + cmpToPop(
                            covidVaccinatedInfo[1].replace(' ', '')) + ")")

    else:
        print("Nie udało się odnaleźć danych covida!")


from messenger import sendMessage
