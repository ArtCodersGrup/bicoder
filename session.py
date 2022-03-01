import json
#import sqlite3 as sq
import csv
from telethon.sync import TelegramClient


# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

# Присваиваем значения внутренним переменным
api_id = 16220734
api_hash = '6b03083238042a2d9345483104a71263'
username = '@bi_coder'



client = TelegramClient(username, api_id, api_hash)

client.start()


async def dump_all_participants(channel):
    """Записывает json-файл с информацией о всех участниках канала/чата"""
    offset_user = 0    # номер участника, с которого начинается считывание
    limit_user = 100   # максимальное число записей, передаваемых за один раз

    all_participants = []   # список всех участников канала
    filter_user = ChannelParticipantsSearch('')

    while True:
        participants = await client(GetParticipantsRequest(channel,
            filter_user, offset_user, limit_user, hash=0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset_user += len(participants.users)

    all_users_details = []   # список словарей с интересующими параметрами участников канала

    for participant in all_participants:
        with open("members3.csv", "w", encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            #writer.writerow([participant.username, participant.id, participant.first_name, 'group', 'group id'])
            writer.writerow(participant)

async def dump_all_messages(channel):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0    # номер записи, с которой начинается считывание
    limit_msg = 100   # максимальное число записей, передаваемых за один раз

    all_messages = []   # список всех сообщений
    total_messages = 0
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    class DateTimeEncoder(json.JSONEncoder):
        '''Класс для сериализации записи дат в JSON'''
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, add_offset=0,
			limit=limit_msg, max_id=0, min_id=0,
			hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open('channel_messages.json', 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main():
    url = input("Введите ссылку на канал или чат: ")
    channel = await client.get_entity(url)
    await dump_all_participants(channel)
    await dump_all_messages(channel)


with client:
    client.loop.run_until_complete(main())
