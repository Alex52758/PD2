import asyncio
import logging
import threading
import time
import random
from threading import current_thread
from multiprocessing import Process, Value, Array
import Auth
import Session
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Adress import register_handlers_adress
from Education_Plan import register_handlers_Education_Plan
import main_fanctions

from common import register_handlers_common
from Session import register_handlers_session
import requests


class data_arr:
    arr = []
    arr_num_person = []


num = Value('d', 0.0)
arr = Array('i', range(1, 10))
ab = data_arr()
# num_last_message = -1

lock = threading.Lock()

id_users_redy_for_messages = Array('i', [])
logger = logging.getLogger(__name__)


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


async def add_to_id_users_redy_for_messages(new_id):
    arr[0] = new_id
    print("()", arr[:])
    return new_id


async def run(i, message):
    await bot.send_message(i, message)


async def message_checking(num, a):
    print('собираю результат проверки', current_thread())
    num_last_message = -1
    num_last_message_for_person = -1
    resp = requests.get('https://new.mospolytech.ru/upload/files/mfc-blank/На%20выход%20из%20академического%20отпуска.pdf')
    print(resp)
    while True:
        await asyncio.sleep(3)
        #   with lock:
        #       print("+ ",arr[:],ab.arr,num)
        # #  print(get_to_id_users_redy_for_messages(),current_thread())
        response = requests.post('http://127.0.0.1:5000/newMessage', json={'num_last_message': num_last_message})
        response_persons = requests.post('http://127.0.0.1:5000/newMessageForPersons', json={})
        if response_persons is not None:
            print("! ", response_persons.json().get('ans'))
            for i in response_persons.json().get('ans'):

                for j in range(len(ab.arr)):
                    if ab.arr[j] == i[0]:
                        print("- ", i[0], " ", ab.arr_num_person[j], " ", i[1])
                        if ab.arr_num_person[j] < i[1]:
                            response_persons = requests.post('http://127.0.0.1:5000/getMessagePerson',
                                                             json={'person_id': i[0],
                                                                   'num_message_from': ab.arr_num_person[j],
                                                                 'num_message_to': i[1]})
                            print(response_persons.json().get('last'))
                            await bot.send_message(i[0], response_persons.json().get('last'))
                            ab.arr_num_person[j] = i[1]
        if response is not None:
            # print("current uploaded message : " + str(num_last_message) + " current  message : " + str(
            #    response.json().get('last')) + " need to upload " + str(
            #   int(response.json().get('last')) - num_last_message) + " messages")

            if int(response.json().get('last')) > num_last_message:
                for j in range(num_last_message, int(response.json().get('last'))):
                    num_last_message += 1
                    message = requests.post('http://127.0.0.1:5000/getMessage', json={'num_message': num_last_message})

                    #         print("- message", message.json().get('last'), id_users_redy_for_messages)
                    with lock:
                        for i in ab.arr:
                            print("send to user with ", i, "message" + str(message.json().get('last')))
                            # loop = get_or_create_eventloop()
                            #
                            # send_fut = asyncio.run_coroutine_threadsafe(run(i,message.json().get('last')),loop)
                            # # wait for the coroutine to finish
                            # send_fut.result()
                            await bot.send_message(i, message.json().get('last'))


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/drinks", description="Заказать напитки"),
        BotCommand(command="/log_in", description="Авторизироваться"),
        BotCommand(command="/log_out", description="выйти из учетной записи")
    ]
    await bot.set_my_commands(commands)


bot = Bot(token="1724700687:AAE3F-hlj7SmbLvsjbsaRTFjd6-zbM0Gbc4")
dp = Dispatcher(bot, storage=MemoryStorage())


def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]


def worker(number):
    sleep = random.randrange(1, 10)
    time.sleep(sleep)
    print("I am Worker {}, I slept for {} seconds".format(number, sleep))


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Парсинг файла конфигурации
    # config = load_config("config/bot.ini")
    # Объявление и инициализация объектов бота и диспетчера
    # Регистрация хэндлеров
    register_handlers_common(dp, 987654321)

    main_fanctions.register_handlers_main_functional(dp)
    Auth.register_handlers_login(dp)
    dp.register_message_handler(main_fanctions.main_functiona_start, state=Auth.Auth.show_functional_)
    register_handlers_session(dp)
    register_handlers_Education_Plan(dp)
    register_handlers_adress(dp)
    # Установка команд бота
    await set_commands(bot)
    # asyncio.create_task(message_checking())
    # asyncio.create_task(run(message.json().get('last')))

    # t = multiprocessing.Process(target=message_checking,args=(id_users_redy_for_messages))
    # t.start()
    # t.join()

    # p = threading.Thread(target=message_checking, args=(num, arr,))
    # p.start()
    # #    p.join()
    #     threads.append(t)
    #     t.start()
    #     # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    asyncio.ensure_future(dp.start_polling())

    # await dp.start_polling()


# @dp.message_handler(commands=["log_in"])
# async def log_in_command(message: types.Message):
#     await Auth.auth_start(message)


@dp.message_handler(commands=['start_receive_messages'])
async def with_puree(message: types.Message):
    ab.arr.append(message.chat.id)
    ab.arr_num_person.append(0)
    print("0 ", ab.arr)
    response = requests.post('http://127.0.0.1:5000/addPerson', json={'person_id': message.chat.id})
    await main_fanctions.show_main_functions(message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main())
    asyncio.ensure_future(message_checking(num, arr))
    # asyncio.run(main())
    loop.run_forever()
