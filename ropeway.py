import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import json

with open("secret", "r") as f:
    api_key = f.readline()[:-1]

with open("dialogs.json", "r") as f:
    messages = json.load(f)

print("<...ropeway.initialized...>")
vk = vk_api.VkApi(token=api_key)
print("<...connecting...>")
vk._auth_token()
print("<...connected.succesfully...>\n<...longpoll.initializing...>")
longpoll = VkLongPoll(vk)
print("<...longpoll.initialized...>\n<...ropeway.is.running...>\n<...enjoy...>")

def on_registration(current_occupation, people_amount):
    return messages["on_registration"].replace("${1}", str(current_occupation)).replace("${2}", str(people_amount))

def already_registered(current_occupation, people_amount):
    return messages["already_registered"].replace("${1}", str(current_occupation)).replace("${2}", str(people_amount))

PEOPLE_AMOUNT = 3
cabe = []

def write_msg(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s, 'random_id':random.randint(0, 100)})

def add_user_to_cabe(u_id):
    if u_id in cabe:
        write_msg(u_id, already_registered(len(cabe), PEOPLE_AMOUNT))
    else:
        cabe.append(u_id)
        if len(cabe) != PEOPLE_AMOUNT:
            write_msg(u_id, on_registration(len(cabe), PEOPLE_AMOUNT))
        else:
            for uid in cabe:
                write_msg(uid, messages["start"])
            cabe.clear()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        valid_message = False
        for pattern in messages["enter_patterns"]:
            if pattern in event.text:
                add_user_to_cabe(event.user_id)
                valid_message = True
                break
        if not valid_message:
            write_msg(event.user_id, messages["error"])

