#import
import discord
from  dotenv import load_dotenv
import os
from discord.ext import commands
import time
import schedule
from langchain.llms import OpenAI
import openai

# .env
load_dotenv()

# discord
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.Model.retrieve("gpt-3.5-turbo")

chat_channel = os.getenv("CHAT_CHANNEL")
# bot online
@bot.event
async def on_ready():
    print(f">>> {bot.user} is ready <<<")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("弄ChatGPT"))

# slash-ping
@bot.command(description="確認機器人在線狀況")
async def ping(ctx): 
    await ctx.respond(f"Pong! 我還在線喔！")

# @bot.command(description="向機器人問問題")
# async def q(ctx, question):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "user", "content": "%s, 用中文回答" % (question)}
#         ]
#     )
#     completed_text = response["choices"][0]["message"]["content"]
#     await ctx.respond(completed_text)

@bot.event
async def on_message(message):
    channel = bot.get_channel(chat_channel)
    # 确保机器人不会响应自己的消息
    if message.author != bot.user:
        if message.content.startswith('http'):
            return
        else:
            if message.channel.id == chat_channel:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": "%s, 用中文在20字以內接續聊天, 你叫SlimeChat, 如果被問到\"你是誰\"等問題就回答\"我是SlimeChat 很開心和你聊天\" " % (message.content)}
                    ],
                    max_tokens = 35
                )
                completed_text = response["choices"][0]["message"]["content"]
                await channel.send(completed_text)
    else:
        return
    # 处理收到的消息
    

bot.run(os.getenv('TOKEN'))