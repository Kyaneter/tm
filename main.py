from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime
import asyncio


async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Парсим аргументы: /remind <время> <текст>
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("❌ Используй: /remind <время ЧЧ:ММ> <текст напоминания>")
            return

        time_str = args[0]
        text = " ".join(args[1:])

        # Преобразуем время
        now = datetime.datetime.now()
        remind_time = datetime.datetime.strptime(time_str, "%H:%M").replace(
            year=now.year,
            month=now.month,
            day=now.day
        )

        # Если время уже прошло сегодня, переносим на завтра
        if remind_time < now:
            remind_time += datetime.timedelta(days=1)

        # Вычисляем задержку в секундах
        delta = (remind_time - now).total_seconds()

        # Создаем задачу
        async def send_reminder():
            await asyncio.sleep(delta)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"⏰ Напоминание: {text}"
            )

        asyncio.create_task(send_reminder())
        await update.message.reply_text(f"✅ Напоминание установлено на {time_str}!")

    except ValueError:
        await update.message.reply_text("❌ Неправильный формат времени! Используй ЧЧ:ММ")


def main():
    application = Application.builder().token("8138336556:AAHwfihp6Er6q_TlQwEB4UHTKwIajqO_X7w").build()
    application.add_handler(CommandHandler("remind", remind))
    application.run_polling()


if __name__ == "__main__":
    main()
