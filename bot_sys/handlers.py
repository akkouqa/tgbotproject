from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters.command import Command, CommandStart
from aiogram.fsm.context import FSMContext
from bot_sys import texts as txt
from bot_sys import services as serv
from bot_sys import keyboards as kb
from bot_sys import states as st
from bot_sys import data as db


router = Router()


#обработка команды /start всегда самый первый
@router.message(CommandStart())
async def start(msg: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message = await msg.answer(txt.MESSAGES['start_msg'], reply_markup = kb.menu(data.get('user_score', None)))

    await serv.delete_user_msg(msg)
    await serv.cleanup(state, bot, msg.chat.id)
    await state.clear()
    await state.update_data(bot_message_ids = [message.message_id])


#обработчик для получение file_id потом уберем
@router.message(F.photo)
async def temp_file_id(msg: Message):
    id = msg.photo[-1].file_id
    print(id)
    await msg.answer('айди в терминале, лучше кидать несколько сразу')


#обработчик кнопки направления вуза
@router.callback_query(F.data.startswith('vuz_direction_'))
async def direction_button_pick(call: CallbackQuery, state: FSMContext):
    await call.answer()

    data = await state.get_data()
    dir_id = call.data.split('_')[2]
    
    await state.update_data(user_direction = dir_id)

    if data.get('user_score'):
        user_score = data.get('user_score')

        await state.set_state(None)
        await call.message.edit_text(text = txt.MESSAGES['grid_header'].format(#score = user_score,
                                                        direction_name = serv.get_direction_name(dir_id)), 
                                                        reply_markup = kb.get_vuz_keyboard(user_score, 0, dir_id))
        return 
    
    await state.set_state(st.InputScore.waiting_score)
    await call.message.edit_text(txt.MESSAGES['ask_ege'])


#обработчик баллов егэ пользователя и вывод сетки вузов как минимум пока что она будет вылетать сразу
@router.message(st.InputScore.waiting_score)
async def input_user_score(msg: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    ids = data.get('bot_message_ids', [])
    error_text = None
    dir_id = data.get('user_direction')

    dir_name = serv.get_direction_name(dir_id) 
    
    await serv.delete_user_msg(msg)

    if msg.text:
        user_message = msg.text.strip()
        if not user_message.startswith('-'):
            if user_message.isdigit():
                user_score = int(user_message)
                if user_score <= 310:
                    await state.update_data(user_score = user_score)
                    await state.set_state(None)
                    await bot.edit_message_text(message_id = ids[0], chat_id = msg.chat.id,
                                                text = txt.MESSAGES['grid_header'].format(score = user_score,
                                                                                          direction_name = 
                                                                                          dir_name),
                                                reply_markup = kb.get_vuz_keyboard(user_score, 0, dir_id))
                    return
                else:
                    error_text = txt.MESSAGES['ege_too_high']
            else:
                error_text = txt.MESSAGES['ege_invalid']
        else:
            error_text = txt.MESSAGES['ege_negative']
    else:
        error_text = txt.MESSAGES['ege_invalid']

    try:
        await bot.edit_message_text(chat_id = msg.chat.id, message_id = ids[0], text = error_text)
    except Exception:
        pass


#обработчик пагинации
@router.callback_query(F.data.startswith('to_page_'))
async def back_to_buttons(call: CallbackQuery, state: FSMContext):
    await call.answer()
    
    is_catalog = call.data.endswith('_cat')    
    page = int(call.data.split('_')[2])
    data = await state.get_data()

    if is_catalog:
        await call.message.edit_reply_markup(reply_markup=kb.get_vuz_keyboard(None, page, 'all'))
    else:
        await call.message.edit_reply_markup(reply_markup=kb.get_vuz_keyboard(data.get('user_score'), page,
                                                                              data.get('user_direction')))


#обработчик карточки вуза 
@router.callback_query(F.data.startswith('vuz_'))
async def vuz_card(call: CallbackQuery, state: FSMContext):
    await call.answer()

    parts = call.data.split('_')
    vuz_id = parts[1]
    page = int(parts[2])
    dir_id = parts[3]
    is_catalog = len(parts) > 4 and parts[4] == 'cat' 

    vuz_data = serv.get_vuz_data(vuz_id)
    dir_data = serv.get_direction_data(vuz_id, dir_id)

    if not vuz_data or not dir_data:
        return

    data = await state.get_data()
    user_score = None if is_catalog else data.get('user_score') 

    if user_score:
        emoji, label = serv.zone_calc(user_score, dir_data.get('passing_score', 0))
        score_text = user_score
    else:
        emoji, label = '', ''
        score_text = 'без баллов'

    description = txt.MESSAGES['card_caption'].format(
        full_name = vuz_data.get('full_name', 'Пусто'),
        passing_score = dir_data.get('passing_score', 0),
        score = score_text,
        zone_emoji = emoji, 
        zone_label = label,
        description = vuz_data.get('description', 'Пусто'),
        direction_name = dir_data.get('name'),
        subjects = ", ".join(dir_data.get('subjects', []))
    )
    
    await call.message.edit_media(media = InputMediaPhoto(
            media = vuz_data['file_id'], 
            caption = description
        ),
        reply_markup = kb.get_vuz_card_keyboard(vuz_data, page, is_catalog))


#обработчик кнопки все вузы
@router.callback_query(F.data == 'menu_all')
async def all_vuz_button(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text(text = txt.MESSAGES['all_vuz_header'], reply_markup = kb.get_vuz_keyboard(None, 0, 'all'))


#обработчик кнопки назад к сетке вузов; нужен чтобы убирать описание вуза
@router.callback_query(F.data.startswith('to_grid_page_'))
async def back_to_grid_page(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.answer()

    is_catalog = call.data.endswith('_cat')
    
    clean_data = call.data.replace('_cat', '')
    page = int(clean_data.split('_')[3])
    
    data = await state.get_data()

    if is_catalog:
        user_score = None
        direction = 'all'
        text = txt.MESSAGES['all_vuz_header']
    else:
        user_score = data.get('user_score')
        direction = data.get('user_direction')
        dir_name = serv.get_direction_name(direction)
        text = txt.MESSAGES['grid_header'].format(score = user_score, direction_name = dir_name)

    message = await call.message.answer(text = text, reply_markup = kb.get_vuz_keyboard(user_score, page, direction))

    await serv.cleanup(state, bot, call.message.chat.id)

    await state.update_data(bot_message_ids=[message.message_id])


#обрабортчик для выхода в меню 
@router.callback_query(F.data == 'exit_to_menu')
async def exit_menu(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.answer()

    data = await state.get_data()

    message = await call.message.answer(text = txt.MESSAGES['start_msg'], reply_markup = kb.menu(data.get('user_score', None)))

    await serv.cleanup(state, bot, call.message.chat.id)
    await state.update_data(bot_message_ids = [message.message_id])
