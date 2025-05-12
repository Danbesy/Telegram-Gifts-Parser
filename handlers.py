
#   ____                        _____                    _                          
#  |  _ \               ____   |  __ \                  | |                         
#  | |_) |  _   _      / __ \  | |  | |   __ _   _ __   | |__     ___   ___   _   _ 
#  |  _ <  | | | |    / / _` | | |  | |  / _` | | '_ \  | '_ \   / _ \ / __| | | | |
#  | |_) | | |_| |   | | (_| | | |__| | | (_| | | | | | | |_) | |  __/ \__ \ | |_| |
#  |____/   \__, |    \ \__,_| |_____/   \__,_| |_| |_| |_.__/   \___| |___/  \__, |
#            __/ |     \____/                                                  __/ |
#           |___/                                                             |___/ 
#
# Telegram - https://t.me/danbesy
# Telegram Channel - https://t.me/Danbesy_Dev
# Telegram Bio - https://Danbesy_Bio
# GitHub - https://github.com/Danbesy

import logging
import asyncio
import re
import os
import random
import aiohttp
import ssl
import certifi
import tempfile
import keyboards as kb
from config import *
from db import *
from datetime import *
from bs4 import BeautifulSoup
from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

bot = Bot(TOKEN)

router = Router()

logging.basicConfig(level=logging.INFO)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):

    await state.clear()

    user_id = message.from_user.id
    user_link = f'tg://user?id={user_id}'

    if user_id in ADMINS:
        await message.answer(
            f"<b>👋 Приветствую, </b><a href='{user_link}'>{message.from_user.full_name}</a> !\n\n"
            "<b>Добро пожаловать в мир коллекционных подарков Telegram! 🎁</b>\n\n"
            "<b>Мы поможем вам найти редкие и уникальные модели в личных коллекциях пользователей. 🚀</b>\n\n"
            "<b>Откройте для себя новые возможности и легко находите то, что ищете! 🌟</b>\n\n"
            "<b>Используйте кнопки ниже, чтобы начать. 💼</b>\n\n",
            parse_mode="HTML",
            reply_markup=kb.main_admin)  
    else:
        await message.answer(
            f"<b>👋 Приветствую, </b><a href='{user_link}'>{message.from_user.full_name}</a> !\n\n"
            "<b>Добро пожаловать в мир коллекционных подарков Telegram! 🎁</b>\n\n"
            "<b>Мы поможем вам найти редкие и уникальные модели в личных коллекциях пользователей. 🚀</b>\n\n"
            "<b>Откройте для себя новые возможности и легко находите то, что ищете! 🌟</b>\n\n"
            "<b>Используйте кнопки ниже, чтобы начать. 💼</b>\n\n",
            parse_mode="HTML",
            reply_markup=None)

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_button(callback: CallbackQuery, state: FSMContext):

    await state.clear()

    user_id = callback.from_user.id
    user_link = f'tg://user?id={user_id}'

    if user_id in ADMINS:
        await callback.message.answer(
            f"<b>👋 Приветствую, </b><a href='{user_link}'>{callback.from_user.full_name}</a> !\n\n"
            "<b>Добро пожаловать в мир коллекционных подарков Telegram! 🎁</b>\n\n"
            "<b>Мы поможем вам найти редкие и уникальные модели в личных коллекциях пользователей. 🚀</b>\n\n"
            "<b>Откройте для себя новые возможности и легко находите то, что ищете! 🌟</b>\n\n"
            "<b>Используйте кнопки ниже, чтобы начать. 💼</b>\n\n",
            parse_mode="HTML",
            reply_markup=kb.main_admin)  
    else:
        await callback.message.answer(
            f"<b>👋 Приветствую, </b><a href='{user_link}'>{callback.from_user.full_name}</a> !\n\n"
            "<b>Добро пожаловать в мир коллекционных подарков Telegram! 🎁</b>\n\n"
            "<b>Мы поможем вам найти редкие и уникальные модели в личных коллекциях пользователей. 🚀</b>\n\n"
            "<b>Откройте для себя новые возможности и легко находите то, что ищете! 🌟</b>\n\n"
            "<b>Используйте кнопки ниже, чтобы начать. 💼</b>\n\n",
            parse_mode="HTML",
            reply_markup=kb.main)

class GiftSearch(StatesGroup):
    waiting_for_gift_name = State()
    waiting_for_search_method = State()
    waiting_for_model_name = State()
    waiting_for_backdrop_name = State()
    waiting_for_model_and_backdrop_name = State()
    waiting_for_symbol_name = State()
    waiting_for_number = State()
    waiting_for_confirm = State()

@router.callback_query(F.data == "gifts_search")
async def gifts_search_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "<b>🎁 Выберите подарок для поиска, который вас интересует!</b>\n\n"
        "<b>✨ Доступные варианты:\n</b>"
        "<b>├ <a href='https://t.me/addemoji/AstralShardSkins'>Astral Shard 🌌</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/BDayCandleSkins'>B-Day Candle 🕯️</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/BerryBoxSkins'>Berry Box 🍓</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/BunnyMuffinSkins'>Bunny Muffin 🧁</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/CandyCaneSkins'>Candy Cane 🍬</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/CookieHeartSkins'>Cookie Heart 🍪</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/CrystalBallSkins'>Crystal Ball 🔮</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/DeskCalendarSkins'>Desk Calendar 📅</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/DiamondRingSkins'>Diamond Ring 💍</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/DurovsCapSkins'>Durov’s Cap 🧢</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/ElectricSkullSkins'>Electric Skull 💀</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/EternalCandleSkins'>Eternal Candle 🕯️</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/EternalRoseSkins'>Eternal Rose 🌹</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/EvilEyeSkins'>Evil Eye 👁️</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/FlyingBroomSkins'>Flying Broom 🧹</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/GenieLampSkins'>Genie Lamp 🛋️</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/GingerCookieSkins'>Ginger Cookie 🍪</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/HangingStarSkins'>Hanging Star ⭐</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/HexPotSkins'>Hex Pot 🪴</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/HomemadeCakeSkins'>Homemade Cake 🍰</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/HypnoLollipopSkins'>Hypno Lollipop 🍭</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/IonGemSkins'>Ion Gem 💎</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/JackInTheBoxSkins'>Jack-in-the-Box 📦</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/JellyBunnySkins'>Jelly Bunny 🐰</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/JesterHatSkins'>Jester Hat 🎩</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/JingleBellsSkins'>Jingle Bells 🔔</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/KissedFrogSkins'>Kissed Frog 🐸</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/LolPopSkins'>Lol Pop 🍭</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/LootBagSkins'>Loot Bag 🎒</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/LoveCandleSkins'>Love Candle 🕯️</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/LovePotionSkins'>Love Potion 💖</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/LunarSnakeSkins'>Lunar Snake 🐍</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/MadPumpkinSkins'>Mad Pumpkin 🎃</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/MagicPotionSkins'>Magic Potion 🍷</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/MiniOscarSkins'>Mini Oscar 🏆</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/NekoHelmetSkins'>Neko Helmet 🐾</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/PartySparklerSkins'>Party Sparkler 🎇</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/PerfumeBottleSkins'>Perfume Bottle 💐</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/PlushPepeSkins'>Plush Pepe 🐸</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/PreciousPeachSkins'>Precious Peach 🍑</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/RecordPlayerSkins'>Record Player 🎶</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/SakuraFlowerSkins'>Sakura Flower 🌸</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/SantaHatSkins'>Santa Hat 🎅</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/ScaredCatSkins'>Scared Cat 😺</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/SharpTongueSkins'>Sharp Tongue 🗣️</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/SignetRingSkins'>Signet Ring 💍</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/SkullFlowerSkins'>Skull Flower 💀</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/SleighBellSkins'>Sleigh Bell 🔔</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/SnowGlobeSkins'>Snow Globe 🌍</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/SnowMittensSkins'>Snow Mittens 🧤</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/SpicedWineSkins'>Spiced Wine 🍷</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/SpyAgaricSkins'>Spy Agaric 🍄</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/StarNotepadSkins'>Star Notepad 📓</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/SwissWatchSkins'>Swiss Watch ⌚</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/TamaGadgetSkins'>Tama Gadget 🎮</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/TopHatSkins'>Top Hat 🎩</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/ToyBearSkins'>Toy Bear 🐻</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/TrappedHeartSkins'>Trapped Heart 💔</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/VintageCigarSkins'>Vintage Cigar 🚬</a></b>\n"
        "<b>├ <a href='https://t.me/addemoji/VoodooDollSkins'>Voodoo Doll 🪆</a></b>\n"
        "<b>└ <a href='https://t.me/addemoji/WinterWreathSkins'>Winter Wreath 🌲</a></b>\n"
        "<b>└ <a href='https://t.me/addemoji/WitchHatSkins'>Witch Hat 🎩</a></b>\n",
        parse_mode="HTML",
        reply_markup=kb.gifts_list,
        disable_web_page_preview=True)
    
    await state.set_state(GiftSearch.waiting_for_gift_name)

@router.callback_query(GiftSearch.waiting_for_gift_name)
async def get_gift_name(callback: CallbackQuery, state: FSMContext):

    callback_data = callback.data

    if callback_data == "back_to_menu":
        await back_to_menu_button(callback, state)

    gift_name = callback_data.split(":")[0]
    gift_emoji_link = callback_data.split(":")[1]

    await callback.message.answer(
        f"<b>🎁 Выбран подарок: <a href='https://t.me/addemoji/{gift_emoji_link}Skins'>{gift_name}</a></b>\n\n"
        "<b>🔍 Выберите способ поиска:</b>",
        parse_mode="HTML",
        reply_markup=kb.search_methods,
        disable_web_page_preview=True)

    await state.update_data(gift_name=gift_name)

    await state.set_state(GiftSearch.waiting_for_search_method)

@router.callback_query(GiftSearch.waiting_for_search_method)
async def get_search_method(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    gift_name = data.get('gift_name')

    callback_data = callback.data

    if callback_data == "back_to_menu":
        await back_to_menu_button(callback, state)

    search_method = callback_data

    if search_method == "Модель 🎁":
        text = "<b>🌟 Введите название модели для поиска:</b>"
    elif search_method == "Фон 🖼️":
        text = "<b>🌟 Введите название фона для поиска:</b>"
    elif search_method == "Модель + Фон 🌈":
        text = "<b>🌟 Введите название модели и фона для поиска:</b>"
    elif search_method == "Узор 🎨":
        text = "<b>🌟 Введите название узора для поиска:</b>"
    elif search_method == "Номер 🔢":
        text = "<b>🌟 Введите номер подарка или диапазон (например, 100-200) для поиска — оба числа включительно:</b>"

    await callback.message.answer(
        f"<b>🎁 Подарок: {gift_name}</b>\n"
        f"<b>🔍 Выбранный способ поиска: {search_method}</b>\n\n"
        f"{text}\n"
        "<i>💡 Пожалуйста, убедитесь, что данные введены корректно!</i>",
        parse_mode="HTML")
    
    await state.update_data(search_method=search_method)

    if search_method == "Модель 🎁":
        await state.set_state(GiftSearch.waiting_for_model_name)
    elif search_method == "Фон 🖼️":
        await state.set_state(GiftSearch.waiting_for_backdrop_name)
    elif search_method == "Модель + Фон 🌈":
        await state.set_state(GiftSearch.waiting_for_model_and_backdrop_name)
    elif search_method == "Узор 🎨":
        await state.set_state(GiftSearch.waiting_for_symbol_name)
    elif search_method == "Номер 🔢":
        await state.set_state(GiftSearch.waiting_for_number)

@router.message(GiftSearch.waiting_for_model_name)
async def get_model_name(message: Message, state: FSMContext):
    
    data = await state.get_data()

    gift_name = data.get('gift_name')

    search_method = data.get('search_method')

    model_name = message.text

    await message.answer(
        f"<b>🎁 Подарок: {gift_name}</b>\n"
        f"<b>🔍 Способ поиска: {search_method}</b>\n"
        f"<b>🌟 Название модели: {model_name}</b>\n\n"
        "<b>➡️ Вы уверены, что данные введены корректно?</b>",
        parse_mode="HTML",
        reply_markup=kb.yes_or_no)
    
    await state.update_data(model_name=model_name)

    await state.set_state(GiftSearch.waiting_for_confirm)

@router.message(GiftSearch.waiting_for_backdrop_name)
async def get_backdrop_name(message: Message, state: FSMContext):
    
    data = await state.get_data()

    gift_name = data.get('gift_name')

    search_method = data.get('search_method')

    backdrop_name = message.text

    await message.answer(
        f"<b>🎁 Подарок: {gift_name}</b>\n"
        f"<b>🔍 Способ поиска: {search_method}</b>\n"
        f"<b>🌟 Название фона: {backdrop_name}</b>\n\n"
        "<b>➡️ Вы уверены, что данные введены корректно?</b>",
        parse_mode="HTML",
        reply_markup=kb.yes_or_no)
    
    await state.update_data(backdrop_name=backdrop_name)

    await state.set_state(GiftSearch.waiting_for_confirm)

@router.message(GiftSearch.waiting_for_model_and_backdrop_name)
async def get_model_and_backdrop_name(message: Message, state: FSMContext):

    data = await state.get_data()
    gift_name = data.get('gift_name')
    search_method = data.get('search_method')

    model_and_backdrop_name = message.text

    split_input = model_and_backdrop_name.split(',')
    
    if len(split_input) != 2:
        await message.answer(
            "<b>⚠️ Ошибка! Пожалуйста, введите данные в формате:</b>\n"
            "<b>Модель, Фон</b>.\n"
            "<b>Пример:</b> модель1, фон1",
            parse_mode="HTML")
        
        return

    model_name = split_input[0].strip()
    backdrop_name = split_input[1].strip()

    await message.answer(
        f"<b>🎁 Подарок: {gift_name}</b>\n"
        f"<b>🔍 Способ поиска: {search_method}</b>\n"
        f"<b>🌟 Название модели: {model_name}</b>\n"
        f"<b>🌟 Название фона: {backdrop_name}</b>\n\n"
        "<b>➡️ Вы уверены, что данные введены корректно?</b>",
        parse_mode="HTML",
        reply_markup=kb.yes_or_no)

    await state.update_data(model_name=model_name, backdrop_name=backdrop_name)

    await state.set_state(GiftSearch.waiting_for_confirm)

@router.message(GiftSearch.waiting_for_symbol_name)
async def get_symbol_name(message: Message, state: FSMContext):
    
    data = await state.get_data()

    gift_name = data.get('gift_name')

    search_method = data.get('search_method')

    symbol_name = message.text

    await message.answer(
        f"<b>🎁 Подарок: {gift_name}</b>\n"
        f"<b>🔍 Способ поиска: {search_method}</b>\n"
        f"<b>🌟 Название узора: {symbol_name}</b>\n\n"
        "<b>➡️ Вы уверены, что данные введены корректно?</b>",
        parse_mode="HTML",
        reply_markup=kb.yes_or_no)
    
    await state.update_data(symbol_name=symbol_name)

    await state.set_state(GiftSearch.waiting_for_confirm)

@router.message(GiftSearch.waiting_for_number)
async def get_number(message: Message, state: FSMContext):

    data = await state.get_data()

    gift_name = data.get('gift_name')
    search_method = data.get('search_method')

    number_text = message.text.strip()

    if number_text.isdigit():
        number = int(number_text)
        number_display = f"Номер подарка: {number}"
        number_data = number
    
    elif re.fullmatch(r'\d+-\d+', number_text):
        start, end = map(int, number_text.split('-'))
        if start > end:
            await message.answer("⚠️ Ошибка: начальное число больше конечного. Введите корректный диапазон!")
            return
        number_data = list(range(start, end + 1))
        number_display = f"Диапазон номеров: {start} - {end}"

    else:
        await message.answer("⚠️ Ошибка: Введите одно число или диапазон (например, 100-200)!")
        return

    await message.answer(
        f"<b>🎁 Подарок: {gift_name}</b>\n"
        f"<b>🔍 Способ поиска: {search_method}</b>\n"
        f"<b>🌟 {number_display}</b>\n\n"
        "<b>➡️ Вы уверены, что данные введены корректно?</b>",
        parse_mode="HTML",
        reply_markup=kb.yes_or_no)

    await state.update_data(number=number_data)

    await state.set_state(GiftSearch.waiting_for_confirm)

async def send_links(callback: CallbackQuery, links, search_method, model_name, backdrop_name, symbol_name, number):
    
    callback_data = callback.data

    if callback_data == "yes":
        if not links:
            await callback.message.answer("❌ Подарки не найдены.")
            return

        if len(links) <= 50:
            batch_size = 50
            for i in range(0, len(links), batch_size):
                text = "\n".join(links[i:i+batch_size])
                await callback.message.answer(text, disable_web_page_preview=True)
        
        else:
            file_name = "gift_links.txt"
            
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, file_name)

            with open(file_path, "w", encoding="utf-8") as file:
                file.write("\n".join(links))

            await callback.message.answer_document(FSInputFile(file_path), caption="📄 Ваш список ссылок")

            os.remove(file_path)

        if search_method == "Модель 🎁":
            search_info = f"<b>🔹 Модель:</b> {model_name}"
        elif search_method == "Фон 🖼️":
            search_info = f"<b>🔹 Фон:</b> {backdrop_name}"
        elif search_method == "Модель + Фон 🌈":
            search_info = f"<b>🔹 Модель:</b> {model_name}\n<b>🔹 Фон:</b> {backdrop_name}"
        elif search_method == "Узор 🎨":
            search_info = f"<b>🔹 Узор:</b> {symbol_name}"
        elif search_method == "Номер 🔢":
            if isinstance(number, list):
                search_info = f"<b>🔹 Номер:</b> {number[0]} - {number[-1]}"
            else:
                search_info = f"<b>🔹 Номер:</b> {number}"

        statistics_message = (
            f"<b>📊 Статистика парсинга:</b>\n"
            f"<b>🔹 Способ поиска:</b> {search_method}\n"
            f"{search_info}\n"
            f"<b>🔹 Количество ссылок:</b> {len(links)}"
        )

        await callback.message.answer(statistics_message, parse_mode="HTML")

    elif callback_data == "no":
        await callback.message.answer(
            "<b>❌ Действие успешно отменено.</b>",
            parse_mode="HTML",
            reply_markup=kb.back_to_menu)

@router.callback_query(GiftSearch.waiting_for_confirm)
async def get_confirm(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    gift_name = data.get('gift_name')
    search_method = data.get('search_method')
    model_name = data.get('model_name')
    backdrop_name = data.get('backdrop_name')
    model_and_backdrop_name = data.get('model_and_backdrop_name')
    symbol_name = data.get('symbol_name')
    number = data.get('number')

    gift_name = gift_name.replace(" ", "").replace("_", "").replace("’", "").replace("-", "")

    db_connection = await get_db_connection()

    if search_method == "Модель 🎁":
        links = await get_links_by_model_name(db_connection, gift_name, model_name)
    elif search_method == "Фон 🖼️":
        links = await get_links_by_backdrop_name(db_connection, gift_name, backdrop_name)
    elif search_method == "Модель + Фон 🌈":
        links = await get_links_by_model_and_backdrop_name(db_connection, gift_name, model_name, backdrop_name)
    elif search_method == "Узор 🎨":
        links = await get_links_by_symbol_name(db_connection, gift_name, symbol_name)
    elif search_method == "Номер 🔢":
        links = await get_links_by_number(db_connection, gift_name, number)

    callback_data = callback.data

    if callback_data == "yes":

        await send_links(callback, links, search_method, model_name, backdrop_name, symbol_name, number)

    elif callback_data == "no":
        await callback.message.answer(
            "<b>❌ Действие успешно отменено.</b>",
            parse_mode="HTML",
            reply_markup=kb.back_to_menu)

class GlobalSearch(StatesGroup):
    waiting_for_search_method = State()
    waiting_for_backdrop_name = State()
    waiting_for_backdrop_and_symbol_name = State()
    waiting_for_symbol_name = State()
    waiting_for_confirm = State()
    waiting_for_link_type = State()

@router.callback_query(F.data == "global_search")
async def global_search_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        f"<b>🕵️‍♂️ Вы выбрали глобальный поиск</b>\n\n"
        "<b>🔍 Выберите способ поиска:</b>",
        parse_mode="HTML",
        reply_markup=kb.global_search_methods)

    await state.set_state(GlobalSearch.waiting_for_search_method)

@router.callback_query(GlobalSearch.waiting_for_search_method)
async def get_global_search_method(callback: CallbackQuery, state: FSMContext):

    callback_data = callback.data

    if callback_data == "back_to_menu":
        await back_to_menu_button(callback, state)

    search_method = callback_data

    if search_method == "Фон 🖼️":
        text = "<b>🌟 Введите название фона для поиска:</b>"
    elif search_method == "Фон + Узор 🌈":
        text = "<b>🌟 Введите название фона и узора для поиска:</b>"
    elif search_method == "Узор 🎨":
        text = "<b>🌟 Введите название узора для поиска:</b>"

    await callback.message.answer(
        f"<b>🔍 Выбранный способ поиска: {search_method}</b>\n"
        f"{text}\n"
        "<i>💡 Пожалуйста, убедитесь, что данные введены корректно!</i>",
        parse_mode="HTML")
    
    await state.update_data(search_method=search_method)

    if search_method == "Фон 🖼️":
        await state.set_state(GlobalSearch.waiting_for_backdrop_name)
    elif search_method == "Фон + Узор 🌈":
        await state.set_state(GlobalSearch.waiting_for_backdrop_and_symbol_name)
    elif search_method == "Узор 🎨":
        await state.set_state(GlobalSearch.waiting_for_symbol_name)

@router.message(GlobalSearch.waiting_for_backdrop_name)
async def get_global_backdrop_name(message: Message, state: FSMContext):

    data = await state.get_data()

    search_method = data.get('search_method')
    backdrop_name = message.text

    await message.answer(
        f"<b>🔍 Способ поиска: {search_method}</b>\n"
        f"<b>🌟 Название фона: {backdrop_name}</b>\n\n"
        "<b>➡️ Вы уверены, что данные введены корректно?</b>",
        parse_mode="HTML",
        reply_markup=kb.yes_or_no)
    
    await state.update_data(backdrop_name=backdrop_name)

    await state.set_state(GlobalSearch.waiting_for_confirm)

@router.message(GlobalSearch.waiting_for_backdrop_and_symbol_name)
async def get_backdrop_and_symbol_name(message: Message, state: FSMContext):

    data = await state.get_data()
    search_method = data.get('search_method')

    backdrop_and_symbol_name = message.text
    split_input = backdrop_and_symbol_name.split(',')

    if len(split_input) != 2:
        await message.answer(
            "<b>⚠️ Ошибка! Пожалуйста, введите данные в формате:</b>\n"
            "<b>Фон, Узор</b>.\n"
            "<b>Пример:</b> фон1, узор1",
            parse_mode="HTML")
        return

    backdrop_name = split_input[0].strip()
    symbol_name = split_input[1].strip()

    await message.answer(
        f"<b>🔍 Способ поиска: {search_method}</b>\n"
        f"<b>🌟 Название фона: {backdrop_name}</b>\n"
        f"<b>🌟 Название узора: {symbol_name}</b>\n\n"
        "<b>➡️ Вы уверены, что данные введены корректно?</b>",
        parse_mode="HTML",
        reply_markup=kb.yes_or_no)

    await state.update_data(backdrop_name=backdrop_name, symbol_name=symbol_name)

    await state.set_state(GlobalSearch.waiting_for_confirm)

@router.message(GlobalSearch.waiting_for_symbol_name)
async def get_global_symbol_name(message: Message, state: FSMContext):

    data = await state.get_data()

    search_method = data.get('search_method')
    symbol_name = message.text

    await message.answer(
        f"<b>🔍 Способ поиска: {search_method}</b>\n"
        f"<b>🌟 Название узора: {symbol_name}</b>\n\n"
        "<b>➡️ Вы уверены, что данные введены корректно?</b>",
        parse_mode="HTML",
        reply_markup=kb.yes_or_no)
    
    await state.update_data(symbol_name=symbol_name)

    await state.set_state(GlobalSearch.waiting_for_confirm)

@router.callback_query(GlobalSearch.waiting_for_confirm)
async def get_global_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    search_method = data.get('search_method')
    backdrop_name = data.get('backdrop_name')
    symbol_name = data.get('symbol_name')

    db_connection = await get_db_connection()

    if search_method == "Фон 🖼️":
        links = await get_global_links_by_backdrop_name(db_connection, backdrop_name)
    elif search_method == "Узор 🎨":
        links = await get_global_links_by_symbol_name(db_connection, symbol_name)
    elif search_method == "Фон + Узор 🌈":
        links = await get_global_links_by_backdrop_and_symbol_name(db_connection, backdrop_name, symbol_name)

    await send_global_links(callback, links, search_method, backdrop_name, symbol_name)

async def send_global_links(callback: CallbackQuery, links, search_method, backdrop_name, symbol_name):
    if not links:
        await callback.message.answer("❌ Ссылки не найдены.")
        return

    if len(links) <= 50:
        batch_size = 50
        for i in range(0, len(links), batch_size):
            text = "\n".join(links[i:i + batch_size])
            await callback.message.answer(text, disable_web_page_preview=True)
    else:
        file_name = "global_links.txt"
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(links))

        await callback.message.answer_document(FSInputFile(file_path), caption="📄 Ваш список ссылок")
        os.remove(file_path)

    if search_method == "Фон 🖼️":
        search_info = f"<b>🔹 Фон:</b> {backdrop_name}"
    elif search_method == "Фон + Узор 🌈":
        search_info = f"<b>🔹 Фон:</b> {backdrop_name}\n<b>🔹 Узор:</b> {symbol_name}"
    elif search_method == "Узор 🎨":
        search_info = f"<b>🔹 Узор:</b> {symbol_name}"

    statistics_message = (
        f"<b>📊 Статистика поиска:</b>\n"
        f"<b>🔹 Способ поиска:</b> {search_method}\n"
        f"{search_info}\n"
        f"<b>🔹 Количество ссылок:</b> {len(links)}"
    )

    await callback.message.answer(statistics_message, parse_mode="HTML")

@router.callback_query(F.data == "general_db_stats")
async def stats_db_button(callback: CallbackQuery):

    db_connection = await get_db_connection()

    number_of_tables = await get_number_of_tables(db_connection)

    total_number_gifts = await get_total_number_gifts(db_connection)

    statistics = await get_statistics(db_connection)

    await callback.message.answer(
        f"<b>📊 <u>Статистика базы данных</u>:</b>\n\n"
        f"<b>🎁 Общее количество подарков:</b> <code>{total_number_gifts}</code>\n"
        f"<b>🌈 Всего моделей в базе:</b> <code>{statistics['total_unique_models']}</code>\n"
        f"<b>🖼️ Всего фонов в базе:</b> <code>{statistics['total_unique_backdrops']}</code>\n"
        f"<b>🎨 Всего узоров в базе:</b> <code>{statistics['total_unique_symbols']}</code>\n\n"
        f"<b>📂 Количество баз данных:</b> <code>{number_of_tables}</code>",
        parse_mode="HTML",
        reply_markup=kb.back_to_menu)

@router.callback_query(F.data == "info")
async def info_button(callback: CallbackQuery):
    await callback.message.answer(
        "<b>ℹ️ Информация о боте</b>\n\n"
        "<b>Все самые важные сведения в одном месте. Следи за обновлениями, узнавай больше о разработке и будь в курсе новостей! 🚀</b>",
        parse_mode="HTML",
        reply_markup=kb.info)

@router.callback_query(F.data == "admin_panel")
async def admin_panel_button(callback: CallbackQuery):
    await callback.message.answer(
        "<b>🔧 Админ-панель</b>\n\n"
        "<b>🛠 Выберите действие:</b>",
        parse_mode="HTML",
        reply_markup=kb.admin_panel)

@router.callback_query(F.data == "parsing")
async def parsing_button(callback: CallbackQuery):
    await callback.message.answer(
        "<i>⬇️ Выберите действие:</i>",
        parse_mode="HTML",
        reply_markup=kb.parsing)

@router.callback_query(F.data == "auto_parsing")
async def auto_parsing_button(callback: CallbackQuery):
    await callback.message.answer(
        "<b>ℹ️ Для вашего удобства, чтобы вы могли следить за процессом и получать логи в режиме реального времени, пожалуйста, добавьте меня в ваш Telegram канал и назначьте администратором. 🛡️</b>\n"
        "<b>🔔 Так вы всегда будете в курсе событий!</b>\n\n"
        "<i>⬇️ Выберите действие:</i>",
        parse_mode="HTML",
        reply_markup=kb.auto_parsing)

HEADERS = {"User-Agent": "Mozilla/5.0"}
semaphore = asyncio.Semaphore(50)

progress_data = {}

ssl_context = ssl.create_default_context(cafile=certifi.where())

@router.callback_query(F.data == "progress_parsing")
async def show_parsing_progress(callback: CallbackQuery):

    global parsing_enabled

    if not parsing_enabled:
        await callback.message.answer("ℹ️ Статус: парсинг не запущен. Начните процесс, чтобы получить обновлённые данные.")
        return

    progress_messages = []

    for gift_name in GIFTS:
        gift_display = GIFTS_NAME_WITH_LINKS.get(gift_name, gift_name)
        if gift_name in progress_data:
            progress = progress_data[gift_name]
            progress_messages.append(f"{gift_display}: <i>{progress:.2f}%</i>")
        else:
            progress_messages.append(f"{gift_display}: <i>🔄 Ожидание...</i>")

    progress_text = "\n\n".join(progress_messages)
    await callback.message.answer(f"<b>📊 Прогресс парсинга:</b>\n\n{progress_text}", parse_mode="HTML", reply_markup=kb.back_to_menu, disable_web_page_preview=True)

async def get_last_number(db_connection, gift_name):
    table_name = gift_name
    cursor = await db_connection.execute(f"SELECT MAX(number) FROM {table_name}")
    result = await cursor.fetchone()
    return result[0] if result[0] else 0

async def get_quantity(gift_name):
    url = f"https://t.me/nft/{gift_name}-1"
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")

                quantity_row = soup.find("th", string=lambda text: text and "Quantity" in text)
                if quantity_row:
                    quantity_data = quantity_row.find_next_sibling("td").text.strip().replace("\xa0", " ").replace("issued", "").strip()

                    quantity_data = quantity_data.replace(" ", "")

                    if "/" in quantity_data:
                        issued, total = quantity_data.split("/")
                        try:
                            issued = int(issued)
                            total = int(total)
                            return issued, total
                        except ValueError:
                            return 0, 0
                    else:
                        try:
                            total = int(quantity_data)
                            return 0, total
                        except ValueError:
                            return 0, 0
    return 0, 0

async def safe_request(session, url, headers, retries=5, delay=5):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    for attempt in range(retries):
        try:
            async with session.get(url, headers=headers, ssl=ssl_context) as response:
                if response.status == 200:
                    return await response.text()
                # logging.info(f"⚠️ Ошибка {response.status} при запросе {url}. Повтор {attempt + 1}/{retries}")
        except (aiohttp.ClientError, ConnectionResetError, ssl.SSLError) as e:
            logging.info(f"⚠️ Ошибка сети {e}. Повтор {attempt + 1}/{retries}")

        await asyncio.sleep(delay + random.uniform(1, 3))
        
    # logging.info(f"🚨 Не удалось получить данные с {url} после {retries} попыток.")
    return None

async def parse_page(session, gift_name, number):

    url = f"https://t.me/nft/{gift_name}-{number}"
    html = await safe_request(session, url, HEADERS)
    if not html:
        return (number, None, None, None, None, None, None)

    soup = BeautifulSoup(html, "html.parser")

    def extract_data(label):
        element = soup.find("th", string=label)
        if element:
            data = element.find_next_sibling("td")
            if data:
                text = data.text.split("<mark>")[0].strip()
                match = re.search(r'(\d+(\.\d+)?)%', text)
                percent = match.group(0) if match else None
                text = text.replace(percent, "").strip() if percent else text
                return text, percent
        return None, None

    model_text, model_percent = extract_data("Model")
    backdrop_text, backdrop_percent = extract_data("Backdrop")
    symbol_text, symbol_percent = extract_data("Symbol")

    return (number, model_text, model_percent, backdrop_text, backdrop_percent, symbol_text, symbol_percent)

async def parse_owner(session, gift_name, number):
    url = f"https://t.me/nft/{gift_name}-{number}"
    logging.info(f"Пытаемся получить HTML для {gift_name}-{number} по URL: {url}")
    
    html = await safe_request(session, url, HEADERS)
    
    if not html:
        logging.info(f"Не удалось получить HTML для {gift_name}-{number} по URL: {url}")
        return number, None

    logging.info(f"HTML получен для {gift_name}-{number}, начинаем парсинг...")
    soup = BeautifulSoup(html, "html.parser")

    owner_element = soup.find("th", string="Owner")
    if owner_element:
        owner_td = owner_element.find_next_sibling("td")
        if owner_td:
            owner_a = owner_td.find("a", href=True)
            if owner_a and "https://t.me/" in owner_a["href"]:
                owner_nick = owner_a["href"].split("/")[-1]
                logging.info(f"Владелец найден для {gift_name}-{number}: {owner_nick}")
                return number, owner_nick

    logging.info(f"Владелец не найден для {gift_name}-{number}")
    return number, None

async def update_progress(progress_queue, quantity_issued, gift_name):

    global progress_data

    while True:
        if not parsing_enabled:
            # logging.info(f"Обновление прогресса для {gift_name} было остановлено.")
            break

        last_number = await progress_queue.get()
        progress = (last_number / quantity_issued) * 100
        progress_data[gift_name] = progress
        # logging.info(f"🔄 [{gift_name}] Прогресс парсинга: {progress:.2f}%")

        if last_number >= quantity_issued:
            break

        await asyncio.sleep(5)

async def process_gift(db_connection, gift_name):
    # logging.info(f"🎁 Начинаем обработку подарка: {gift_name}")
    await create_table(db_connection, gift_name)

    last_number = await get_last_number(db_connection, gift_name)
    quantity_issued, _ = await get_quantity(gift_name)

    # logging.info(f"🎁 Парсим {gift_name}: найдено {quantity_issued}, начинаем с {last_number + 1}")

    progress_queue = asyncio.Queue()
    progress_task = asyncio.create_task(update_progress(progress_queue, quantity_issued, gift_name))

    async with aiohttp.ClientSession() as session:
        # logging.info(f"🎁 [{gift_name}] Запускаем цикл парсинга страниц...")
        for i in range(last_number + 1, quantity_issued + 1):
            if not parsing_enabled:
                # logging.info(f"Парсинг {gift_name} был отменен на номере {i}.")
                break

            # logging.info(f"🎁 [{gift_name}] Парсим страницу номер {i}...")
            try:
                data = await parse_page(session, gift_name, i)
                await save_to_db(db_connection, gift_name, data)
                await progress_queue.put(i) 
                await asyncio.sleep(0.02)
            except Exception as e:
                # logging.info(f"🎁 [{gift_name}] Ошибка при парсинге страницы {i}: {e}")
                continue

        # logging.info(f"🎁 [{gift_name}] Цикл парсинга страниц завершен.")

    await progress_queue.put(quantity_issued)
    await progress_task
    # logging.info(f"🎁 Обработка подарка {gift_name} завершена.")

parsing_enabled = False
parsing_task = None

async def start_parsing(new_gifts_list):
    global parsing_enabled, parsing_task

    # logging.info(f"🚀 Запуск программы парсинга начат для подарков: {new_gifts_list}")

    if not parsing_enabled:
        # logging.info("🚫 Парсинг отключен.")
        return

    db_connection = await get_db_connection()

    tasks = [process_gift(db_connection, gift) for gift in new_gifts_list]

    parsing_task = asyncio.gather(*tasks)

    try:
        await parsing_task
    except Exception as e:
        logging.info(f"🚨 Произошла ошибка во время парсинга: {e}")
    finally:
        parsing_enabled = False
        # logging.info("✅ Парсинг завершен.")

@router.callback_query(F.data == "start_gift_parsing")
async def start_gift_parsing_button(callback: CallbackQuery):
    global parsing_enabled, parsing_task

    if parsing_enabled:
        await callback.answer("Парсинг уже включен. Ожидайте завершения.")
        return

    parsing_enabled = True
    # logging.info("Парсинг включен.")
    await callback.answer("Парсинг начат! 🚀")

    await start_parsing(GIFTS)

    parsing_enabled = False
    await callback.answer("Парсинг завершен. ✅")

@router.callback_query(F.data == "stop_gift_parsing")
async def stop_gift_parsing_button(callback: CallbackQuery):

    global parsing_enabled, parsing_task

    if not parsing_enabled:
        await callback.answer("Парсинг уже выключен.")
        return

    if parsing_task:
        parsing_task.cancel()
            
    parsing_enabled = False
    await callback.answer("Парсинг остановлен. ❌")

auto_parsing_enabled = False
auto_parsing_task = None
parsing_enabled = False

async def auto_parsing(user_id):
    global auto_parsing_enabled, auto_parsing_task, parsing_enabled

    await bot.send_message(user_id, "<b>Начинаем через секунду... ⏳</b>", parse_mode="HTML")
    await asyncio.sleep(1)

    # logging.info(f"🚀 Авто-парсинг запущен для пользователя {user_id}.")
    await bot.send_message(user_id, "🚀 <b>Авто-парсинг запущен!</b>\n\nПроверка на новые подарки будет проводиться <b>каждую минуту</b>.", parse_mode="HTML")

    auto_parsing_enabled = True
    try:
        while auto_parsing_enabled:
            await check_new_gifts(user_id)
            # logging.info(f"🔍 Проверка новых подарков для пользователя {user_id} завершена.")
            if parsing_enabled:
                while parsing_enabled:
                    await asyncio.sleep(1)
                # logging.info(f"⏳ Пауза 15 минут после парсинга перед следующей проверкой для пользователя {user_id}...")
                for i in range(900):
                    # logging.info(f"⏳ [После парсинга] Ожидание секунда {i+1}/900...")
                    if not auto_parsing_enabled:
                        # logging.info(f"🔴 Авто-парсинг отключён во время ожидания после парсинга. Пользователь: {user_id}")
                        await bot.send_message(user_id, "❌ Авто-парсинг остановлен.")
                        return
                    await asyncio.sleep(1)
                    # logging.info(f"⏳ [После парсинга] Секунда {i+1}/900 ожидания завершена.")
                # logging.info(f"⏳ 15-минутная пауза после парсинга завершена.")
            else:
                # logging.info(f"⏳ Ожидание 15 минут перед следующей проверкой для пользователя {user_id}...")
                for i in range(900):
                    # logging.info(f"⏳ [Без парсинга] Ожидание секунда {i+1}/900...")
                    if not auto_parsing_enabled:
                        # logging.info(f"🔴 Авто-парсинг отключён во время ожидания. Пользователь: {user_id}")
                        await bot.send_message(user_id, "❌ Авто-парсинг остановлен.")
                        return
                    await asyncio.sleep(1)
                    # logging.info(f"⏳ [Без парсинга] Секунда {i+1}/900 ожидания завершена.")
                # logging.info(f"⏳ 15-минутное ожидание завершено.")

    except asyncio.CancelledError:
        # logging.info(f"🛑 Задача авто-парсинга отменена для пользователя {user_id}.")
        await bot.send_message(user_id, "❌ Авто-парсинг остановлен (отмена задачи).")
    finally:
        auto_parsing_task = None
        # logging.info(f"Авто-парсинг завершен для пользователя {user_id}.")

@router.callback_query(F.data == "start_auto_parsing")
async def start_auto_parsing_button(callback: CallbackQuery):

    global auto_parsing_enabled, auto_parsing_task

    user_id = callback.from_user.id

    if auto_parsing_enabled:
        await callback.answer("Авто-парсинг уже включен.")
        return

    auto_parsing_enabled = True
    if auto_parsing_task is None:
        auto_parsing_task = asyncio.create_task(auto_parsing(user_id))
    else:
        await callback.answer("Авто-парсинг задача уже запущена.")

@router.callback_query(F.data == "stop_auto_parsing")
async def stop_auto_parsing_button(callback: CallbackQuery):

    global auto_parsing_enabled, auto_parsing_task

    if not auto_parsing_enabled:
        await callback.answer("Авто-парсинг уже выключен.")
        return

    auto_parsing_enabled = False
    if auto_parsing_task is not None:
        auto_parsing_task.cancel()
    else:
        await callback.answer("Авто-парсинг не запущен.")

async def check_new_gifts(user_id):

    global parsing_enabled
    # logging.info(f"🔍 Проверка новых подарков для пользователя {user_id}...")

    db_connection = await get_db_connection()
    report_lines = []
    total_new_gifts_count = 0
    new_gifts_to_parse = []

    gifts_data = []

    for gift in GIFTS:
        last_number = await get_last_number(db_connection, gift)
        issued, total = await get_quantity(gift)
        new_items_count = issued - last_number
        new_gift_available = total - last_number
        gifts_data.append((gift, issued, new_items_count, new_gift_available))

    report_lines = []
    total_new_gifts_count = 0

    for gift, issued, new_items_count, new_gift_available in gifts_data:

        gift_name = GIFTS_NAME_WITH_LINKS.get(gift, f"<b>{gift}</b>")
        gift_line = f"{gift_name} ({new_items_count})"

        if new_items_count > 0:
            gift_line += " 🆕️"
            total_new_gifts_count += new_items_count
            if new_items_count > 0:
                new_gifts_to_parse.append(gift)

        report_lines.append(gift_line)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_message = (
        f"✨ <b>NFT Update Report!</b> ✨\n"
        f"<b>Time:</b> {timestamp} (MSK)\n\n"
        + "\n".join(report_lines) +
        f"\n\n<b>New:</b> {total_new_gifts_count} gifts")

    await bot.send_message(LOGS_CHANNEL_ID, report_message, parse_mode="HTML", disable_web_page_preview=True)

    if new_gifts_to_parse:
        parsing_enabled = True

        await start_parsing(new_gifts_to_parse)

        parsing_enabled = False

    # if total_new_gifts_count == 0:
    #     await bot.send_message(user_id, "✅ <b>Новых подарков не найдено.</b>\n\nПроверка будет повторена через минуту.", parse_mode="HTML")
    # else:
    #     await bot.send_message(user_id, report_message, parse_mode="HTML", reply_markup=kb.back_to_menu, disable_web_page_preview=True)

    #     if new_gifts_to_parse:
    #         parsing_enabled = True
    #         await bot.send_message(user_id, "🚀 <b>Запущен парсинг найденных подарков...</b>", parse_mode="HTML")

    #         await start_parsing(new_gifts_to_parse)
    #         parsing_enabled = False

    #         await bot.send_message(user_id, "✅ <b>Парсинг завершён!</b>", parse_mode="HTML")

