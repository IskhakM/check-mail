import asyncio
import os
from aiogram import Bot
from dotenv import load_dotenv


load_dotenv()


API_TOKEN = os.getenv('API_TOKEN')
USER_ID = os.getenv('USER_ID')


async def send_text_from_file(file_path: str):
    if not os.path.exists(file_path):
        print(f'Файл {file_path} не найден')
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    bot = Bot(token=API_TOKEN)

    try:
        await bot.send_message(
            chat_id=USER_ID,
            text=content
        )
        print('Сообщение успешно улетело в Telegram!')
    except Exception as e:
        print(f'Что-то пошло не так: {e}')
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(send_text_from_file('message.txt'))
