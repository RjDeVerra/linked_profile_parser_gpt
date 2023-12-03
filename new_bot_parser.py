from aiogram import Bot, Dispatcher, executor, types
import re
import requests
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import load_tools
from langchain.agents import initialize_agent
import json
import os
import openai

API_TOKEN = ""
api_key = ""
openai_api_key = ""

os.environ["OPENAI_API_KEY"] = openai_api_key
openai.api_key = os.getenv('OPENAI_API_KEY')

headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_message(message: types.Message):
   await message.answer(text="Пришлите ссылку на профиль LinkedIn")

@dp.message_handler(content_types=["text"])
async def send_message(message: types.Message):
	try:
		re.search("(?P<url>https?://[^\\s]+)", message.text).group("url")
		linkedin_profile_url = message.text
		response = requests.get(api_endpoint,
                        params={'url': linkedin_profile_url},
                        headers=headers)

		data = json.loads(response.text)
		completion = openai.ChatCompletion.create(
		  model = 'gpt-4',
		  messages = [
		    {'role': 'user', 'content': 'У меня есть заказчик с таким описанием: {}. Составь предложение от компании HappyAI на внедрение AI в его бизнес. Спасибо'.format(data["headline"])}
		  ],
		  temperature = 0  
		)
		openai_function = completion['choices'][0]['message']['content']
		exec(openai_function)
		await message.answer(openai_function)
	except:
		await message.answer("Пришлите ссылку!")


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
