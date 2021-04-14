def on_message(message):
    msgs = message.split(';')
    print(str(msgs[0]))
    return str(msgs[0])

