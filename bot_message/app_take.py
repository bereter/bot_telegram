from telethon import functions, types
from conf import name_video
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from time import sleep
import asyncio


# Функция для рассылки сообщения по геолокации
async def geo_local(client, geo1, geo2):
    message = 'https://t.me/+gIa3WG65jOpjY2Zi'
    result = await client(functions.contacts.GetLocatedRequest(
        geo_point=types.InputGeoPoint(
            lat=geo1,
            long=geo2,
            accuracy_radius=5)))

    if name_video:
        for user in result.users:
            await asyncio.sleep(1)
            await client.send_file(user, name_video, caption=f'{message}')
            await asyncio.sleep(1)
    else:
        for user in result.users:
            await asyncio.sleep(1)
            await client.send_message(user, message)
            await asyncio.sleep(1)


# Функция для добавления пользователей групп в контакты
async def add_contact(url_group, client):
    try:
        channel = await client.get_entity(url_group)
        OFFSET_USER = 0  # номер участника, с которого начинается считывание
        LIMIT_USER = 200  # максимальное число записей, передаваемых за один раз, но не более 200
        ALL_PARTICIPANTS = []  # список всех участников канала
        FILTER_USER = ChannelParticipantsSearch('')  # фильтр для определенных пользователей
        while True:
            participants = await client(GetParticipantsRequest(channel,
                                                               FILTER_USER, OFFSET_USER, LIMIT_USER,
                                                               hash=0))
            if not participants.users:
                break
            ALL_PARTICIPANTS.extend(participants.users)
            OFFSET_USER += len(participants.users)
            if len(participants.users) == len(ALL_PARTICIPANTS):
                break

        for users in ALL_PARTICIPANTS:
            user = await client.get_entity(users)
            await client(functions.contacts.AddContactRequest(id=user.id, first_name=f'{user.first_name}',
                                                              last_name=f'{user.last_name}', phone=f'{user.phone}'))

    except Exception as e:
        print(e)


# Функция по отправке сообщения всем контактам
async def sending_message_contacts(client):
    message = input('Введите сообщение для отправки сообщения контактам: ')
    contacts = await client(functions.contacts.GetContactsRequest(hash=0))
    for contact in contacts.users:
        user = await client.get_entity(contact)
        await client.send_message(user, message)
        sleep(3)


# Функция по отправки сообщения участникам группы
async def sending_message_group(url_group, client):
    try:
        message = input('Введите текст для отправки сообщения участникам группы: ')
        channel = await client.get_entity(url_group)
        OFFSET_USER = 0  # номер участника, с которого начинается считывание
        LIMIT_USER = 200  # максимальное число записей, передаваемых за один раз, но не более 200
        ALL_PARTICIPANTS = []  # список всех участников канала
        FILTER_USER = ChannelParticipantsSearch('')  # фильтр для определенных пользователей
        while True:
            participants = await client(GetParticipantsRequest(channel,
                                                               FILTER_USER, OFFSET_USER, LIMIT_USER,
                                                               hash=0))
            if not participants.users:
                break
            ALL_PARTICIPANTS.extend(participants.users)
            OFFSET_USER += len(participants.users)
            if len(participants.users) == len(ALL_PARTICIPANTS):
                break
        for users in ALL_PARTICIPANTS:
            user = await client.get_entity(users)
            await client.send_message(user, message)
            sleep(5)
    except Exception as e:
        print(e)
