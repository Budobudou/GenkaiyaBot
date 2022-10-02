#Discord.py v1.7
import discord
import pickle
import asyncio
import pickle
import os
import sys
import jaconv
import re
from discord.ext import tasks
from datetime import datetime
GLOBAL_CH_NAME = "限界やちゃっと"
GLOBAL_WEBHOOK_NAME = "genkaichat-Webhook"
ngwords = {}
with open("nglist.pickle", mode="rb") as f:
    ngwords = pickle.load(f)
client = discord.Client(intents=discord.Intents.all())
setting = open('token.txt', 'r').readlines()
Token = setting[0]
Genkaiya_emoji = "<:genkaiya:1003377706521600042>"
genkaiwordlist = ["限界","げんかい","limit","極限","無理","極限","ダメ","駄目","genkai","文鎮","壊れ","ゴミだ","つらい","くそ"]
loading_emoji = "<a:loading:1011568375748636772>"
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
async def on_ready():
    startnotify_channel = "1010162569799028869"
    print("起動しました")
    notify = await client.fetch_channel(startnotify_channel)
    await notify.send("グローバルチャット&リアクションサービスを開始したや...")
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
        ngtest = 0
        ngcheck1 = message.content.replace('　', '')
        ngcheck2 = ngcheck1.replace(' ', '')
        ngcheck3 = ngcheck2.replace('ー', '')
        ngcheck4 = jaconv.kata2hira(ngcheck3)
        ngcheck5 = ngcheck4.lower()
        for word in ngwords:
            if word in ngcheck5:
                ngtest = 1
                break
            
        if ngtest == 1:
            await message.add_reaction("❌")
            embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}エラー", description="エラーが発生したので処理を停止したや...", color=0xffffff)
            embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
            embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
            embed.add_field(name="詳細や...", value=f"不適切な単語が含まれています。", inline=False)
            await message.reply(embed=embed)
            return
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
