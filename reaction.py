#Discord.py v1.7
import discord
import asyncio
import pickle
import os
import sys
from discord.ext import tasks
from datetime import datetime
GLOBAL_CH_NAME = "限界やちゃっと"
GLOBAL_WEBHOOK_NAME = "genkaichat-Webhook"
client = discord.Client(intents=discord.Intents.all())
setting = open('token.txt', 'r').readlines()
Token = setting[0]
Genkaiya_emoji = "<:genkaiya:1003377706521600042>"
genkaiwordlist = ["限界","げんかい","limit","極限","無理","極限","ダメ","駄目","genkai","文鎮","壊れ","ゴミだ","つらい","くそ"]

global gencount
# 限界カウンター Start
try:
    with open('gencount.pickle', 'rb') as f:
      try:
          gencount = pickle.load(f)
      except EOFError:
          gencount = 0
except FileNotFoundError:
    with open("gencount.pickle","wb") as f:
        gencount = 0
        pickle.dump(gencount, f)
        print("gencount ファイルを作成したから再起動するや...")
        python = sys.executable
        os.execl(python,python, * sys.argv)

@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    print(now)
    if now == '22:00':
        ch_name = "限界やちゃっと"
        global gencount
        msg = f"今日の全世界での限界やちゃん出現数は{gencount}回や...！\n明日はどうなるかや...おやすみや..."
        for channel in client.get_all_channels():
            if channel.name == ch_name:
                try:
                    await channel.send(msg)
                except discord.errors.Forbidden:
                    pass
                with open("gencount.pickle","wb") as f:
                    gencount = 0
                    pickle.dump(gencount, f)
loop.start()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    #mension
    if message.author.bot or message.author.discriminator == "0000":
        return
    user_data_text = open('user.txt', 'r')
    user_data = user_data_text.readlines()
    user_data_text.close()
    count = 0
    for raw_data in user_data:
        server_id = message.guild.id
        user_id = message.author.id
        data = raw_data.split(",")
        if count > 100:
            break
        elif server_id == int(data[0]):
            if user_id == int(data[1]):
                await message.add_reaction(Genkaiya_emoji)
        count += 1
    for word in genkaiwordlist:
        if word in message.content:
            await message.add_reaction(Genkaiya_emoji)
            with open("gencount.pickle","wb") as f:
                global gencount
                gencount += 1
                pickle.dump(gencount, f)
                print(gencount)
            break
    if message.author.discriminator == "0000":return
    if message.channel.name == GLOBAL_CH_NAME:
        channels = client.get_all_channels()
        global_channels = [ch for ch in channels if ch.name == GLOBAL_CH_NAME]
        try:
            await message.add_reaction(loading_emoji)
        except:pass
        for channel in global_channels:
            if channel.id == message.channel.id:continue
            try:
               ch_webhooks = await channel.webhooks()
            except discord.errors.Forbidden:continue
            if ch_webhooks == []:
                try:webhook = await channel.create_webhook(name=GLOBAL_WEBHOOK_NAME, reason=f"{GLOBAL_CH_NAME}の為にwebhook作成したや...")
                except:continue
            else:
                webhook = ch_webhooks[0]
            content = message.content.replace("@", "＠")
            if content == "":content = "メッセージ内容がありません"
            for attachment in message.attachments:
                content = content + "\n" + attachment.url
            try:
                await webhook.send(content=content,
                    username=f"{message.author} from {message.guild}",
                    avatar_url=message.author.avatar_url_as(format="png"),
                    embed=message.embeds[0])
            except:
                await webhook.send(content=content,
                    username=f"{message.author} from {message.guild}",
                    avatar_url=message.author.avatar_url_as(format="png"))
        try:
            await message.remove_reaction(loading_emoji, message.guild.me)
            await message.add_reaction("✅")
        except:pass
client.run(Token)
