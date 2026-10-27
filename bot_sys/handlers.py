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
    message = await msg.answer(txt.MESSAGES['start_msg'], reply_markup = kb.menu)

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


#обработчик кнопки подобрать вуз
@router.callback_query(F.data == 'menu_pick')
async def menu_button_pick(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(st.InputScore.waiting_score)
    await call.message.edit_text(txt.MESSAGES['ask_ege'])


#обработчик баллов егэ пользователя и вывод сетки вузов как минимум пока что она будет вылетать сразу
@router.message(st.InputScore.waiting_score)
async def input_user_score(msg: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    ids = data.get('bot_message_ids', [])
    error_text = None
    
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
                                                text = txt.MESSAGES['grid_header'].format(score = user_score),
                                                reply_markup = kb.get_vuz_keyboard(user_score, 0))
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
    
    page = int(call.data.split('_')[2])
    data = await state.get_data()

    try:
        await call.message.edit_reply_markup(reply_markup = kb.get_vuz_keyboard(data.get('user_score', 0), page))
    except Exception:
        pass


#обработчик карточки вуза 
@router.callback_query(F.data.startswith('vuz_'))
async def vuz_card(call: CallbackQuery, state: FSMContext):
    await call.answer()
    
    vuz_id = call.data.split('_')[1]
    page = int(call.data.split('_')[2])

    vuz_data = None
    for v in db.UNIVERSITIES:
        if v['id'] == vuz_id:
            vuz_data = v
            break
            
    if not vuz_data:
        return

    data = await state.get_data()
    user_score = data.get('user_score') 

    if user_score:
        emoji, label = serv.zone_calc(user_score, vuz_data.get('passing_score', 0))
        score_text = user_score
    else:
        emoji, label = "", ""
        score_text = "не введены"

    description = txt.MESSAGES['card_caption'].format(
        full_name = vuz_data.get('full_name', 'Пусто'),
        passing_score = vuz_data.get('passing_score', 0),
        score = score_text,
        zone_emoji = emoji, 
        zone_label = label,
        description = vuz_data.get('description', 'Пусто')
    )
    
    await call.message.edit_media(media = InputMediaPhoto(
            media = vuz_data['file_id'], 
            caption = description
        ),
        reply_markup = kb.get_vuz_card_keyboard(vuz_data, page))


#обработчик кнопки все вузы
@router.callback_query(F.data == 'menu_all')
async def all_vuz_button(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text(text = txt.MESSAGES['all_vuz_header'], reply_markup = kb.get_vuz_keyboard(None, 0))


#обработчик кнопки назад к сетке вузов; нужен чтобы убирать описание вуза
@router.callback_query(F.data.startswith('to_grid_page_'))
async def back_to_grid_page(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.answer()

    page = int(call.data.split('_')[3])
    data = await state.get_data()

    if data.get('user_score'):
        text = txt.MESSAGES['grid_header'].format(score = data.get('user_score'))
        user_score = data.get('user_score')
    else:
        text = txt.MESSAGES['all_vuz_header']
        user_score = None

    message = await call.message.answer(text = text, reply_markup = kb.get_vuz_keyboard(user_score, page))

    await serv.cleanup(state, bot, call.message.chat.id)

    await state.update_data(bot_message_ids = [message.message_id])


#обрабортчик для выхода в меню 
@router.callback_query(F.data == 'exit_to_menu')
async def exit_menu(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.answer()

    data = await state.get_data()

    message = await call.message.answer(text = txt.MESSAGES['start_msg'], reply_markup = kb.menu)

    await serv.cleanup(state, bot, call.message.chat.id)
    await state.update_data(bot_message_ids = [message.message_id])
