from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup

import main_fanctions


class adresses(StatesGroup):
    wait_subject = State()


t = ["Учебные корпус", "Общежития"]


async def show_adress(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*t)
    await message.answer("Вы можете получить результаты работ по определенному предмеу или по по всем сразу",
                         reply_markup=keyboard)
    await adresses.wait_subject.set()


async def Ed_classes(message: types.Message, state: FSMContext):
    await message.answer("Кампус на Большой Семёновской:\n" +
                         "Учебные корпуса «А», «Б», «В», «Н», «НД» \n" +
                         "ст. м. «Электрозаводская», ул. Б. Семёновская, д. 38.")
    await message.answer("Учебный корпус на ст. м. «Автозаводская»:\n" +
                         "ст. м. «Автозаводская», ул. Автозаводская, д. 16.")
    await message.answer("Учебный корпус на ул. Павла Корчагина: \n" +
                         "ст. м. «ВДНХ», ул. Павла Корчагина, д. 22.")
    await message.answer("Учебный корпус на ул. Прянишникова: \n" +
                         "ул. Прянишникова, 2А \n" +
                         "Корпуса 1, 2")
    await message.answer("Учебный корпус на ул. Михалковская:\n" +
                         "ул. Михалковская, д. 7")
    await message.answer("Учебный корпус на ул. Садовая-Спасская:\n" +
                         "ст. м. «Сухаревская», ул. Садовая-Спасская, д. 6.")
    await message.answer("Учебный корпус на ст. м. «Авиамоторная»:\n" +
                         "ст. м. «Авиамоторная», ул. Лефортовский вал, д. 26.")

    await state.finish()
    await main_fanctions.show_main_functions(message)


async def Objaga_classes(message: types.Message, state: FSMContext):
    await message.answer("Общежитие № 1 \n"+"т. м. «Электрозаводская», ул. М. Семёновская, д. 12")
    await message.answer("Общежитие № 2 \n"+"ст. м. «Первомайская», ул. 7–я Парковая, д. 9/26.")
    await message.answer("Общежитие № 3 \n"+"ст. м. «Дубровка», ул. 1-я Дубровская, д. 16а.")
    await message.answer("Общежитие № 4 \n"+"ул. 800-летия Москвы, д. 28.")
    await message.answer("Общежитие № 5\n"+"ул. Михалковская, д. 7, корп. 3.")
    await message.answer("Общежитие № 6 \n"+"ул. Б. Галушкина, д. 9.")
    await message.answer("Общежитие № 7 \n"+"ул. Павла Корчагина, д. 20 А, к. 3.")
    await message.answer("Общежитие № 8 \n"+"Рижский проезд, д. 15, к. 2.")
    await message.answer("Общежитие № 9 \n"+"Рижский проезд, д. 15, к. 1")
    await message.answer("Общежитие № 10 \n"+"ст. м. «Сокол», 1-й Балтийский переулок, д. 6/21 корп. 3.")

    await state.finish()
    await main_fanctions.show_main_functions(message)


async def with_puree(message: types.Message, state: FSMContext):
    if message.text == "Учебные корпус":
        await Ed_classes(message, state)
    if message.text == "Общежития":
        await Objaga_classes(message, state)


def register_handlers_adress(dp: Dispatcher):
    #    dp.register_message_handler(show_adress, state=adresses.addres)
    dp.register_message_handler(with_puree, state=adresses.wait_subject)
