from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from threading import current_thread
import main_fanctions
import bot

t = ["bhj", "sdfgh"]


class Auth(StatesGroup):
    waiting_for_login = State()
    waiting_for_pass = State()
    show_functional_ = State()


async def auth_start(message: types.Message):
    await message.answer("Введите логин")
    await Auth.waiting_for_login.set()


async def login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text.lower())
    await Auth.waiting_for_pass.set()
    await message.answer("Введите пароль")


async def password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text.lower())
    await message.answer("Вы вошли в свою учетную записьавва "+str(message.chat.id))
    await message.answer("Вызовите команду /start_receive_messages, чтобы начал получать сообщения от админимтрации университета")

#    await bot.add_to_id_users_redy_for_messages(message.chat.id)
  #  await bot.add_to_id_users_redy_for_messages(message.chat.id)
#    bot.arr.append(message.chat.id)
#     bot.ab.arr = [1]
#     print(bot.arr[:],bot.ab.arr,current_thread())
    await state.finish()



# await Auth.show_functional_.set()


def register_handlers_login(dp: Dispatcher):
    dp.register_message_handler(auth_start, commands="log_in", state="*")
    dp.register_message_handler(login, state=Auth.waiting_for_login)
    dp.register_message_handler(password, state=Auth.waiting_for_pass)


