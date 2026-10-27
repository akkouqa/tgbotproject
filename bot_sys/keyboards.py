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
