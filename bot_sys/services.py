<<<<<<< HEAD
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot_sys import data as db


#функция для удаления старых сообщений
async def cleanup(state: FSMContext, bot: Bot, chat_id):
    data = await state.get_data()
    messages_ids = data.get('bot_message_ids', [])
    
    if messages_ids:
        for msg_id in messages_ids:
            try:
                await bot.delete_message(message_id = msg_id, chat_id = chat_id)
            except Exception:
                pass
    await state.update_data(bot_message_ids = [])


#функция для удаления сообщения пользователя
async def delete_user_msg(msg: Message):
    try:
        await msg.delete()
    except Exception:
        pass


#функция для расчета цветовой зоны
def zone_calc(user_score, pass_score):
    diff = user_score - pass_score
    if diff >= 15:
        return '🟢', '(Безопасно)'
    elif -5 <= diff <= 14:
        return '🟡', '(На грани)'
    else:
        return '🔴', '(Риск)' 


#функция для получения название направления
def get_direction_name(dir_id):
    if not dir_id or dir_id == 'all':
        return 'Все направления'
        
    for vuz in db.UNIVERSITIES:
        for dir in vuz.get('directions', []):
            if dir.get('id') == dir_id:
                return dir.get('name')
                
    return 'Неизвестное направление'


#функция для получения всех вузов нужна для легкого переноса на sql
def get_all_vuz():
    return db.UNIVERSITIES


#функция для получения вуза по айди
def get_vuz_data(vuz_id):
    for vuz in get_all_vuz():
        if vuz.get('id') == vuz_id:
            return vuz 
    return None


#функция для получения словаря с данными конкретного направления
def get_direction_data(vuz_id, dir_id):
    vuz = get_vuz_data(vuz_id)

    if vuz:
        for dir in vuz.get('directions', []):
            if dir.get('id') == dir_id:
                return dir
        return None
=======
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


#функция для удаления старых сообщений
async def cleanup(state: FSMContext, bot: Bot, chat_id):
    data = await state.get_data()
    messages_ids = data.get('bot_message_ids', [])
    
    if messages_ids:
        for msg_id in messages_ids:
            try:
                await bot.delete_message(message_id = msg_id, chat_id = chat_id)
            except Exception:
                pass
    await state.update_data(bot_message_ids = [])


#функция для удаления сообщения пользователя
async def delete_user_msg(msg: Message):
    try:
        await msg.delete()
    except Exception:
        pass


#функция для расчета цветовой зоны
def zone_calc(user_score, pass_score):
    diff = user_score - pass_score
    if diff >= 15:
        return '🟢', '(Безопасно)'
    elif -5 <= diff <= 14:
        return '🟡', '(На грани)'
    else:
        return '🔴', '(Риск)' 
>>>>>>> 0dff2d58d5023ced76669f342a49bcb37339fe22
