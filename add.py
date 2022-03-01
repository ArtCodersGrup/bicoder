from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import os
import sys
import csv
import traceback
import time
import random

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

print (re+"╔╦╗┌─┐┬  ┌─┐╔═╗  ╔═╗┌┬┐┌┬┐┌─┐┬─┐")
print (gr+" ║ ├┤ │  ├┤ ║ ╦  ╠═╣ ││ ││├┤ ├┬┘")
print (re+" ╩ └─┘┴─┘└─┘╚═╝  ╩ ╩─┴┘─┴┘└─┘┴└─")

print (cy+"version : 0.0.1")
print (cy+"Loading")
print (cy+"Dastur ishga tushmoqda")

print (re+"NOTE :")
print ("1. Telegramdagi gruxlarga 200 ta odam qoshsa boladi")
print ("2. Guruxga odam qoshganingizdan song 15-30 daqiqa kutasiz")
print ("3. Guruxda siz Admin bolishingiz kerak")

phone = '+998903430422'

try:
    api_id = 16220734
    api_hash = '6b03083238042a2d9345483104a71263'
    username = '@bi_coder'

    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    print(re+"[!] run python setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('[+] Kodni yozing: '))

users = []
with open(r"members.csv", encoding='UTF-8') as f:  #Enter your file name
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chats)
    except:
        continue

print(gr+'Odam qoshish uchun guruxni tanlang'+cy)
i = 0
for group in groups:
    print(str(i) + '- ' + group)
    i += 1

g_index = input(gr+"Sonni kiriting: "+re)
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = int(input(gr+"Username orqali qoshish uchun 1 ni kiriting, ID orqali qoshmoqchi bolsangiz 2 ni yozing: "+cy))

n = 0

for user in users:
    n += 1
    if n % 80 == 0:
        pass
    try:
        print("Qoshilmoqda {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Xato! Boshqattan urinib koring")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("60-180 Sekund kuting...")
        time.sleep(random.randrange(0, 5))
    except PeerFloodError:
        print("Telegramdan xatolik oldik, Iltimos 2-3 soattan song urib koring...")
        print("Kuting seconds")
    except UserPrivacyRestrictedError:
        print("Foydalanuvchini guruxga qoshib bolmadi. Tushurib kettik.")
        print("5 sekund kuting...")
        time.sleep(random.randrange(0, 5))
    except:
        traceback.print_exc()
        print("Unexpected Error, Xatolik")
        continue
