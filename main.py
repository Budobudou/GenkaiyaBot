print("起動してるんや...")
import sys
import os
import random
import discord
import pickle
import pandas as pd
from datetime import datetime
from discord.ext import tasks
client = discord.Client()
# Token file read.
setting = open('token.txt', 'r').readlines()
Token = setting[0]
Version = "1.1"
Genkaiya_emoji = "<:genkaiya:1003377706521600042>"
startnotify_channel = "1000607546274488452"
global gencount
# 限界カウンター Start
try:
    with open('gencount.pickle', 'rb') as f:
      global gencount
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
    if now == '23:59':
        ch_name = "限界や出現数"
        for channel in client.get_all_channels():
            if channel.name == ch_name:
                try:
                    global gencount
                    await channel.send(f"今日の全世界での限界やちゃん出現数は{gencount}回や...！\n明日はどうなるかや...おやすみや...")
                    with open("gencount.pickle","wb") as f:
                        gencount = 0
                        pickle.dump(gencount, f)
                except discord.errors.Forbidden:
                    pass
loop.start()
@client.event
async def on_ready():
    print("起動しました")
    await client.change_presence(activity=discord.Game(name="限界リアクション"))
    notify = await client.fetch_channel(startnotify_channel)
    await notify.send("起動したや...")
@client.event
async def on_message(message):
    if message.author.bot:
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
    if '限界' in message.content:
        await message.add_reaction(Genkaiya_emoji)

        with open("gencount.pickle","wb") as f:
            global gencount
            gencount += 1
            pickle.dump(gencount, f)
            print(gencount)
    elif message.content == 'gen!ping':
        raw_ping = client.latency
        ping = round(raw_ping * 1000)
        await message.reply("BotのPing値は" + str(ping) + "msや...")
    elif message.content == 'gen!license':
        await message.reply("限界やちゃんは `Brain Hackers` により、Creative Commons BY-SA 4.0 でライセンスされています。\nhttps://github.com/brain-hackers/README/blob/main/assets.md")
    elif message.content == 'gen!exit':
        if message.author.guild_permissions.administrator:
            await message.reply("さよならや...")
            sys.exit()
        else:
            await message.reply("権限がないんや...")
    elif message.content == 'gen!random':
        df = pd.read_csv('genkaiya.csv')
        images = df['url']
        image_url = random.choice(images)
        await message.reply(image_url)
    # ヘルプ コマンド
    elif message.content == 'gen!help':
        embed = discord.Embed(title=f"限界やBot{Genkaiya_emoji}のコマンド一覧や...")
        embed.add_field(name="gen!help", value="今実行したコマンドや...", inline=True)
        embed.add_field(name="gen!ping",value="Pingを測るコマンドや...",inline=True)
        embed.add_field(name="gen!license",value="ライセンス情報を表示するや...",inline=True)
        embed.add_field(name="gen!add [メンション]",value="指定されたユーザーの全てのメッセージを限界にするコマンドや...",inline=True)
        embed.add_field(name="gen!random",value="限界やちゃんの画像をランダムに表示するコマンドや...",inline=True)
        embed.set_footer(text=f"バージョン情報:{Version}")
        embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
        await message.channel.send(embed=embed)
    elif message.content[:7] == "gen!add":
        # User add transaction.
        user_data_text_write = open('user.txt', 'a')
        server_id = message.guild.id
        message_user_id = message.content.split(" ")
        if len(message_user_id) == 2:
            user_id = message_user_id[1][2:-1]
            user_id_mention = message_user_id[1]
        else:
            user_id = message.author.id
            user_id_mention = "<@"+str(message.author.id)+">"
        user_data_text_write.write(str(server_id)+","+str(user_id)+"\n")
        user_data_text_write.close()
        await message.reply(user_id_mention+"を追加したんや...")
    elif message.content == 'gen!reboot':
        if message.author.guild_permissions.administrator:
            await message.reply('再起動してるんや...')
            python = sys.executable
            os.execl(python,python, * sys.argv)
        else:
            await message.reply("権限がないんや...")
client.run(Token)
