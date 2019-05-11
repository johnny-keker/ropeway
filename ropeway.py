import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import json

with open("secret", "r") as f:
    api_key = f.readline()[:-1]

with open("dialogs.json", "r") as f:
    messages = json.load(f)

with open("state.json", "r") as f:
    cabe = json.load(f)

print("<...ropeway.initialized...>")
vk = vk_api.VkApi(token=api_key)
print("<...connecting...>")
vk._auth_token()
print("<...connected.succesfully...>\n<...longpoll.initializing...>")
longpoll = VkLongPoll(vk)
print("<...longpoll.initialized...>\n<...ropeway.is.running...>\n<...enjoy...>")

def on_registration(current_occupation, people_amount):
    return messages["on_registration"].format(str(current_occupation), str(people_amount))

def already_registered(current_occupation, people_amount):
    return messages["already_registered"].format(str(current_occupation), str(people_amount))

PEOPLE_AMOUNT = 3

def write_msg(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s, 'random_id':random.randint(0, 100)})

def save_state():
    with open('state.json', 'w') as f:
        json.dump(cabe, f)

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

def valid_message(text):
    for pattern in messages["enter_patterns"]:
        if pattern in text.lower():
            return True
    return False

def is_end_message(u_id, text):
    return u_id in messages["admins"] and text.lower() in messages["stop_words"]

def main_cycle():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if is_end_message(event.user_id, event.text):
                print("<...enough.for.today...>")
                save_state()
                for uid in cabe:
                    write_msg(uid, messages["on_closing"])
                return
            elif valid_message(event.text):
                add_user_to_cabe(event.user_id)
            else:
                write_msg(event.user_id, messages["error"])
main_cycle()
