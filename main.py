print("起動してるんや...")
import sys
import os
import random
import discord
import asyncio
import pickle
import subprocess
import pandas as pd
from datetime import datetime
from discord.ext import tasks
client = discord.Client()
# Token file read.
setting = open('token.txt', 'r').readlines()
Token = setting[0]
Version = "1.2(Developer Preview)"
support_server_link = "https://discord.com/invite/NjBheceZRB"
Genkaiya_emoji = "<:genkaiya:1003377706521600042>"
startnotify_channel = "1010162569799028869"
with open("./admins.txt") as f:
    admins = f.read()
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

    if now == '22:00':
        ch_name = "限界や出現数"
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
    print("起動しました")
    serversuu = len(client.guilds)
    await client.change_presence(activity=discord.Game(name=random.choice(("限界リアクション",f"現在、{serversuu}サーバーにいるや...","コマンド一覧の表示はgen!helpを入力してや...","gen!randomと打ってみてや...","「限界や」と言ってみてや..."))
))
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
    if '限界' in message.content or 'げんかい' in message.content or 'genkai' in message.content or 'limit' in message.content:
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
        if str(message.author.id) in admins:
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
            embed.add_field(name="gen!ping",value="Pingを測るや...",inline=True)
            embed.add_field(name="gen!license",value="ライセンス情報を表示するんや...",inline=True)
            embed.add_field(name="gen!add [メンション]",value="指定されたユーザーの全てのメッセージを限界にするや...",inline=True)
            embed.add_field(name="gen!remove",value="自分のメッセージを限界にするのをやめるんや...",inline=True)
            embed.add_field(name="gen!random",value="限界やちゃんの画像をランダムに表示するや...",inline=True)
            embed.add_field(name="gen!timer",value="秒数の分だけ時間を測るや...",inline=True)
            embed.add_field(name="gen!channel",value="特殊なチャンネルリストを表示するや...",inline=True)
            if str(message.author.id) in admins:
                embed.add_field(name="gen!exit",value="Botを終了するや...",inline=True)
                embed.add_field(name="gen!reboot",value="Botを再起動するや...",inline=True)
                embed.add_field(name="gen!update",value="Botを GitHub から更新するや...",inline=True)
                embed.add_field(name="gen!eval [コード]",value="Python コードを実行するんや...",inline=True)
                embed.add_field(name="gen!shell [コマンド]",value="Linux コマンドを実行するんや...",inline=True)
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
    elif message.content == "gen!remove":
        with open("./user.txt") as f:
            rem = f.read()
            f.close
        removeid = f"{message.guild.id},{message.author.id}"
        deleted = re.sub(str(removeid),"", rem, 1)
        with open("./user.txt","w") as f:
            f.write(deleted)
            f.close
    elif message.content.startswith("gen!eval "):
       if str(message.author.id) in admins:
           eva = message.content[8:]
           await eval(eva)
       else:
           await message.channel.send('権限がないんや...') 
    elif message.content.startswith("gen!shell "):
       if str(message.author.id) in admins:
           cmd = message.content[9:]
           kekka = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
           kekka2 = kekka.stdout.read()
           kekka3 = kekka2.decode("utf-8")
           await message.reply(f'```\n{kekka3}\n```')
       else:
           await message.channel.send('権限がないんや...') 
    elif message.content == 'gen!reboot':
        if str(message.author.id) in admins:
            await message.reply('再起動してるんや...')
            python = sys.executable
            os.execl(python,python, * sys.argv)
        else:
            await message.reply("権限がないんや...")
    elif message.content == 'gen!update':
        if str(message.author.id) in admins:
          await message.reply('git pull しているんや...')
          cmd = 'git pull'
          kekka = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
          kekka2 = kekka.stdout.read()
          kekka3 = kekka2.decode("utf-8")
          await message.reply(f'pullってきたや...\n```\n{kekka3}\n```ちょっと一回寝てくる、おやすみや...')
          python = sys.executable
          os.execl(python,python, * sys.argv)
        else:
            await message.reply("権限がないんや...")
    elif message.channel.topic == "チャンネル作成":
          new_channel = await message.guild.create_text_channel(message, channel_name=message.content)
          text = f"{new_channel.mention} を作成しました"
          await message.channel.send(text)
          channel = client.get_channel(new_channel.id)
          member = channel.guild.get_member(message.author.id)
          await channel.set_permissions(member, manage_channels=True, manage_messages=True)
          await new_channel.edit(position=0)
          await message.channel.edit(position=0)
          channel = client.get_channel(new_channel)
            
    elif message.content.startswith("gen!timer "):
          timer = int(message.content[10:])
          await message.channel.send(f"タイマーを{timer}秒にセットしたや...")
          await asyncio.sleep(timer)
          replymsg = f'{message.author.mention} {timer}秒経ったや... これ以上待つのは限界や...'
          await message.reply(replymsg)
    if message.content == 'gen!channel':
          embed=discord.Embed(title=f"限界やBot{Genkaiya_emoji}特殊チャンネル", description="※これらの機能はコマンドではありません。指示に従ってチャンネルを作成してください。", color=0xffffff)
          embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
          embed.add_field(name="チャンネル作成機能", value="任意のチャンネルのトピックを **チャンネル作成** に設定してください。そこに発言されるとチャンネルが作成されます。\nチャンネル作成用にカテゴリーを作成してください", inline=True)
client.run(Token)
