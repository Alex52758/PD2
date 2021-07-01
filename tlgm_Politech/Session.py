from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup

import main_fanctions


class session(StatesGroup):
    marks = State()
    wait_choose_subject = State()


t = [["Математика", "ИБ", "ИС"],
     ["ОС", "Физра", "Курсовые работы"]
     ,["все предметы"]]
marks_ = {"Математика":[13,1312,232,31], "ИБ":[13,1312,232,31], "ИС":[13,1312,232,31],
     "ОС":[13,1312,232,31], "Физра":[13,1312,232,31], "Курсовые работы":[13,1312,232,31]
     ,"все предметы":[13,1312,232,31]}


async def show_marks(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in t:
        keyboard.row(*i)
    await message.answer("Вы можете получить результаты сессии по определённому предмету или по всем сразу", reply_markup=keyboard)
    await session.wait_choose_subject.set()

async def choose_subject_for_marks(message: types.Message, state: FSMContext):
    print(message.text)
    for i in t:
        if message.text in i:
            await message.answer(marks_[message.text])
    await state.finish()
    await main_fanctions.show_main_functions(message)


def register_handlers_session(dp: Dispatcher):
    dp.register_message_handler(show_marks, state=session.marks)
    dp.register_message_handler(choose_subject_for_marks, state=session.wait_choose_subject)
