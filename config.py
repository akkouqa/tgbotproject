<<<<<<< HEAD
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
=======
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
>>>>>>> 0dff2d58d5023ced76669f342a49bcb37339fe22
    raise RuntimeError('токен бота не найден')