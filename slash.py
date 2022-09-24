print("起動してるんや...")
import sys
import os
import random as r
import discord
import asyncio
import re
import pickle
import subprocess
import psutil
import requests
import pandas as pd
import csv
import typing
from datetime import datetime
from discord import app_commands
from bs4 import BeautifulSoup

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)
# Token file read.
setting = open('token.txt', 'r').readlines()
Token = setting[0]
# 環境設定
Version = "1.4rb"
support_server_link = "https://discord.com/invite/NjBheceZRB"
invite_link = f"https://discord.com/api/oauth2/authorize?client_id=1008709839683334186&permissions=52304&scope=applications.commands%20bot"
Genkaiya_emoji = "<:genkaiya:1003377706521600042>"
loading_emoji = "<a:loading:1011568375748636772>"
GLOBAL_CH_NAME = "限界やちゃっと"
GLOBAL_WEBHOOK_NAME = "genkaichat-Webhook"
Updatedate = "2022年9月06日"
startnotify_channel = "1010162569799028869"
genkaiwordlist = ["限界","げんかい","limit","極限","無理","極限","ダメ","駄目","genkai","文鎮","壊れ","ゴミだ","つらい","くそ"]

with open("./admins.txt") as f:
    admins = f.read()
print(' --===Powered by Re:StrawberryBot System===-- ')
print('準備中...')

@client.event
async def on_ready():
    print("起動しました")
    await tree.sync()
    serversuu = len(client.guilds)
    await client.change_presence(activity=discord.Game(name=r.choice(("限界リアクション",f"現在、{serversuu}サーバーにいるや...","コマンド一覧の表示は/helpを入力してや...","/randomと打ってみてや...","「限界や」と言ってみてや..."))
))
    notify = await client.fetch_channel(startnotify_channel)
    await notify.send("起動したや...")
#関数
async def create_channel(message, channel_name):
    category_id = message.channel.category_id
    category = message.guild.get_channel(category_id)
    new_channel = await category.create_text_channel(name=channel_name)
    return new_channel
#リプライ
async def reply2(message):
    reply2 = f'{message.author.mention} 限界や... \n ||コマンド一覧は/helpで表示されるや...||' # 返信メッセージの作成
    await message.reply(reply2) # 返信メッセージを送信
#サーバーに招待されたとき

@client.event
async def on_guild_join(guild):
    channel = guild.system_channel
    await channel.send("**初めまして！限界やBotや...** \n コマンド一覧は /help と発言してくれや...\n困った場合は/resohelpでサポートサーバーに入ってくれや...")
    cchannel = client.get_channel(739108586025648158)
    await cchannel.send(f"```{guild.name}```\nにBotが導入されました!")

@client.event
async def on_guild_remove(guild):
    cchannel = client.get_channel(739108586025648158)
    await cchannel.send(f"```{guild.name}```\nが逃げたぞ!")

# メッセージ受信時に動作する処理
@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        try:
            if '退出通知' in channel.topic:
                await channel.send(f" {member.name}さんがサーバーを退出したや...")
        except:
            pass

@client.event
async def on_message(message):
    if message.author.bot:
        return
    elif 'ｱﾋｬ' in message.content:
        await message.reply('( ﾟ∀ﾟ)ｱﾋｬ...')
    #mension
    elif client.user in message.mentions: # 話しかけられたかの判定
        await reply2(message) # 返信する非同期関数を実行
    if message.author.bot or message.author.discriminator == "0000":
        return
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

@tree.command(name="google")
async def google(interaction: discord.Interaction, text: str):
        await interaction.response.send_message(f'**Google検索結果**\nhttps://www.google.com/search?q={text}')
       
@tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    raw_ping = client.latency
    ping = round(raw_ping * 1000)
    await interaction.response.send_message(f"ping値は... \n {str(ping)}msや...！")
    
@tree.command(name="exit")
async def exit(interaction: discord.Interaction):
    if interaction.user.id == 650349871152496661:
       await interaction.response.send_message('終了します.....')
       sys.exit()
    else:
        await interaction.response.send_message('eval権限がありませんw', ephemeral=True)

@tree.command(name="eval")
async def eval(interaction: discord.Interaction, cmd: str):
        #eval
        if interaction.user.id == 650349871152496661:
           await eval(cmd)
        else:
            await interaction.response.send_message('eval権限がありませんw', ephemeral=True)

@tree.command(name="invite")
async def invite(interaction: discord.Interaction):
    #/invite と発言したらメッセージを返す
    await interaction.response.send_message('こちらがこのBotの招待URLや...! https://discord.com/api/oauth2/authorize?client_id=1008709839683334186&permissions=52304&scope=applications.commands%20bot')

@tree.command(name="toolhelp")
async def toolhelp(interaction: discord.Interaction):
    embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}コマンド一覧 ＞ ユーティリティ", description="便利なユーティリティ達や...", color=0xffffff)
    embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
    embed.add_field(name="/timer <秒数>", value="タイマーをセットするや...", inline=True)
    embed.add_field(name="/sdlurl <リンク>", value="ダウンロードURL短縮でURLを短縮するや..", inline=True)
    embed.add_field(name="/shorturl <リンク>", value="is.gdでURLを短縮するや...", inline=True)
    embed.add_field(name="/calc", value="計算コマンドリストを表示するや...", inline=True)
    embed.add_field(name="/google <検索ワード>", value="Google検索のURLを表示するや...", inline=True)
    embed.add_field(name="/ds <検索ワード>", value="Disboardでサーバーを検索するや...", inline=True)
    embed.add_field(name="/server", value="コマンドを実行したサーバーの情報を表示するや...", inline=True)
    embed.add_field(name="/user <メンションまたはID>", value="指定したユーザーの情報を表示するや...", inline=True)
    embed.add_field(name="/getin <ID>", value="他のBotのIDからBotの招待リンクを発行するや...", inline=True)
    embed.add_field(name="/emoji <カスタム絵文字>", value="カスタム絵文字のURLを取得・表示するや...", inline=True)
    embed.add_field(name="/say <発言させる文章>", value="Botに代わって任意のメッセージを言うや...", inline=True)
    embed.add_field(name="/safeweb <URL>", value="そのURLが安全かどうか調べるや...", inline=True)
    embed.add_field(name="/braincheck <Brainの型番>", value="電子辞書Brainの型番からスペックを表示するや...\n実行例:/braincheck PW-SH2", inline=True)
    await interaction.response.send_message(embed=embed)

@tree.command(name="playhelp")
async def playhelp(interaction: discord.Interaction):
    embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}コマンド一覧 ＞ お楽しみ", description="お楽しみや...", color=0xffffff)
    embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
    embed.add_field(name="/janken", value="ジャンケンをするや...", inline=True)
    embed.add_field(name="/dice", value="サイコロを振って1から6の数値を出すや...", inline=True)
    embed.add_field(name="/cdice <目数>", value="任意の目数のサイコロを振るや...", inline=True)
    embed.add_field(name="/cointoss", value="コイントスをするや...", inline=True)
    embed.add_field(name="/random", value="限界やちゃんの画像をランダムに表示するや...", inline=True)
    await interaction.response.send_message(embed=embed)

@tree.command(name="resohelp")
async def resohelp(interaction: discord.Interaction):
    mem = psutil.virtual_memory()
    embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}コマンド一覧 ＞ リソース", description=f"導入サーバー数：{len(client.guilds)}\nBot鯖の使用RAM:{mem.percent}%", color=0xffffff)
    embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
    embed.add_field(name="/invite", value="このBotの招待リンクを表示するや...", inline=True)
    embed.add_field(name="/updateinfo", value="アップデート情報を表示するや...", inline=True)
    embed.add_field(name="/license", value="ライセンス情報を表示するや...", inline=True)
    embed.add_field(name="/ping", value="pingを測定するや...", inline=True)
    embed.add_field(name="限界やちゃんBotの公式サーバー", value=f"[参加する]({support_server_link})", inline=True)
    embed.set_footer(text=f"更新日：{Updatedate}")
    await interaction.response.send_message(embed=embed)

@tree.command(name="license")
async def license(interaction: discord.Interaction):
    await interaction.response.send_message("限界やちゃんは `Brain Hackers` により、Creative Commons BY-SA 4.0 でライセンスされています。\nhttps://github.com/brain-hackers/README/blob/main/assets.md")

@tree.command(name="update")
async def update(interaction: discord.Interaction):
    if str(interaction.user.id) in admins:
        await interaction.response.send_message('git pull しているんや...')
        cmd = 'git pull'
        kekka = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        kekka2 = kekka.stdout.read()
        kekka3 = kekka2.decode("utf-8")
        await interaction.response.edit_message(f'pullってきたや...\n```\n{kekka3}\n```ちょっと一回寝てくる、おやすみや...')
        python = sys.executable
        os.execl(python,python, * sys.argv)
    else:
        await interaction.response.send_message("権限がないんや...", ephemeral=True)

@tree.command(name="updateinfo")
async def updateinfo(interaction: discord.Interaction):
    embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}リソース ＞ アップデート情報", description="このBotのアップデート情報を表示するや...", color=0xffffff)
    embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
    embed.add_field(name="バージョン", value="1.4rb", inline=False)
    embed.add_field(name="更新内容", value="・一部のコマンドの項目を更新\nプレフィックスを変更", inline=False)
    embed.set_footer(text=f"更新日：{Updatedate}")
    await interaction.response.send_message(embed=embed)

@tree.command(name="rehelp")
async def rehelp(interaction: discord.Interaction):
    embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}コマンド一覧 ＞ 限界リアクション機能について ", description="この機能についての説明や...", color=0xffffff)
    embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
    embed.add_field(name="**Q**.これは何や...?", value="**A**.限界リアクション機能とは、「無理」「極限」などといった__「限界」に関係する文をリアクションでかわいく見せる__機能のことです。", inline=True)    
    await interaction.response.send_message(embed=embed)

@tree.command(name="shorturl")
async def shorturl(interaction: discord.Interaction, url: str):
    geturl = f"https://is.gd/create.php?format=simple&format=json&url={url}"
    res = requests.get(geturl)
    json = res.json()
    se = json['shorturl']
    await interaction.response.send_message(f"is.gdでURLを短縮したや...\n{se}")

@tree.command(name="safeweb")
async def safeweb(interaction: discord.Interaction, url: str):
    link = f"https://safeweb.norton.com/report/show?url={url}&ulang=jpn"
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    title_text = soup.find('b').get_text(strip=True)
    embed=discord.Embed(title=f"診断してきたや...", color=0xffffff)
    if title_text == "危険":
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Budobudou/GenkaiyaBot/main/assets/kiken.png")
    elif title_text == "安全":
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Budobudou/GenkaiyaBot/main/assets/genkaiya_jelly_droid_face.png")
    elif title_text == "未評価":
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Budobudou/GenkaiyaBot/main/assets/hatena.png")
    elif title_text == "注意":
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Budobudou/GenkaiyaBot/main/assets/chuui.png")
    embed.add_field(name=f"診断結果", value=f"このサイトは**{title_text}**と判定されたや...\n[詳細]({link})", inline=True)
    embed.set_footer(text=f"Powered by Norton Safeweb")
    await interaction.response.send_message(embed=embed)

@tree.command(name="timer")
async def timer(interaction: discord.Interaction, timer: int):
    #/timer
    await interaction.response.send_message(f"タイマーを{timer}秒にセットしたや...")
    await asyncio.sleep(timer)
    reply = f'{interaction.user.mention} {timer}秒経ったや... これ以上待つのは限界や...' # 返信メッセージの作成
    await interaction.channel.send(reply)

@tree.command(name="globalhelp")
async def globalhelp(interaction: discord.Interaction):
    # /gc_help       
    await interaction.response.send_message('・参加するには任意のチャンネルの名前を 限界やちゃっと に設定してください。 \n ・以下の行為は禁止とさせて頂きます。ご了承下さい。 \n 他人を傷つけるような事を発言 \n スパム、荒らし投稿 \n NSFWに繋がる恐れのある画像、発言 \n 宣伝(Bot管理者が許可した物は除く) \n Botに負荷をかける行為 \n セルフBotの使用 \n このような行為が発見された場合規制を行います。ルールを守ってご利用ください。')
    print('/gc_helpが実行されました。')

@tree.command(name="dice")
async def dice(interaction: discord.Interaction):
    #dice
    dice = r.randint(1, 6)
    await interaction.response.send_message(f"🎲{dice}や...!")

@tree.command(name="cdice")
async def cdice(interaction: discord.Interaction, max: int):
    # dice
    dice = r.randint(1, max)
    await interaction.response.send_message(f"🎲{dice}や...!")

@tree.command(name="roulette")
async def roulette(interaction: discord.Interaction):
    #dice
    roulette = r.randint(1, 100)
    await interaction.response.send_message(f"{roulette}や...!")

@tree.command(name="cointoss")
async def cointoss(interaction: discord.Interaction):
    #cointoss
    cointoss = r.randint(0, 1)
    if cointoss == 1:
        await interaction.response.send_message("📀表や...")
    elif cointoss == 0:
        await interaction.response.send_message("💿裏や...")

@tree.command(name="say")
async def say(interaction: discord.Interaction, text: str):
    msg = text.replace('@','＠')
    await interaction.response.send_message(msg)
    if "@" in text:
        await interaction.channel.send('セキュリティ上の理由でアットマークを大文字に変換したや...')

@tree.command(name="calc")
async def calc(interaction: discord.Interaction, mode: typing.Optional[str], moto: typing.Optional[int], saki: typing.Optional[int]):
    if not mode:
        await interaction.response.send_message('🥽四則演算コマンドリスト \n コマンドの使用例(足し算の場合):/calc + 99 1 \n >計算結果：100 \n ======== \n /calc + 足し算 \n /calc- 引き算 \n /calc * 掛け算  \n /calc / 割り算 \n /calc . 小数点以下切り捨ての割り算 \n /calc % 割り算あまり')
    else:
        if mode == "+":
            #sisoku
            kekka = moto + saki
            await interaction.response.send_message(f"計算結果：\n {kekka}")
        elif mode == "-":
            #sisoku
            kekka = moto - saki
            await interaction.response.send_message(f"計算結果：\n {kekka}")
        elif mode == "*":
            #sisoku
            kekka = moto * saki
            await interaction.response.send_message(f"計算結果：\n {kekka}")
        elif mode == "/":
            #sisoku
            kekka = moto / saki
            await interaction.response.send_message(f"計算結果：\n {kekka}")
        elif mode == ".":
            #sisoku
            kekka = moto // saki
            await interaction.response.send_message(f"計算結果：\n {kekka}")
        elif mode == "%":
            # sisoku
            kekka = moto % saki
            await interaction.response.send_message(f"計算結果：\n {kekka}")

@tree.command(name="embed")
async def embed(interaction: discord.Interaction, title: str, description: str):
    embed=discord.Embed(title=title, description=description)
    await interaction.response.send_message(embed=embed)

@tree.command(name="ds")
async def ds(interaction: discord.Interaction, text: str):
    #ds
    ds1 = text.replace('@','＠')
    await interaction.response.send_message(f"https://disboard.org/ja/search?keyword={text}")

@tree.command(name="getin")
async def getin(interaction: discord.Interaction, id: str):
    #/getinvitelink
    if interaction.message.mentions:
        return
    adi = f"https://discord.com/api/oauth2/authorize?client_id={id}&permissions=0&scope=applications.commands%20bot"
    embed=discord.Embed(title="発行", color=0xffffff)
    embed.add_field(name="招待リンクを作成しました！", value=adi, inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="user")
async def user(interaction: discord.Interaction, user: discord.Member):
    #userinfo
    embed = discord.Embed(title=f"{user.name}の情報", color=0xffffff)
    embed.set_thumbnail(url=user.avatar)
    embed.set_footer(
        text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar)
    embed.add_field(name="・ユーザー名", value=f"{user.name}", inline=False)
    embed.add_field(
        name="・ユーザータグ", value=f"#{user.discriminator}", inline=False)
    embed.add_field(name="・ユーザーID", value=f"{user.id}", inline=False)
    embed.add_field(name="・BOTか", value=f"{user.bot}", inline=False)
    embed.add_field(name="・アカウントの作成日(UTC)",
        value=f"{user.created_at}", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="server")
async def server(interaction: discord.Interaction):
    #userinfo
    guild = interaction.guild
    embed = discord.Embed(title=f"{guild}の情報", color=0xffffff)
    embed.set_thumbnail(url=guild.icon)
    embed.set_footer(
        text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar)
    embed.add_field(name="・サーバー名", value=f"{guild.name}", inline=False)
    embed.add_field(
        name="・サーバーオーナー", value=f"{guild.owner}", inline=False)
    embed.add_field(name="・サーバーID", value=f"{guild.id}", inline=False)
    embed.add_field(name="・カスタム絵文字の数", value=f"{len(guild.emojis)}/{guild.emoji_limit}", inline=False)
    embed.add_field(name="・メンバーの数", value=f"{guild.member_count}人", inline=False)
    embed.add_field(name="・システムチャンネル", value=f"{guild.system_channel}", inline=False)
    embed.add_field(name="・サーバーの作成日(UTC)",
        value=f"{guild.created_at}", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="sdlurl")
async def sdlurl(interaction: discord.Interaction, url: str):
       #surl
        udrl = f'https://s.kantantools.com/api/v2/action/shorten?url={url}'
        response = requests.get(udrl)
        dlk = response.text
        await interaction.response.send_message(f"{dlk}\nファイルのダウンロードリンクを短縮しました！")

@tree.command(name="urlunzip")
async def urlunzip(interaction: discord.Interaction, url: str):
    #unzip
    anzip = requests.get(url).url
    await interaction.response.send_message(anzip)

@tree.command(name="emoji")
async def emoji(interaction: discord.Interaction, emoji: str):
    match = re.match('^<:.+:([0-9]+)>', emoji) or re.match('^<a:.+:([0-9]+)>', emoji)
    if not match:
        return await interaction.response.send_message("これはカスタム絵文字ではないかもしれないんや...")
    emoji = client.get_emoji(int(match.groups()[0]))
    if not emoji:
        return await interaction.response.send_message("絵文字が取得できなかったんや...")
    await interaction.response.send_message(str(emoji.url))

@tree.command(name="random")
async def random(interaction: discord.Interaction):
    df = pd.read_csv('genkaiya.csv')
    images = df['url']
    image_url = r.choice(images)
    await interaction.response.send_message(image_url)

@tree.command(name="shell")
async def shell(interaction: discord.Interaction, cmd: str):
    if str(interaction.user.id) in admins:
        if 'token.txt' in cmd:
            await interaction.response.send_message('このファイルはここでは操作できないや...')
        else:
            kekka = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            kekka2 = kekka.stdout.read()
            kekka3 = kekka2.decode("utf-8")
            await interaction.response.send_message(f'```\n{kekka3}\n```')
    else:
        await interaction.response.send_message('権限がないんや...', ephemeral=True)

@tree.command(name="braincheck")
async def braincheck(interaction: discord.Interaction, kishu: str):
    file = './brains.csv'
    atta = 0
    search = kishu.upper()
    f = open(file,'r',encoding="utf-8")
    rows = csv.reader(f)
    for row in rows: # for文で行を1つずつ取り出す(5)
        py = row[0]
        if py == search:
            hatubaiziki = row[1]
            sedai = (f"{row[2]}世代")
            model = row[3]
            cpu = row[4]
            display = (f"サイズ:{row[6]}  解像度:{row[7]}")
            battery = (f"形式:{row[8]}  駆動時間:{row[9]}")
            os = row[12]
            mem = (f"ストレージ:{row[5]}\nRAM:{row[13]}")
            komoji = py.lower()
            sharplink = f"https://jp.sharp/support/dictionary/product/{komoji}.html"
            bimage1 = komoji.replace('-','')
            bimage2 = f"https://jp.sharp/support/dictionary/images/img_{bimage1}.jpg"
            embed = discord.Embed(title=f"{search}の情報", color=0xffffff,description="その型番のBrainが見つかったんや...")
            embed.set_thumbnail(url=bimage2)
            embed.add_field(name="・発売時期", value=f"{hatubaiziki}", inline=False)
            embed.add_field(name="・世代", value=f"{sedai}", inline=False)
            embed.add_field(name="・モデル", value=f"{model}", inline=False)
            embed.add_field(name="・CPU", value=f"{cpu}", inline=False)
            embed.add_field(name="・メモリ", value=f"{mem}", inline=False)
            embed.add_field(name="・ディスプレイ", value=f"{display}", inline=False)
            embed.add_field(name="・バッテリー", value=f"{battery}", inline=False)
            embed.add_field(name="・OS",value=f"{os}", inline=False)
            embed.add_field(name="・公式紹介ページ",value=f"{sharplink}", inline=False)
            embed.set_footer(text=f"データ:Brainスペック一覧 by Brain Hackers")
            await interaction.response.send_message(embed=embed)
            atta = 1
            break
    f.close() 
    if atta == 0:
            embed = discord.Embed(title=f"その型番は見つからなかったや...", color=0xffffff)
            await interaction.response.send_message(embed=embed)

@tree.command(name="janken")
async def janken(interaction: discord.Interaction):
    #じゃんけん
    await interaction.response.send_message("最初はグー、じゃんけん ※ぐー、ちょき、ぱー、の中から発言してや...")

    jkbot = r.choice(("ぐー", "ちょき", "ぱー"))
    draw = "引き分けや..."
    wn = "君の勝ちや..."
    lst = r.choice(("僕の勝ちや...！やったやwwwwwwwwwww","僕の勝ちや..."))

    def jankencheck(m):
        return (m.author == interaction.user) and (m.content in ['ぐー', 'ちょき', 'ぱー'])

    reply = await client.wait_for("message", check=jankencheck)
    if reply.content == jkbot:
        judge = draw
    else:
        if reply.content == "ぐー":
            if jkbot == "ちょき":
                judge = wn
            else:
                judge = lst

        elif reply.content == "ちょき":
            if jkbot == "ぱー":
                judge = wn
            else:
                judge = lst

        else:
            if jkbot == "ぐー":
                judge = wn
            else:
                judge = lst

    await interaction.channel.send(judge)

@tree.command(name="help")
async def help(interaction: discord.Interaction):
    embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}コマンド一覧 ", description="コマンド種類別にヘルプをまとめたや...", color=0xffffff)
    embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
    embed.add_field(name="限界リアクション機能について", value="/rehelp", inline=True)
    embed.add_field(name="ユーティリティ", value="/toolhelp", inline=True)
    embed.add_field(name="お楽しみ", value="/playhelp", inline=True)
    embed.add_field(name="グローバルチャット", value="/globalhelp", inline=True)
    embed.add_field(name="リソース", value="/resohelp", inline=True)
    embed.add_field(name="ライセンス情報", value="/license", inline=True)
    embed.set_footer(text=f"バージョン {Version}")
    await interaction.response.send_message(embed=embed)

#@tree.command(name="add")
#async def add(interaction: discord.Interaction):
#   if interaction.user.guild_permissions.administrator:
#       if str(interaction.guild.id) in data1:
#           f = open('serverid.txt', 'r')
#           data3 = f.read()
#           print(data3)
#           deleted = re.sub(str(interaction.guild.id),"", data3, 1)
#           with open("serverid.txt","w", encoding = "utf_8") as f:
#               f.write(deleted)
#               f.close()
#           await interaction.response.send_message('このサーバーは既に有効になっていた為、無効化しました。')
#           return
#       f = open('serverid.txt', 'r')
#       data2 = f.read()
#       f.close()
#       print(data2)
#       file = "serverid.txt"
#       with open(file,"w", encoding = "utf_8") as f:
#           f.write(f"{data2},{interaction.guild.id}")
#           f.close
#           await interaction.response.send_message('挨拶機能を有効にしました。\n 無効化する場合はこのコマンドをもう一度実行してください')
#   else:
#       await interaction.response.send_message('権限がないんや...', ephemeral=True)

# TOKEN の 指定
client.run(Token)
