from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters.command import Command, CommandStart
from aiogram.fsm.context import FSMContext
from bot_sys import texts as txt
from bot_sys import services as serv
from bot_sys import keyboards as kb
from bot_sys import states as st
from bot_sys import data as db

#использованные callback_data == menu_pick, to_page_, vuz_, to_grid_page_, menu_all, exit_to_menu


router = Router()


