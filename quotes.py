import random

quotes = []


def addQuote(data):
    print("addQuote")
    global quotes
    data = data.replace("!dodajCytat ", "")
    data = data.replace("!dodajcytat ", "")
    quote = data[:data.find('-') - 1]
    author = data[data.find('-') + 2:]

    quotes.append(quote)
    quotes.append(author)

    file = open("C:\\Users\\kajte\\PycharmProjects\\quotes.txt", "a", encoding='utf8')
    file.write(quote + '\n')
    file.write(author + '\n')
    file.close()


def loadQuotes():
    print("loading quotes...")
    global quotes
    quotes = []
    file = open("C:\\Users\\kajte\\PycharmProjects\\quotes.txt", encoding='utf8')
    for line in file:
        quotes.append(line.replace('\n', ''))
    file.close()


def sendQuote(browser):
    x = random.randint(0, len(quotes) - 1)
    if x % 2 == 1:
        x -= 1
    quote = "\"" + quotes[x] + "\""
    author = "-" + quotes[x + 1]
    sendMessage(browser, quote)
    sendMessage(browser, author)


from messenger import sendMessage
