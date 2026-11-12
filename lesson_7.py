import os
import ptbot


from pytimeparse import parse
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), 'Sens_inf.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

api_key = os.environ['TG_TOKEN']
ID_key = os.environ['TG_CHAT_ID']
bot = ptbot.Bot(api_key)


def notify(chat_id):
    bot.send_message(chat_id, "Время вышло!")


def render_progressbar(
    total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'
):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, chat_id, message_id, total_seconds):
    passed_seconds = total_seconds - secs_left
    progressbar = render_progressbar(total_seconds, passed_seconds)
    bot.update_message(
        chat_id, message_id, f"Осталось секунд: {secs_left}\n{progressbar}"
    )


def reply(chat_id, message):
    seconds = parse(message)
    message_id = bot.send_message(chat_id, "Запускаю таймер...")
    bot.create_countdown(
        seconds,
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        total_seconds=seconds,
    )
    bot.create_timer(seconds, notify, chat_id=chat_id)


def main():
    bot.reply_on_message(reply)
    bot.run_bot()


if __name__ == "__main__":
    main()
