import discord
from discord import app_commands
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

keywords_responses = {
    '狗叫': '汪汪汪',
}

f = open("tk.txt")
token = f.read()
f.close

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f'Logged in as {bot.user}')
    print(f"Loading {len(slash)} slash commands")

@bot.event
async def on_message(message):
    print(f'Received message: {message.content} from {message.author}')  # 調試信息

    if message.author == bot.user:
        return  # 防止機器人回應自己


    for keyword, response in keywords_responses.items():
        if keyword in message.content.lower() and not message.content.startswith(bot.command_prefix):
            await message.channel.send(response)
            break  # 如果找到匹配的關鍵字，就停止搜尋

    await bot.process_commands(message)  # 確保命令仍然可以正常工作


# 註冊 slash command
@bot.tree.command(name="truth")
async def truth(interaction: discord.Interaction):
    await interaction.response.send_message("Ranger is handsome")

@bot.tree.command(name="nottruth")
async def nottruth(interaction: discord.Interaction):
    await interaction.response.send_message("py is handsome")




@bot.command()

async def yesorno(ctx, *, question=None):
    if question is None:
        await ctx.send('你想問啥?')
    elif "吳哲愷帥" in question:
        await ctx.send("Yes")
    else:
        response = random.choice(['Yes', 'No'])
        await ctx.send(response)
    
#async def japanesegrammar()



bot.run(token)