import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
from datetime import datetime, timedelta
import openai
import asyncio

# .env
load_dotenv()

# discord
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

chat_channel = int(os.getenv("CHAT_CHANNEL"))  # 将字符串转换为整数类型
user_message_tracker = {}  # 用于跟踪用户的消息时间戳

@bot.event
async def on_ready():
    print(f">>> {bot.user} is ready <<<")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("弄ChatGPT"))

@bot.command(description="確認機器人在線狀況")
async def ping(ctx):
    await ctx.respond(f"Pong! 我還在線喔！")

@bot.event
async def on_message(message):
    channel = bot.get_channel(chat_channel)
    # 确保机器人不会响应自己的消息
    if message.author != bot.user:
        if message.content.startswith('http'):
            return
        else:
            if message.channel.id == chat_channel:
                # 设置限制的时间间隔（15秒）
                cooldown = timedelta(seconds=15)
                
                # 检查消息发送者是否已经在字典中
                if message.author.id in user_message_tracker:
                    # 获取上一次消息的时间戳
                    last_message_time = user_message_tracker[message.author.id]
        
                    # 计算距离上一次消息的时间间隔
                    time_elapsed = datetime.now() - last_message_time
        
                    # 如果时间间隔在限制范围内，则发送警示消息
                    if time_elapsed < cooldown:
                        warning_message = await channel.send("OpenAI Key 调用频率过高，请稍后再试")
                        
                        # 延迟3秒后删除警示消息
                        await asyncio.sleep(3)
                        await warning_message.delete()
                        return
                
                # 更新用户的消息时间戳为当前时间
                user_message_tracker[message.author.id] = datetime.now()

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": "%s, 用中文在20字以內接續聊天, 你叫SlimeChat, 如果被問到\"你是誰\"等問題就回答\"我是SlimeChat 很開心和你聊天\" " % (message.content)}
                    ],
                    max_tokens=35
                )
                completed_text = response["choices"][0]["message"]["content"]
               
                
                await channel.send(completed_text)
                
    else:
        return




bot.run(os.getenv('TOKEN'))
