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


#обработчик для кнопки подобрать 
@router.callback_query(F.data == 'menu_pick')
async def menu_button_pick(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text(text = txt.MESSAGES['ask_direction'], reply_markup = kb.get_direction_keyboard())


#обработчик для кнопки изменить баллы
@router.callback_query(F.data == 'score_change')
async def change_user_score(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await state.update_data(user_score = None)
    await state.set_state(st.InputScore.waiting_score)

    await call.message.edit_text(text = txt.MESSAGES['ask_ege_change'])


#функция для обработки кнопки о боте
@router.callback_query(F.data == 'about')
async def about_bot_page(call: CallbackQuery, state: FSMContext):
    await call.answer()

    data = await state.get_data()

    await call.message.edit_text(text = txt.MESSAGES['about_text'],
                                 reply_markup = kb.menu(data.get('user_score', None)))
