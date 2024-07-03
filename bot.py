from math import ceil
import logging
import asyncio
from db import BoT_DB
from keys import BOT_TOKEN, ADMINS
from aiogram.methods import DeleteWebhook
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class Exchage(CallbackData, prefix="adm"):
    currency: str
    num: int


class YuanState(StatesGroup):
    new_yuan_cur = State()


class DollarState(StatesGroup):
    new_dollar_cur = State()


class EuroState(StatesGroup):
    new_euro_cur = State()


bot_db = BoT_DB('/data/courses.db')
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command(commands=['admin']))
async def admin_command(msg: types.Message):
    if msg.from_user.id in ADMINS:
        yuan_btn = types.InlineKeyboardButton(text='Курс Юань', callback_data='yuan')
        dollar_btn = types.InlineKeyboardButton(text='Курс Доллара', callback_data='dollar')
        euro_btn = types.InlineKeyboardButton(text='Курс Евро', callback_data='euro')
        current_btn = types.InlineKeyboardButton(text='Текущие курсы', callback_data='current')
        keyboard = InlineKeyboardBuilder().add(yuan_btn).add(dollar_btn).add(euro_btn).add(current_btn)
        await msg.reply('Приветствую в панели админа', reply_markup=keyboard.as_markup())


@dp.callback_query(F.data == 'yuan')
async def process_callback_user(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer('Введите новый курс (отделяйте дробную часть точкой)')
    await state.set_state(YuanState.new_yuan_cur)


@dp.callback_query(F.data == 'current')
async def process_callback_user(callback_query: types.CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback_query.id)
    data = bot_db.get_current()
    await callback_query.message.answer(f"Текущий курс \n"
                                        f"Юань: {data[1]} \n"
                                        f"Доллар: {data[2]} \n"
                                        f"Евро: {data[3]} \n")


@dp.message(YuanState.new_yuan_cur)
async def password(message: types.Message, state: FSMContext):
    bot_db.update_yuan(float(message.text))
    await message.reply('Курс успешно изменен')
    await state.clear()


@dp.callback_query(F.data == 'dollar')
async def process_callback_user(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer('Введите новый курс (отделяйте дробную часть точкой)')
    await state.set_state(DollarState.new_dollar_cur)


@dp.message(DollarState.new_dollar_cur)
async def password(message: types.Message, state: FSMContext):
    bot_db.update_dollar(float(message.text))
    await message.reply('Курс успешно изменен')
    await state.clear()


@dp.callback_query(F.data == 'euro')
async def process_callback_user(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer('Введите новый курс (отделяйте дробную часть точкой)')
    await state.set_state(EuroState.new_euro_cur)


@dp.message(EuroState.new_euro_cur)
async def password(message: types.Message, state: FSMContext):
    bot_db.update_euro(float(message.text))
    await message.reply('Курс успешно изменен')
    await state.clear()


@dp.message()
async def echo_message(msg: types.Message):
    if msg.text.isdigit():
        yuan_btn = types.InlineKeyboardButton(text='ЮАНЬ', callback_data=Exchage(currency='yuan', num=int(msg.text)).pack())
        dollar_btn = types.InlineKeyboardButton(text='ДОЛЛАР', callback_data=Exchage(currency='dollar', num=int(msg.text)).pack())
        euro_btn = types.InlineKeyboardButton(text='ЕВРО', callback_data=Exchage(currency='euro', num=int(msg.text)).pack())
        exchange_markup = InlineKeyboardBuilder().add(yuan_btn).add(dollar_btn).add(euro_btn)
        await msg.reply('Выберете валюту в которую хотите перевести', reply_markup=exchange_markup.as_markup())
    try:
        num_list = [int(i) for i in msg.text.split()]
        if len(num_list) > 1:
            await msg.reply(f'Сумма цифр {sum(num_list)}')
            yuan_btn = types.InlineKeyboardButton(text='ЮАНЬ',
                                                  callback_data=Exchage(currency='yuan', num=sum(num_list)).pack())
            dollar_btn = types.InlineKeyboardButton(text='ДОЛЛАР',
                                                    callback_data=Exchage(currency='dollar', num=sum(num_list)).pack())
            euro_btn = types.InlineKeyboardButton(text='ЕВРО',
                                                  callback_data=Exchage(currency='euro', num=sum(num_list)).pack())
            exchange_markup = InlineKeyboardBuilder().add(yuan_btn).add(dollar_btn).add(euro_btn)
            await msg.reply('Выберете валюту в которую хотите перевести', reply_markup=exchange_markup.as_markup())
    except Exception:
        pass


@dp.callback_query(Exchage.filter(F.currency == 'yuan'))
async def process_callback_user(callback_query: types.CallbackQuery, bot: Bot, callback_data: Exchage):
    await bot.answer_callback_query(callback_query.id)
    cur = bot_db.get_yuan()[0]
    price = ceil(callback_data.num / float(cur))
    await callback_query.message.answer(f'{price}')


@dp.callback_query(Exchage.filter(F.currency == 'dollar'))
async def process_callback_user(callback_query: types.CallbackQuery, bot: Bot, callback_data: Exchage):
    await bot.answer_callback_query(callback_query.id)
    cur = bot_db.get_dollar()[0]
    price = ceil(callback_data.num / float(cur))
    await callback_query.message.answer(f'{price}')


@dp.callback_query(Exchage.filter(F.currency == 'euro'))
async def process_callback_user(callback_query: types.CallbackQuery, bot: Bot, callback_data: Exchage):
    await bot.answer_callback_query(callback_query.id)
    cur = bot_db.get_euro()[0]
    price = ceil(callback_data.num / float(cur))
    await callback_query.message.answer(f'{price}')




async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if '__main__' == __name__:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
