import asyncio
import logging
import re
import sqlite3
import datetime
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализируем бота
TOKEN = "YOUR_BOT_TOKEN"  # Замени на свой токен
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Класс для работы с базой данных
class ReminderDB:
    def __init__(self, db_name='reminders.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            reminder_text TEXT NOT NULL,
            reminder_time TIMESTAMP NOT NULL,
            is_sent BOOLEAN DEFAULT 0
        )
        ''')
        conn.commit()
        conn.close()
    
    def add_reminder(self, user_id, reminder_text, reminder_time):
        """Добавление напоминания в базу данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO reminders (user_id, reminder_text, reminder_time) VALUES (?, ?, ?)',
            (user_id, reminder_text, reminder_time)
        )
        reminder_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return reminder_id
    
    def get_active_reminders(self):
        """Получение всех активных напоминаний"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, user_id, reminder_text, reminder_time FROM reminders WHERE is_sent = 0'
        )
        reminders = cursor.fetchall()
        conn.close()
        return reminders
    
    def get_user_reminders(self, user_id):
        """Получение всех напоминаний пользователя"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, reminder_text, reminder_time FROM reminders WHERE user_id = ? AND is_sent = 0 ORDER BY reminder_time',
            (user_id,)
        )
        reminders = cursor.fetchall()
        conn.close()
        return reminders
    
    def mark_reminder_as_sent(self, reminder_id):
        """Отметка напоминания как отправленного"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE reminders SET is_sent = 1 WHERE id = ?',
            (reminder_id,)
        )
        conn.commit()
        conn.close()

# Создаем экземпляр базы данных
db = ReminderDB()

# Функция для парсинга текста и времени напоминания
def parse_reminder(text):
    """
    Парсит текст напоминания и время из сообщения пользователя.
    Поддерживает форматы:
    - через X часов/часа/час
    - через X минут/минуты/минуту
    - через X секунд/секунды/секунду
    """
    # Паттерны для поиска времени
    time_patterns = [
        (r'через (\d+)\s+час(ов|а|)?', 'hours'),
        (r'через (\d+)\s+минут(у|ы|)?', 'minutes'),
        (r'через (\d+)\s+секунд(у|ы|)?', 'seconds'),
    ]
    
    reminder_text = text
    reminder_time = None
    
    # Ищем все паттерны времени
    for pattern, time_unit in time_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Извлекаем количество времени
            amount = int(match.group(1))
            
            # Вычисляем время напоминания
            if time_unit == 'hours':
                delta = datetime.timedelta(hours=amount)
            elif time_unit == 'minutes':
                delta = datetime.timedelta(minutes=amount)
            else:  # seconds
                delta = datetime.timedelta(seconds=amount)
            
            reminder_time = datetime.datetime.now() + delta
            
            # Удаляем информацию о времени из текста напоминания
            reminder_text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
            break
    
    if reminder_time:
        # Очищаем текст от лишних слов и символов
        reminder_text = re.sub(r'^напомни\s*', '', reminder_text, flags=re.IGNORECASE).strip()
        reminder_text = re.sub(r'^напоминание\s*', '', reminder_text, flags=re.IGNORECASE).strip()
        reminder_text = re.sub(r'^\s*:\s*', '', reminder_text).strip()
        
        return reminder_text, reminder_time
    
    return None, None

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обрабатывает команду /start"""
    await message.answer(
        "👋 Привет! Я бот для напоминаний.\n\n"
        "Чтобы создать напоминание, напиши, например:\n"
        "- Позвонить маме через 1 час\n"
        "- Напомни через 10 минут: выпить воду\n"
        "- Купить молоко через 2 часа\n\n"
        "Чтобы увидеть список всех напоминаний, введи /list"
    )

# Обработчик команды /list
@router.message(Command("list"))
async def cmd_list(message: Message):
    """Обрабатывает команду /list и показывает список активных напоминаний"""
    user_id = message.from_user.id
    reminders = db.get_user_reminders(user_id)
    
    if not reminders:
        await message.answer("📭 У вас нет активных напоминаний.")
        return
    
    response = "📋 Ваши активные напоминания:\n\n"
    for i, reminder in enumerate(reminders, 1):
        reminder_id, reminder_text, reminder_time_str = reminder
        try:
            reminder_time = datetime.datetime.strptime(reminder_time_str, "%Y-%m-%d %H:%M:%S")
            time_str = reminder_time.strftime("%d.%m.%Y %H:%M")
            response += f"{i}. {reminder_text} - {time_str}\n"
        except ValueError:
            response += f"{i}. {reminder_text} - время неизвестно\n"
    
    await message.answer(response)

# Обработчик обычных сообщений (для создания напоминаний)
@router.message(F.text)
async def handle_reminder(message: Message):
    """Обрабатывает текстовые сообщения и создает напоминания"""
    text = message.text
    user_id = message.from_user.id
    
    # Парсим текст и время напоминания
    reminder_text, reminder_time = parse_reminder(text)
    
    if reminder_text and reminder_time:
        # Добавляем напоминание в базу данных
        reminder_id = db.add_reminder(user_id, reminder_text, reminder_time.strftime("%Y-%m-%d %H:%M:%S"))
        
        # Отправляем подтверждение
        time_str = reminder_time.strftime("%d.%m.%Y %H:%M")
        await message.answer(f"✅ Хорошо! Я напомню вам:\n\n«{reminder_text}»\n\nВремя: {time_str}")
        
        # Запускаем задачу для отправки напоминания
        asyncio.create_task(send_reminder_at_time(reminder_id, user_id, reminder_text, reminder_time))
    else:
        await message.answer(
            "❓ Не могу понять, когда нужно напомнить. Пожалуйста, укажите время в формате:\n"
            "- через X часов\n"
            "- через X минут\n"
            "- через X секунд\n\n"
            "Например: Позвонить маме через 1 час"
        )

# Асинхронная функция для отправки напоминания в заданное время
async def send_reminder_at_time(reminder_id, user_id, reminder_text, reminder_time):
    """Отправляет напоминание пользователю в указанное время"""
    # Вычисляем, сколько нужно ждать
    now = datetime.datetime.now()
    wait_time = (reminder_time - now).total_seconds()
    
    if wait_time > 0:
        try:
            await asyncio.sleep(wait_time)
            await bot.send_message(user_id, f"⏰ НАПОМИНАНИЕ: {reminder_text}")
            db.mark_reminder_as_sent(reminder_id)
        except Exception as e:
            logging.error(f"Ошибка при отправке напоминания: {e}")
    else:
        # Если время уже прошло, отправляем сразу
        try:
            await bot.send_message(user_id, f"⏰ НАПОМИНАНИЕ (задержано): {reminder_text}")
            db.mark_reminder_as_sent(reminder_id)
        except Exception as e:
            logging.error(f"Ошибка при отправке задержанного напоминания: {e}")

# Функция для восстановления напоминаний при запуске бота
async def restore_reminders():
    """Восстанавливает напоминания из базы данных при запуске бота"""
    logging.info("Восстанавливаем сохраненные напоминания...")
    reminders = db.get_active_reminders()
    count = 0
    
    for reminder in reminders:
        reminder_id, user_id, reminder_text, reminder_time_str = reminder
        try:
            reminder_time = datetime.datetime.strptime(reminder_time_str, "%Y-%m-%d %H:%M:%S")
            
            # Проверяем, не прошло ли уже время напоминания
            now = datetime.datetime.now()
            if reminder_time > now:
                # Если нет, запускаем задачу
                asyncio.create_task(send_reminder_at_time(reminder_id, user_id, reminder_text, reminder_time))
                count += 1
            else:
                # Если да, отправляем напоминание сразу с пометкой о задержке
                delay = now - reminder_time
                delay_minutes = delay.total_seconds() // 60
                
                message = f"⏰ НАПОМИНАНИЕ (пропущено на {int(delay_minutes)} мин): {reminder_text}"
                await bot.send_message(user_id, message)
                db.mark_reminder_as_sent(reminder_id)
                count += 1
        except Exception as e:
            logging.error(f"Ошибка при восстановлении напоминания: {e}")
    
    logging.info(f"Восстановлено {count} напоминаний")

# Функция для запуска бота
async def main():
    """Основная функция для запуска бота"""
    logging.info("Запускаем бот...")
    
    # Восстанавливаем напоминания
    await restore_reminders()
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())