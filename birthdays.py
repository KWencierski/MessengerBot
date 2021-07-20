def chceckBirthdays(browser, now, sender):
    if now.day == 18 and now.month == 5 and "Gracjan" in sender:
        reactToLastMessage(browser, 2)

    elif now.day == 6 and now.month == 7 and "Szym" in sender:
        reactToLastMessage(browser, 2)

    elif now.day == 15 and now.month == 1 and "Pi" in sender:
        reactToLastMessage(browser, 2)

    elif now.day == 19 and now.month == 1 and "Krzy" in sender:
        reactToLastMessage(browser, 2)

    elif now.day == 24 and now.month == 1 and "Kaj" in sender:
        reactToLastMessage(browser, 2)


from messenger import reactToLastMessage
