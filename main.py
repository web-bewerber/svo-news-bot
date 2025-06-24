import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import telegram

# 🔐 Загружаем ключи из переменных окружения
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

client = OpenAI(api_key=OPENAI_API_KEY)

# 📅 Дата сводки
date = "23-06-2025"
url = f"https://lostarmour.info/summary/voyna-na-ukraine-svodka-za-{date}"

# 📥 Парсим страницу
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
content_blocks = []
for block in soup.find_all(["h2", "p"]):
    text = block.get_text(strip=True)
    if text:
        content_blocks.append(text)
sample_text = "\n".join(content_blocks[:6])

# 🧠 GPT-запрос
prompt = f"""
Ты — редактор новостного блога. На основе сводки событий за {date} создай связный, уникальный и хорошо читаемый новостной пост для сайта. Используй вводное предложение и завершение. Избегай повторов.

Сводка:
{sample_text}
"""

chat_completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Ты опытный редактор военных новостей."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=700,
)

generated_text = chat_completion.choices[0].message.content

# 🚀 Отправка в Telegram
bot = telegram.Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHAT_ID, text=generated_text, parse_mode="HTML")
