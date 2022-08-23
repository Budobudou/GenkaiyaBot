print("起動してるんや...")
import sys
import os
import random
import discord
import asyncio
import re
import pickle
import subprocess
import requests
import pandas as pd
from datetime import datetime
from discord.ext import tasks
client = discord.Client(intents=discord.Intents.all())
# Token file read.
setting = open('token.txt', 'r').readlines()
Token = setting[0]
# 環境設定
Version = "1.2(Developer Preview)"
support_server_link = "https://discord.com/invite/NjBheceZRB"
Genkaiya_emoji = "<:genkaiya:1003377706521600042>"
loading_emoji = "<a:loading:1011568375748636772>"
GLOBAL_CH_NAME = "限界やちゃっと"
GLOBAL_WEBHOOK_NAME = "genkaichat-Webhook"
startnotify_channel = "1010162569799028869"
genkaiwordlist = ["限界","げんかい","limit","極限","無理","極限","ダメ","駄目","genkai","文鎮","壊れ","ゴミだ","つらい"]
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
    select = random.choice(("限界リアクション",f"現在、{serversuu}サーバーにいるや...","コマンド一覧の表示はgen!helpを入力してや...","gen!randomと打ってみてや...","「限界や」と言ってみてや...")
    await client.change_presence(activity=discord.Game(name=select))
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
    if message.content == 'gen!ping':
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
            embed.add_field(name="gen!timer [秒数]",value="秒数の分だけ時間を測るや...",inline=True)
#            embed.add_field(name="gen!channel",value="特殊なチャンネルリストを表示するや...",inline=True)
            embed.add_field(name="gen!emoji [カスタム絵文字]",value="カスタム絵文字のURLを取得するや...",inline=True)
            embed.add_field(name="gen!serverinfo",value="このサーバーの情報を取得するや...",inline=True)
            embed.add_field(name="gen!userinfo [メンション]",value="カスタム絵文字のURLを取得するや...",inline=True)
            embed.add_field(name="gen!shorturl [短縮するURL]",value="URLを短縮するや...",inline=True)
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
        a = await message.channel.send('削除しているんや...')
        with open("./user.txt") as f:
            rem = f.read()
            f.close
        removeid = f"{message.guild.id},{message.author.id}"
        deleted = re.sub(str(removeid),"", rem, 1)
        with open("./user.txt","w") as f:
            f.write(deleted)
            f.close
        await a.edit('削除したんや...') 
    elif message.content.startswith("gen!eval "):
       if str(message.author.id) in admins:
           eva = message.content[8:]
           await eval(eva)
       else:
           await message.channel.send('権限がないんや...') 
    elif message.content.startswith("gen!shell "):
       if str(message.author.id) in admins:
           if 'token.txt' in message.content:
               await message.reply('このファイルはここでは操作できないや...')
           else:
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
# グローバルチャット
    if message.channel.name == GLOBAL_CH_NAME:
        channels = client.get_all_channels()
        global_channels = [ch for ch in channels if ch.name == GLOBAL_CH_NAME]
        try:
            await message.add_reaction(loading_emoji)
        except:pass
        for channel in global_channels:
            if channel.id == message.channel.id:continue
            ch_webhooks = await channel.webhooks()
            if ch_webhooks == []:
                try:webhook = await channel.create_webhook(name=GLOBAL_WEBHOOK_NAME, reason=f"{GLOBAL_CH_NAME}の為にwebhook作成したや...")
                except:continue
            else:
                webhook = ch_webhooks[0]
            content = message.content.replace("@", "＠")
            if content == "":content = "メッセージ内容がないんや..."
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
            await message.remove_reaction("📡", message.guild.me)
            await message.add_reaction("✅")
        except:pass
#    elif message.channel.topic == "チャンネル作成":
#          new_channel = await message.guild.create_text_channel(name=message.content)
#          text = f"{new_channel.mention} を作成したや..."
#          await message.reply(text)
#          channel = client.get_channel(new_channel.id)
#          await channel.set_permissions(message.author, manage_channels=True, manage_messages=True)
#          await new_channel.edit(position=0)
#          await message.channel.edit(position=0)
#          channel = client.get_channel(new_channel)
            
    elif message.content.startswith("gen!timer "):
          timer = int(message.content[10:])
          await message.channel.send(f"タイマーを{timer}秒にセットしたや...")
          await asyncio.sleep(timer)
          replymsg = f'{message.author.mention} {timer}秒経ったや... これ以上待つのは限界や...'
          await message.reply(replymsg)
#    if message.content == 'gen!channel':
#          embed=discord.Embed(title=f"限界やBot{Genkaiya_emoji}特殊チャンネル", description="※これらの機能はコマンドではありません。指示に従ってチャンネルを作成してください。", color=0xffffff)
#          embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
#          embed.add_field(name="チャンネル作成機能", value="任意のチャンネルのトピックを **チャンネル作成** に設定してください。そこに発言されるとチャンネルが作成されます。\nチャンネル作成用にカテゴリーを作成してください", inline=True)

    elif message.content.startswith("gen!emoji "):
        emoji = message.content[10:]
        match = re.match('^<:.+:([0-9]+)>', emoji) or re.match('^<a:.+:([0-9]+)>', emoji)
        if not match:
            return await message.reply("これはカスタム絵文字ではないかもしれないんや...")
        emoji = client.get_emoji(int(match.groups()[0]))
        if not emoji:
            return await message.reply("絵文字が取得できなかったんや...")
        await message.reply(str(emoji.url))
    elif message.content.startswith("gen!userinfo "):
        suser = re.sub(r"\D", "", message.content)
        user = await client.fetch_user(int(suser))
        embed = discord.Embed(title=f"{user.name}の情報", color=0xffffff)
        embed.set_thumbnail(url=user.avatar_url_as(static_format="png"))
        embed.set_footer(
            text=f"Requested by {message.author}", icon_url=message.author.avatar_url)
        embed.add_field(name="・ユーザー名", value=f"{user.name}", inline=False)
        embed.add_field(
            name="・ユーザータグ", value=f"#{user.discriminator}", inline=False)
        embed.add_field(name="・ユーザーID", value=f"{user.id}", inline=False)
        embed.add_field(name="・BOTか", value=f"{user.bot}", inline=False)
        embed.add_field(name="・アカウントの作成日(UTC)",
            value=f"{user.created_at}", inline=False)
        await message.reply(embed=embed)
    elif message.content == "gen!serverinfo":
        embed = discord.Embed(title=f"{message.guild}の情報", color=0xffffff)
        embed.set_thumbnail(url=message.guild.icon_url)
        embed.set_footer(
            text=f"Requested by {message.author}", icon_url=message.author.avatar_url)
        embed.add_field(name="・サーバー名", value=f"{message.guild.name}", inline=False)
        embed.add_field(
            name="・サーバーオーナー", value=f"{message.guild.owner}", inline=False)
        embed.add_field(name="・サーバーID", value=f"{message.guild.id}", inline=False)
        embed.add_field(name="・カスタム絵文字", value=f"{len(message.guild.emojis)}個", inline=False)
        embed.add_field(name="・サーバーの作成日(UTC)",
            value=f"{message.guild.created_at}", inline=False)
        await message.reply(embed=embed)
    elif message.content.startswith("gen!shorturl "):
        timer = message.content[13:]
        geturl = f"https://is.gd/create.php?format=simple&format=json&url={timer}"
        res = requests.get(geturl)
        json = res.json()
        se = json['shorturl']
        await message.reply(f"is.gdでURLを短縮したや...\n{se}")
client.run(Token)
