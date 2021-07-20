wordDict = dict()
lastReactionWasPositive = True

def standardiseString(string):
    x = string
    x = x.replace('.', '')
    x = x.replace(',', '')
    x = x.replace('?', '')
    x = x.replace('!', '')
    x = x.replace('(', '')
    x = x.replace(')', '')
    x = x.replace('[', '')
    x = x.replace(']', '')
    x = x.replace('{', '')
    x = x.replace('}', '')
    x = x.replace('@', '')
    x = x.replace(':', '')
    x = x.replace(';', '')
    # x = x.replace('/', '')
    x = x.replace('<', '')
    x = x.replace('>', '')
    x = x.replace('-', '')
    x = x.replace('_', '')
    x = x.replace('+', '')
    x = x.replace('=', '')
    x = x.lower()
    return x


def clasificateMessage(message):
    points = 0

    message = standardiseString(message)

    for i in message.split():
        if i in wordDict:
            points += wordDict[i]
    print("Clasification points: " + str(points))
    return points


def addWordToDict(word, weight):
    global wordDict
    if word in wordDict:
        wordDict[word] += weight
    else:
        wordDict[word] = weight


def loadReactions():
    print("loading reactions...")
    posLoad = []
    negLoad = []
    file = open("C:\\Users\\kajte\\PycharmProjects\\positiveReactions.txt", encoding='utf8')
    for line in file:
        posLoad.append(line.replace('\n', ''))
        posLoad[-1] = standardiseString(posLoad[-1])
    file.close()

    file = open("C:\\Users\\kajte\\PycharmProjects\\negativeReactions.txt", encoding='utf8')
    for line in file:
        negLoad.append(line.replace('\n', ''))
        negLoad[-1] = standardiseString(negLoad[-1])
    file.close()

    posProp = len(posLoad) / (len(posLoad) + len(negLoad))
    negProp = len(negLoad) / (len(posLoad) + len(negLoad))

    for i in posLoad:
        for j in i.split():
            addWordToDict(j, negProp)

    for i in negLoad:
        for j in i.split():
            addWordToDict(j, -posProp)


def saveNewReaction(message):
    global lastReactionWasPositive
    if clasificateMessage(message) >= 0:
        lastReactionWasPositive = True
        file = open("C:\\Users\\kajte\\PycharmProjects\\lastReaction.txt", "w", encoding='utf8')
        file.write('+')
        file.close()
        file = open("C:\\Users\\kajte\\PycharmProjects\\positiveReactions.txt", "a", encoding='utf8')
    else:
        lastReactionWasPositive = False
        file = open("C:\\Users\\kajte\\PycharmProjects\\lastReaction.txt", "w", encoding='utf8')
        file.write('-')
        file.close()
        file = open("C:\\Users\\kajte\\PycharmProjects\\negativeReactions.txt", "a", encoding='utf8')
    file.write(message)
    file.write("\n")
    file.close()


def loadLastReaction():
    print("loading last reaction...")
    global lastReactionWasPositive
    file = open("C:\\Users\\kajte\\PycharmProjects\\lastReaction.txt", encoding='utf8')
    x = ''
    for line in file:
        x = line
    file.close()
    if x == '+':
        lastReactionWasPositive = True
    else:
        lastReactionWasPositive = False


def changeLastSavedReaction():
    global lastReactionWasPositive
    print("changing last reaction...")
    posLoad = []
    negLoad = []
    file = open("C:\\Users\\kajte\\PycharmProjects\\positiveReactions.txt", encoding='utf8')
    for line in file:
        posLoad.append(line)
    file.close()

    file = open("C:\\Users\\kajte\\PycharmProjects\\negativeReactions.txt", encoding='utf8')
    for line in file:
        negLoad.append(line)
    file.close()

    file = open("C:\\Users\\kajte\\PycharmProjects\\positiveReactions.txt", 'w', encoding='utf8')
    for i in range(len(posLoad) - 1):
        file.write(posLoad[i])
    file.close()

    file = open("C:\\Users\\kajte\\PycharmProjects\\negativeReactions.txt", 'w', encoding='utf8')
    for i in range(len(negLoad) - 1):
        file.write(negLoad[i])
    file.close()

    if lastReactionWasPositive:
        lastReactionWasPositive = False
        file = open("C:\\Users\\kajte\\PycharmProjects\\negativeReactions.txt", 'a', encoding='utf8')
        file.write(negLoad[-1])
        file.write(posLoad[-1])
        file.close()
    else:
        lastReactionWasPositive = True
        file = open("C:\\Users\\kajte\\PycharmProjects\\positiveReactions.txt", 'a', encoding='utf8')
        file.write(posLoad[-1])
        file.write(negLoad[-1])
        file.close()

