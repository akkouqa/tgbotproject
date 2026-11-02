<<<<<<< HEAD
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from bot_sys import services as serv
from bot_sys import texts as txt


router = Router()


#обработчик который удаляет все случайные сообщения юзера
@router.message()
async def flood_message(msg: Message):
    await serv.delete_user_msg(msg)


#обработчик для случайных нажатий по старым инлайн кнопкам
@router.callback_query()
async def flood_buttons(call: CallbackQuery):
    await call.answer(text = txt.MESSAGES['stale_callback'], show_alert = True)
=======
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from bot_sys import services as serv
from bot_sys import texts as txt


router = Router()


#обработчик который удаляет все случайные сообщения юзера
@router.message()
async def flood_message(msg: Message):
    await serv.delete_user_msg(msg)


#обработчик для случайных нажатий по старым инлайн кнопкам
@router.callback_query()
async def flood_buttons(call: CallbackQuery):
    await call.answer(text = txt.MESSAGES['stale_callback'], show_alert = True)
>>>>>>> 0dff2d58d5023ced76669f342a49bcb37339fe22
