from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = " "
health_bot = Bot(token=api)
dp = Dispatcher(health_bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb.add(button_1)
kb.add(button_2)

kb_in = InlineKeyboardMarkup()
butt_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
butt_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_in.add(butt_1)
kb_in.add(butt_2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора(М): '
                              '10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(ages=int(message.text))
    await message.answer('Введите свой рост в см:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growths=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state, data=None):
    await state.update_data(weights=int(message.text))
    data = await state.get_data()
    calories = 10 * data['weights'] + 6.25 * data['growths'] - 5 * data['ages'] + 5
    await message.answer(f'Ваша ежедневная норма каллорий - {calories}')
    await state.finish()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию.', reply_markup=kb_in)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)