from server.core import storage


def on_message(message):
    msgs = message.split(';')
    if msgs[0] == 'get_user_data':
        user_id = msgs[1]
        type_name = msgs[2]
        return get_user_data(user_id, type_name)
    elif msgs[0] == 'save_user_data':
        user_id = msgs[1]
        type_name = msgs[2]
        value = msgs[3]
        return save_user_data(user_id, type_name, value)
    else:
        return ('wrong type')


def get_user_data(user_id, type_name):
    return storage.read_data(user_id, type_name)


def save_user_data(user_id, type_name, value):
    storage.save_data(user_id, type_name, value)
    return 'Data Saved!'
