import discord
from discord import app_commands
import random
import datetime
import asyncio
import jpgrammar
import jp_vocabulary
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
    jp_vocabulary.initialize()

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
    
    await bot.process_commands(message) 



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

@bot.tree.command(name="jp_grammar_search", description="搜尋日文文法")
@app_commands.describe(keyword="輸入關鍵字")
async def search_jpgrammar(interaction: discord.Interaction, keyword: str):
    result = []
    channel = bot.get_channel(interaction.channel_id)
    await interaction.response.send_message(f"正在搜尋包含{keyword}的內容...")
    await asyncio.sleep(1)
    for title in jpgrammar_all[3]:
        if keyword in title:
            result.append(title)
    if len(result) == 0:
        await interaction.edit_original_response("查無結果")
        return
    await interaction.edit_original_response(content=f"找到{len(result)}則相關內容")
    for title in result:
        await channel.send(jpgrammar_all[3][title])


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
                await message.clear_reactions()
                random_grammar = random.choice(rand_list)
                await message.edit(content=f"正在重新推薦一部{list_name}文法影片給{customer}")
                await asyncio.sleep(1)
                await message.edit(content = f'推薦內容{random_grammar}\n請問要換下一個嗎?(請在一分鐘內按表符)')
                await message.add_reaction('✅')
                await message.add_reaction('❌')
            elif str(reaction.emoji) == '❌':
                await message.clear_reactions()
                grammar_value = jpgrammar_all[lvl][random_grammar]
                await message.edit(content=f'推薦內容: {random_grammar}\n網址: {grammar_value}')
                break
        except asyncio.TimeoutError:
            await message.clear_reactions()
            await message.edit(content='操作超時。請不要浪費我時間。')
            break

@bot.tree.command(name='japanese_vocabulary', description='日文單字庫系統')
@app_commands.describe(reqcode='功能')
@app_commands.choices(reqcode=[
    app_commands.Choice(name='使用者註冊', value=0),
    app_commands.Choice(name='新增單字', value=1),
    app_commands.Choice(name='刪除單字', value=2),
    app_commands.Choice(name='新增例句', value=3),
    app_commands.Choice(name='查詢單字資訊', value=7),
    app_commands.Choice(name='查詢單字數量', value=4),
    app_commands.Choice(name='單字列表', value=5),
    app_commands.Choice(name='隨機抽單字', value=6),
])

async def jp_voc(interaction: discord.Interaction, reqcode: app_commands.Choice[int]):
    def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel
    
    v = reqcode.value
    user_name = interaction.user.name
    if v == 0:
        if jp_vocabulary.add_user(user_name):
            await interaction.response.send_message(f"{user_name}已成功新增至資料庫")
        else:
            await interaction.response.send_message(f"該使用者已存在")
        
                                                
    elif v == 1:
        await interaction.response.send_message("請輸入你要新增的單字、假名和意思(用空格隔開)")
        try:
            msg = await bot.wait_for('message', timeout=60.0, check=check)
            user_input = msg.content
            word = user_input.split()
            if len(word)!=3:
                await interaction.followup.send(f"輸入格式錯誤")
            else:
                await interaction.followup.send(jp_vocabulary.add_voc(user_name, word))
            
        except asyncio.TimeoutError:
            await interaction.followup.send("請求超時，請重新執行命令。")

    elif v == 2:
        await interaction.response.send_message("請輸入你要刪除的單字")
        try:
            msg = await bot.wait_for('message', timeout=60.0, check=check)
            user_input = msg.content
            await interaction.followup.send(jp_vocabulary.del_voc(user_name, user_input))
            
        except asyncio.TimeoutError:
            await interaction.followup.send("請求超時，請重新執行命令。")

    elif v == 3:
        voc = ""
        sentence = ""
        await interaction.response.send_message("請輸入要加入的單字")
        try:
            msg = await bot.wait_for('message', timeout=60.0, check=check)
            voc = msg.content
        except asyncio.TimeoutError:
            await interaction.followup.send("請求超時，請重新執行命令。")
        await interaction.followup.send("請輸入例句。")
        try:
            msg = await bot.wait_for('message', timeout=60.0, check=check)
            sentence = msg.content
        except asyncio.TimeoutError:
            await interaction.followup.send("請求超時，請重新執行命令。")
        await interaction.followup.send(jp_vocabulary.add_sentence(user_name, voc, sentence))
        
    elif v == 4:
        await interaction.response.send_message(jp_vocabulary.inquire_voc_num(user_name)) 
    elif v == 5:
        await interaction.response.send_message(jp_vocabulary.voc_list(user_name)) 
    elif v == 6:
        await interaction.response.send_message(jp_vocabulary.voc_test(user_name))
    elif v == 7:
        voc = ""
        await interaction.response.send_message("請輸入要查詢的單字")
        try:
            msg = await bot.wait_for('message', timeout=60.0, check=check)
            voc = msg.content
        except asyncio.TimeoutError:
            await interaction.followup.send("請求超時，請重新執行命令。")
        await interaction.followup.send(jp_vocabulary.inquire_voc_info(user_name, voc))



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