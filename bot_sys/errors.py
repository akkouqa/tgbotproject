import logging
from aiogram import Bot
from aiogram.types import ErrorEvent
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext


async def error_handler(event: ErrorEvent, bot: Bot, state: FSMContext):
    if isinstance(event.exception, TelegramBadRequest):
        return

    logging.error(f"Ошибка при обработке апдейта: {event.exception}", exc_info = True)

    chat_id = None

    if event.update.message:
        chat_id = event.update.message.chat.id
    elif event.update.callback_query and event.update.callback_query.message:
        chat_id = event.update.callback_query.message.chat.id

    if chat_id:
        try:
            new_msg = await bot.send_message(
                chat_id = chat_id, 
                text='😔 Извините, произошла техническая ошибка. Пожалуйста, попробуйте выбрать действие еще раз или напишите /start.'
            )
            
            if state:
                try:
                    data = await state.get_data()
                    msg_ids = data.get('bot_message_ids', [])
                    msg_ids.append(new_msg.message_id)
                    await state.update_data(bot_message_ids = msg_ids)
                except Exception as e:
                    logging.error(f"Не удалось сохранить ID сообщения об ошибке: {e}")

        except Exception as e:
            logging.error(f"Не удалось отправить сообщение об ошибке: {e}")
