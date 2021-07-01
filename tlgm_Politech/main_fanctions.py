import Adress
import Education_Plan
import Session
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import bot


class main_functions(StatesGroup):
    show_functional = State()
    show_person_data = State()
    show_schedule = State()
    wait =State()


t = [["Адреса", "Телефоны", "Сессия"],
     ["План обучения", "Аттестация", "Курсовые работы"],
     ["Отчисление", "Перевод на курс", "Академический отпуск"],
     ["Вебинары", "Справки", "Оплата за обучение"],
     ["Текщая аттестация", "личный кабинет", "Миграционный учет"]]


async def show_main_functions(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in t:
        keyboard.row(*i)
    await message.answer("Выберите в меню тему справочной информации:", reply_markup=keyboard)
    print("+-",bot.ab.arr)
    await main_functions.wait.set()



#  await main_functions.show_functional.set()
#   await state.finish()


async def main_functiona_start(message: types.Message):
    await message.answer("Введите лfxcbогин")


# await State.set("*")
#    await main_functions.show_.set()
async def with_puree(message: types.Message, state: FSMContext):
    if message.text == "Сессия":
     #   await Session.session.marks.set()
        await state.finish()
        await Session.show_marks(message)
    if message.text == "Текщая аттеста":
     #   await Session.session.marks.set()
        await state.finish()
        await Session.show_marks(message)
    if message.text == "Адреса":
        await state.finish()
        await Adress.show_adress(message)
    if message.text == "Телефоны":
        await message.answer("Многофункциональный центр: +7 (495) 223-05-23")
        await message.answer("Отделение «На Большой Семёновской»: +7 (495) 223-05-23 доб.1375, 121")
        await message.answer("Отделение «На Автозаводской»: +7 (495) 223-05-23 доб. 2257, 2256, 2285")
        await message.answer("Отделение «На Павла Корчагина»: +7 (495) 223-05-23 доб. 3110, 3044, 3230")
        await message.answer("Отделение «На Прянишникова»: +7 (495) 223-05-23 доб. 4052, 4055, 4057")
        await message.answer("Управление студенческим городком: +7(495) 223-05-23 доб. 1284")
        await message.answer("Приёмная комиссия:")
        await message.answer("+7 (495) 223-05-23")
        await message.answer("8 (800) 550-91-4")
    if message.text == "План обучения":
        await Education_Plan.start_(message)


async def show_person_data(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text.lower())
    await Auth.waiting_for_pass.set()
    await message.answer("Введите пароль")


async def show_schedule(message: types.Message, state: FSMContext):
    await message.answer("Вы вошли в свою учетную записьавва")


def register_handlers_main_functional(dp: Dispatcher):
    dp.register_message_handler(main_functiona_start, commands="main_functiona_start", state="*")
    dp.register_message_handler(show_main_functions, commands="show_all", state="*")
    dp.register_message_handler(show_person_data, commands="show_person_data", state="*")
    dp.register_message_handler(show_schedule, commands="show_schedule", state="*")
    dp.register_message_handler(with_puree, state = main_functions.wait)
