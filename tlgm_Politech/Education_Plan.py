from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

import main_fanctions


class Education_Plan(StatesGroup):
    wait_choose_group = State()


marks_ = {"Математика": [13, 1312, 232, 31], "ИБ": [13, 1312, 232, 31], "ИС": [13, 1312, 232, 31],
          "ОС": [13, 1312, 232, 31], "Физра": [13, 1312, 232, 31], "Курсовые работы": [13, 1312, 232, 31]
    , "все предметы": [13, 1312, 232, 31]}


async def start_(message: types.Message):
    await message.answer("Введите номер своей группы, чтобы получить план обучения", reply_markup = ReplyKeyboardRemove())
    await Education_Plan.wait_choose_group.set()


async def choose_group(message: types.Message, state: FSMContext):
    await message.answer("вы выбрали план обучения для группы " + message.text)
    await state.finish()
    await main_fanctions.show_main_functions(message)


def register_handlers_Education_Plan(dp: Dispatcher):
    dp.register_message_handler(choose_group, state=Education_Plan.wait_choose_group)
