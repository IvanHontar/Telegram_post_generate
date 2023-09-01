import logging
import aiohttp
import requests
from aiogram import Bot, Dispatcher, types
import openai
from config import OPEN_AI_KEY, BOT_TOKEN, DEEPAI_TOKEN

BOT_TOKEN = BOT_TOKEN
OPEN_AI_KEY = OPEN_AI_KEY
DEEPAI_TOKEN = DEEPAI_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

openai.api_key = OPEN_AI_KEY

logging.basicConfig(level=logging.INFO)


# photo generate func

async def image_generate(description):
    endpoint = "https://api.deepai.org/api/text2img"
    headers = {'api-key': DEEPAI_TOKEN}
    data = {'text': description}   

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, data=data) as response:
            if response.status == 200:
                result = await response.json()
                image_url = result.get('output_url')
                return image_url
            else:
                print('Erorr', await response.text())
                return None



class UserData:
    def __init__(self):
        self.project_description = None
        self.keywords = None

user_data = {}

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_data[message.from_user.id] = UserData()
    await message.reply("Привет! Для начала кратко опиши какой пост ты бы хотел сгенерировать?")

@dp.message_handler(lambda message: user_data[message.from_user.id].project_description is None)
async def get_project_description(message: types.Message):
    user_data[message.from_user.id].project_description = message.text
    await message.reply('Отлично! Теперь введите ключевые слова, которые вы бы хотели видеть в сгенерированном посте')

@dp.message_handler(lambda message: user_data[message.from_user.id].keywords is None)
async def generate_content(message: types.Message):
    user_data[message.from_user.id].keywords = message.text
    project_description = user_data[message.from_user.id].project_description
    keywords = user_data[message.from_user.id].keywords
    content_prompt = f"Project description {project_description} Please create a few sentences that describe the project concept and include this keywords  {keywords} "
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that generates clues for MidJourney AI."},
        {"role": "user", "content": content_prompt}
    ]
)

    
    content = response.choices[0].message['content'].strip()
    photo_url = await image_generate(content)

    if photo_url:
        await bot.send_photo(message.chat.id, photo=photo_url)
    else:
        await message.reply('Изображение не удалось сгенерировать')


    user_data[message.from_user.id]=UserData()


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
