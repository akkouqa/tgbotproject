<<<<<<< HEAD
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_sys import texts as txt
from bot_sys import data as db
from bot_sys import services as serv


#клавиатура для обработчика старта. пока что со всеми вузами и их подбором; просто меню
def menu(user_score):
    keyboard = InlineKeyboardBuilder()

    b1 = InlineKeyboardButton(text = txt.MESSAGES['menu_btn_pick'], callback_data = 'menu_pick')
    b2 = InlineKeyboardButton(text = txt.MESSAGES['menu_btn_all'], callback_data = 'menu_all')
    b3 = InlineKeyboardButton(text = txt.MESSAGES['menu_btn_about'], callback_data = 'about')

    keyboard.add(b1, b2).adjust(2)

    if user_score:
        keyboard.row(InlineKeyboardButton(text = txt.MESSAGES['menu_btn_change'].format(score = user_score),
                                          callback_data = 'score_change'), b3)
    else:
        keyboard.row(b3)
        
    return keyboard.as_markup()


#клавиатура для сборки сетки вузов
def get_vuz_keyboard(user_score, page, dir_id):
    keyboard = InlineKeyboardBuilder()

    if not dir_id:
        dir_id = 'all'
    
    all_vuz = serv.get_all_vuz()
    sorted_vuz = []

    for vuz in all_vuz:
        for dir in vuz.get('directions', []):
            if dir_id == 'all' or dir.get('id') == dir_id:
                if user_score:
                    circle, _ = serv.zone_calc(user_score, dir.get('passing_score', 0))
        
                    if circle == '🟢':
                        priority = 0
                    elif circle == '🟡':
                        priority = 1
                    else:
                        priority = 2
                else:
                    circle = ""
                    priority = 0 
            
                sorted_vuz.append((priority, vuz, circle, dir))

    if user_score:
        sorted_vuz.sort(key = lambda x: x[0])

    start = page * 6
    end = start + 6
    on_page = sorted_vuz[start:end]

    for priority, vuz, circle, dir in on_page:
        if user_score:
            text = f"{circle} {vuz.get('short_name', 'Пусто')} ({dir.get('name', 'Пусто')})"
            cb_data = f"vuz_{vuz.get('id')}_{page}_{dir.get('id')}"
        else:
            text = f"{vuz.get('short_name', 'Пусто')} ({dir.get('name', 'Пусто')})"
            cb_data = f"vuz_{vuz.get('id')}_{page}_{dir.get('id')}_cat"
            
        keyboard.button(text = text, callback_data = cb_data)

    keyboard.adjust(2)

    pag_buttons = []
    suf = '_cat' if not user_score else ''

    if page > 0:
        pag_buttons.append(InlineKeyboardButton(text = txt.MESSAGES['btn_prev_page'], callback_data = 
                                                f"to_page_{page - 1}{suf}"))
    
    if (page + 1) * 6 < len(sorted_vuz):
        pag_buttons.append(InlineKeyboardButton(text = txt.MESSAGES['btn_next_page'], callback_data = 
                                                f"to_page_{page + 1}{suf}"))

    if pag_buttons:
        keyboard.row(*pag_buttons)

    keyboard.row(InlineKeyboardButton(text = txt.MESSAGES['btn_main_menu'], callback_data = 'exit_to_menu'))

    return keyboard.as_markup()


#клавиатура для карточки вуза
def get_vuz_card_keyboard(vuz_data, page, is_catalog = False):
    keyboard = InlineKeyboardBuilder()

    suf = '_cat' if is_catalog else ''

    bt1 = InlineKeyboardButton(text = txt.MESSAGES['card_btn_back'], callback_data = f"to_grid_page_{page}{suf}")
    bt2 = InlineKeyboardButton(text = txt.MESSAGES['card_btn_site'], url = vuz_data.get('url', 'https://ya.ru'))

    keyboard.add(bt1, bt2).adjust(2)

    keyboard.row(InlineKeyboardButton(text = txt.MESSAGES['btn_main_menu'], callback_data = 'exit_to_menu'))

    return keyboard.as_markup()


#клавиатура для выбора направления
def get_direction_keyboard():
    keyboard = InlineKeyboardBuilder()

    uniq_dir = {}

    for vuz in serv.get_all_vuz():
        for direction in vuz.get('directions'):
            dir_name = direction.get('name')

            uniq_dir[direction.get('id')] = dir_name

    for id in list(uniq_dir.items()):
        keyboard.button(text = id[1], callback_data = f"vuz_direction_{id[0]}")

    keyboard.adjust(2)

    keyboard.row(InlineKeyboardButton(text = txt.MESSAGES['btn_all_directions'], callback_data = 'vuz_direction_all'))

    return keyboard.as_markup()
=======
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_sys import texts as txt
from bot_sys import data as db
from bot_sys import services as serv

#клавиатура для обработчика старта. пока что со всеми вузами и их подбором; просто меню
menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = txt.MESSAGES['menu_btn_pick'], callback_data = 'menu_pick'),
         InlineKeyboardButton(text = txt.MESSAGES['menu_btn_all'], callback_data = 'menu_all')]
    ]
)


#клавиатура для сборки сетки вузов
def get_vuz_keyboard(user_score, page):
    keyboard = InlineKeyboardBuilder()
    
    all_vuz = db.UNIVERSITIES
    sorted_vuz = []

    for vuz in all_vuz:
        if user_score:
            circle, _ = serv.zone_calc(user_score, vuz.get('passing_score', 0))
        
            if circle == '🟢':
                priority = 0
            elif circle == '🟡':
                priority = 1
            else:
                priority = 2
        else:
            circle = ""
            priority = 0 
            
        sorted_vuz.append((priority, vuz, circle))

    if user_score:
        sorted_vuz.sort(key = lambda x: x[0])

    start = page * 4
    end = start + 4
    on_page = sorted_vuz[start:end]

    for priority, vuz, circle in on_page:
        if user_score:
            text = f"{circle} {vuz.get('short_name', 'Пусто')}"
        else:
            text = vuz.get('short_name', 'Пусто')
            
        keyboard.button(text = text, callback_data = f"vuz_{vuz.get('id', None)}_{page}")

    keyboard.adjust(2)

    pag_buttons = []

    if page > 0:
        pag_buttons.append(InlineKeyboardButton(text = txt.MESSAGES['btn_prev_page'], callback_data = 
                                                f"to_page_{page - 1}"))
    
    if (page + 1) * 4 < len(sorted_vuz):
        pag_buttons.append(InlineKeyboardButton(text = txt.MESSAGES['btn_next_page'], callback_data = 
                                                f"to_page_{page + 1}"))

    if pag_buttons:
        keyboard.row(*pag_buttons)

    keyboard.row(InlineKeyboardButton(text = txt.MESSAGES['btn_main_menu'], callback_data = 'exit_to_menu'))

    return keyboard.as_markup()


#клавиатура для карточки вуза
def get_vuz_card_keyboard(vuz_data, page):
    keyboard = InlineKeyboardBuilder()

    bt1 = InlineKeyboardButton(text = txt.MESSAGES['card_btn_back'], callback_data = f"to_grid_page_{page}")
    bt2 = InlineKeyboardButton(text = txt.MESSAGES['card_btn_site'], url = vuz_data.get('url', 'https://ya.ru'))

    keyboard.add(bt1, bt2).adjust(2)

    keyboard.row(InlineKeyboardButton(text = txt.MESSAGES['btn_main_menu'], callback_data = 'exit_to_menu'))

    return keyboard.as_markup()
>>>>>>> 0dff2d58d5023ced76669f342a49bcb37339fe22
