import discord
from discord import app_commands
import random
import datetime
import asyncio
import jpgrammar
import stocks_news_crawler
from discord.ext import commands, tasks
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger



intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

keywords_responses = {
    '狗叫': '汪汪汪',
}

@tasks.loop(minutes=1) 
async def send_daily_stock_news():
    now = datetime.datetime.now()
    if now.hour == 1 and now.minute == 0:
        channel = bot.get_channel(1266418314322907158)
        if channel:
            new_lists = stocks_news_crawler.get_news_list()
            await channel.send("以下是最新股市新聞\n")
            for i in new_lists:
                await channel.send(i)

f = open("tk.txt")
token = f.read()
f.close

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f'Logged in as {bot.user}')
    print(f"Loading {len(slash)} slash commands")
    jpgrammar.file_process()
    global jpgrammar_all
    jpgrammar_all = [jpgrammar.N1, jpgrammar.N2, jpgrammar.N3, jpgrammar.N123]
    print("已載入日檢文法清單")
    send_daily_stock_news.start()

@bot.event
async def on_message(message):
    print(f'Received message: {message.content} from {message.author}')  # 調試信息

    if message.author == bot.user:
        return  # 防止機器人回應自己


    for keyword, response in keywords_responses.items():
        if keyword in message.content.lower() and not message.content.startswith(bot.command_prefix):
            await message.channel.send(response)
            break  # 如果找到匹配的關鍵字，就停止搜尋
    
    if message.channel.id == 1266659148154802186:
        channel = bot.get_channel(1266659148154802186)
        cont = message.content
        await message.delete()
        await channel.send(f"```{cont}```")
    
    await bot.process_commands(message)  # 確保命令仍然可以正常工作



@bot.tree.command(name="truth")
async def truth(interaction: discord.Interaction):
    await interaction.response.send_message("Ranger is handsome")


@bot.tree.command(name="randnum", description="get a random number")
@app_commands.describe(start="from", end="to")
async def getrandnum(interaction: discord.Interaction, start: int, end: int):
    channel = bot.get_channel(interaction.channel_id)
    await interaction.response.send_message(f"正在從 {start} 到 {end} 中挑一個數字")
    await asyncio.sleep(1)
    if start>end:
        await channel.send("不要耍白癡")
        return
    await channel.send("施法中...")
    await asyncio.sleep(1)
    await channel.send(random.randint(start, end))



@bot.tree.command(name='japanese_grammar', description='學習日文文法')
@app_commands.describe(level='級別')
@app_commands.choices(level=[
    app_commands.Choice(name='N1', value=0),
    app_commands.Choice(name='N2', value=1),
    app_commands.Choice(name='N3', value=2),
    app_commands.Choice(name='隨機', value=3),
])

async def jp_grammar(interaction: discord.Interaction, level: app_commands.Choice[int]):

    def check(reaction, user):
        return user == interaction.user and str(reaction.emoji) in ['✅', '❌'] and reaction.message.id == message.id
    
    customer = interaction.user.name
    lvl = level.value
    list_name = 'N'+str(lvl+1)
    rand_list = list(jpgrammar_all[lvl].keys())
    if lvl == 3:
        list_name = "隨機"
    
    await interaction.response.send_message(f"正在隨機推薦一部{list_name}文法影片給{customer}")
    message = await interaction.original_response()
    random_grammar = random.choice(rand_list)
    await asyncio.sleep(1)
    await message.edit(content = f'推薦內容{random_grammar}\n請問要換下一個嗎?(請在一分鐘內按表符)')
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    
    
    while(1):
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == '✅':
                # 用户点击了打勾，重新推荐
                await message.clear_reactions()
                random_grammar = random.choice(rand_list)
                await message.edit(content=f"正在重新推薦一部{list_name}文法影片給{customer}")
                await asyncio.sleep(1)
                await message.edit(content = f'推薦內容{random_grammar}\n請問要換下一個嗎?(請在一分鐘內按表符)')
                await message.add_reaction('✅')
                await message.add_reaction('❌')
            elif str(reaction.emoji) == '❌':
                # 用户点击了叉叉，输出当前键的值
                await message.clear_reactions()
                grammar_value = jpgrammar_all[lvl][random_grammar]
                await message.edit(content=f'推薦內容: {random_grammar}\n網址: {grammar_value}')
                break
        except asyncio.TimeoutError:
            await message.clear_reactions()
            await message.edit(content='操作超時。請不要浪費我時間。')
            break
    



@bot.command()
async def yesorno(ctx, *, question=None):
    if question is None:
        await ctx.send('你想問啥?')
    elif "吳哲愷帥" in question:
        await ctx.send("Yes")
    else:
        response = random.choice(['Yes', 'No'])
        await ctx.send(response)
    



bot.run(token)