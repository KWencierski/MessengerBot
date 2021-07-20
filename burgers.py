def getLastBurgersInfo(browser, browserBurgers):
    browserBurgers.get("https://www.facebook.com/pg/namurze/posts/?ref=page_internal")
    odp = []
    if browserBurgers.find_elements_by_class_name("_4-u8"):
        posty = browserBurgers.find_elements_by_class_name("_4-u8")
        linie = list(posty[9].text.splitlines())
        lubieTo = linie.index("Lubię to!")
        for i in range(1, lubieTo - 3):
            if linie[i] == "":
                continue
            else:
                odp.append(linie[i])

        for i in odp:
            i = ''.join(c for c in i if c <= '\uFFFF')
            sendMessage(browser, i)
    else:
        print("Nie znaleziono burgerow!")


from messenger import sendMessage
