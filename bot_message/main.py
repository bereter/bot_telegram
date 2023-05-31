from conf import send_message_url_groups, add_user_url_groups, geolocations, accounts
from telethon import TelegramClient
from app_take import add_contact, sending_message_contacts, sending_message_group, geo_local
from telethon import functions


def main():
    for i in accounts:
        with TelegramClient(i[0], i[1], i[2], system_version="4.16.30-vxCUSTOM") as client:
            client.loop.run_until_complete(client.get_me())

    count = 0
    while len(accounts) >= count + 1:
        try:
            client = TelegramClient(accounts[count][0],
                                    accounts[count][1],
                                    accounts[count][2],
                                    system_version="4.16.30-vxCUSTOM")

            async def start():
                global command
                while True:
                    command = input(
                        ' Для добавления пользователей из групп в контакты введите - 1 \n Для отправки сообщения всем '
                        'контактам введите - 2 \n Для отправки сообщения всем подписчикам чата введите - 3 \n Для '
                        'рассылки по геолокации введите - 4 \n Для удаления контактов введите - 5 \n Для выхода из '
                        'программы введите - 6 \n Введите число: ')

                    if command == '1':
                        for group in add_user_url_groups:
                            await add_contact(group, client)
                    elif command == '2':
                        await sending_message_contacts(client)
                    elif command == '3':
                        for group in send_message_url_groups:
                            await sending_message_group(group, client)
                    elif command == '4':
                        for geo in geolocations:
                            await geo_local(client, geo[0], geo[1])
                    elif command == '5':
                        contacts = await client(functions.contacts.GetContactsRequest(hash=0))
                        username = []
                        for user in contacts.users:
                            username.append(user.id)
                        await client(functions.contacts.DeleteContactsRequest(id=username))

                    elif command == '6':
                        break
                    else:
                        print('Введено не правильное значение!')

            with client:
                client.loop.run_until_complete(start())

        except Exception as e:
            print(e)
            count += 1
        finally:
            if command == '6':
                break


if __name__ == '__main__':
    main()
