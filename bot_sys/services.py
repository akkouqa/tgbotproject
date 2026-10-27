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
