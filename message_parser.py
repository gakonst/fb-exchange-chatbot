HELP = ["help"]
ORDERS = ["buy", "sell"]
GREETINGS = ["hello", "hi", "get started", "hey", "whatsup", "what's up"]
EXCHANGES = ["gdax", "bittrex"]
TRADE = ['trade']
BULLISH_PHRASES = ["moon", "9k", "rise", "bullish"]
HODL = ["hodl", "hold"]
PRICE_RELATED = ["price", "bubble"]

def word_in_list(msg, lst):
    return any(phrase in msg for phrase in lst)

def process_message(message_payload, message_type):
    responses = []
    
    if message_payload.lower() in GREETINGS:
        responses.append('''Welcome to the crypto chatbot!
Available commands: help, trade
Ask me about: when we get to the moon, bitcoin's over 9k price, if we are bullish etc. I'll do my best.''')

    if word_in_list(message_payload.lower(), HODL):
        responses.append("Hodl well my man. Do your own research and invest wisely.")

    if word_in_list(message_payload.lower(), BULLISH_PHRASES):
        responses.append("Hodl well my man. Do your own research and invest wisely.")

    if word_in_list(message_payload.lower(), PRICE_RELATED):
        responses.append("I do not have that feature yet. Check http://coinmarketcap.com :D")


    if message_payload.lower() in TRADE:
        responses.append(dict(
                text="On which exchange do you want to trade?",
                quick_replies=[
                    dict(label="Bittrex", value="bittrex"),
                    dict(label="GDAX", value="gdax"),
                ]
            ))


    if message_payload.lower() in HELP:
        responses.append("Seems like you need some help!")
        responses.append(dict(
                text="What do you want to learn about?",
                quick_replies=[
                    dict(label="Bitcoin", value="btc"),
                    dict(label="Ethereum", value="eth"),
                ]
            ))

    if message_type == "quick_reply":
        if message_payload == "btc":
            responses.append("Bitcoin is ...")

        if message_payload == "eth":
            responses.append("Ethereum is ...")

        if message_payload in EXCHANGES:
            responses.append(dict(
                    text='Very well. Do you want to BUY or SELL?',
                    quick_replies=[
                        dict(label="Buy!", value="buy"),
                        dict(label="Sell!", value="sell"),
                    ]
                ))
        if message_payload.lower() in ORDERS:
            responses.append('You choise {}'.format(message_payload))

    return responses
