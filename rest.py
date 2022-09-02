print("起動してるんや...")
import sys
import os
import random
import discord
import asyncio
import re
import pickle
import subprocess
import psutil
import requests
import pandas as pd
from datetime import datetime
from discord.ext import tasks
client = discord.Client(intents=discord.Intents.all())
# Token file read.
setting = open('token.txt', 'r').readlines()
Token = setting[0]
# 環境設定
Version = "1.3rb"
support_server_link = "https://discord.com/invite/NjBheceZRB"
invite_link = f"https://discord.com/api/oauth2/authorize?client_id=1008709839683334186&permissions=52304&scope=applications.commands%20bot"
Genkaiya_emoji = "<:genkaiya:1003377706521600042>"
loading_emoji = "<a:loading:1011568375748636772>"
GLOBAL_CH_NAME = "限界やちゃっと"
GLOBAL_WEBHOOK_NAME = "genkaichat-Webhook"
Updatedate = "2022年8月29日"
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
print(' --===Powered Re:StrawberryBot System===-- ')
print('準備中...')
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
    print("起動しました")
    serversuu = len(client.guilds)
    await client.change_presence(activity=discord.Game(name=random.choice(("限界リアクション",f"現在、{serversuu}サーバーにいるや...","コマンド一覧の表示はgen!helpを入力してや...","gen!randomと打ってみてや...","「限界や」と言ってみてや..."))
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
    reply2 = f'{message.author.mention} 限界や... \n ||コマンド一覧はgen!helpで表示されるや...||' # 返信メッセージの作成
    await message.reply(reply2) # 返信メッセージを送信
#サーバーに招待されたとき

@client.event
async def on_guild_join(guild):
    channel = guild.system_channel
    await channel.send("**初めまして！限界やBotや...** \n コマンド一覧は gen!help と発言してくれや...\n困った場合はgen!resohelpでサポートサーバーに入ってくれや...")
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
   try:
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
       if message.content.startswith("gen!google "):
           memog = message.content[11:].replace('@','＠')
           await message.reply(f'**Google検索結果**\nhttps://www.google.com/search?q={memog}')
           
       #ping
       elif message.content == 'gen!ping':
           raw_ping = client.latency
           ping = round(raw_ping * 1000)
           await message.reply(f"ping値は... \n {str(ping)}msや...！")
           
       #exit
       elif message.content == 'gen!exit':
           if message.author.id == 650349871152496661:
               await message.reply('終了します.....')
               sys.exit()
           else:
               await message.reply('eval権限がありませんw')
       #eval
       elif message.content.startswith("gen!eval "):
           if message.author.id == 650349871152496661:
               eva = message.content[9:]
               await eval(eva)
           else:
               await message.reply('eval権限がありませんw')
       # gen!invite と発言したらメッセージを返す
       elif message.content == 'gen!invite':
       
           await message.reply('こちらがこのBotの招待URLや...! https://discord.com/api/oauth2/authorize?client_id=1008709839683334186&permissions=52304&scope=applications.commands%20bot')

       elif message.content == 'gen!toolhelp':
            embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}コマンド一覧 ＞ ユーティリティ", description="便利なユーティリティ達や...", color=0xffffff)
            embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
            embed.add_field(name="gen!timer <秒数>", value="タイマーをセットするや...", inline=True)
            embed.add_field(name="gen!sdlurl <リンク>", value="ダウンロードURL短縮でURLを短縮するや..", inline=True)
            embed.add_field(name="gen!shorturl <リンク>", value="is.gdでURLを短縮するや...", inline=True)
            embed.add_field(name="gen!calc", value="計算コマンドリストを表示するや...", inline=True)
            embed.add_field(name="gen!google <検索ワード>", value="Google検索のURLを表示するや...", inline=True)
            embed.add_field(name="gen!ds <検索ワード>", value="Disboardでサーバーを検索するや...", inline=True)
            embed.add_field(name="gen!getserverinfo", value="コマンドを実行したサーバーの情報を表示するや...", inline=True)
            embed.add_field(name="gen!getuserinfo <メンションまたはID>", value="指定したユーザーの情報を表示するや...", inline=True)
            embed.add_field(name="gen!getin <ID>", value="他のBotのIDからBotの招待リンクを発行するや...", inline=True)
            embed.add_field(name="gen!emoji <カスタム絵文字>", value="カスタム絵文字のURLを取得・表示するや...", inline=True)
            embed.add_field(name="gen!say <発言させる文章>", value="Botに代わって任意のメッセージを言うや...", inline=True)
            await message.reply(embed=embed)
       elif message.content == 'gen!playhelp':
            embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}コマンド一覧 ＞ お楽しみ", description="お楽しみや...", color=0xffffff)
            embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
            embed.add_field(name="gen!janken", value="ジャンケンをするや...", inline=True)
            embed.add_field(name="gen!dice", value="サイコロを振って1から6の数値を出すや...", inline=True)
            embed.add_field(name="gen!cdice <目数>", value="任意の目数のサイコロを振るや...", inline=True)
            embed.add_field(name="gen!cointoss", value="コイントスをするや...", inline=True)
            embed.add_field(name="gen!random", value="限界やちゃんの画像をランダムに表示するや...", inline=True)
            await message.reply(embed=embed)

       elif message.content == 'gen!resohelp':
           mem = psutil.virtual_memory()
           embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}コマンド一覧 ＞ リソース", description=f"導入サーバー数：{len(client.guilds)}\nBot鯖の使用RAM:{mem.percent}%", color=0xffffff)
           embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
           embed.add_field(name="gen!invite", value="このBotの招待リンクを表示するや...", inline=True)
           embed.add_field(name="gen!updateinfo", value="アップデート情報を表示するや...", inline=True)
           embed.add_field(name="gen!license", value="ライセンス情報を表示するや...", inline=True)
           embed.add_field(name="gen!ping", value="pingを測定するや...", inline=True)
           embed.add_field(name="限界やちゃんBotの公式サーバー", value=f"[参加する]({support_server_link})", inline=True)
           embed.set_footer(text=f"更新日：{Updatedate}")
           await message.reply(embed=embed)
       elif message.content == 'gen!license':
           await message.reply("限界やちゃんは `Brain Hackers` により、Creative Commons BY-SA 4.0 でライセンスされています。\nhttps://github.com/brain-hackers/README/blob/main/assets.md")

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
       elif message.content == 'gen!updateinfo':
           embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}リソース ＞ アップデート情報", description="このBotのアップデート情報を表示するや...", color=0xffffff)
           embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
           embed.add_field(name="バージョン", value="1.3rb", inline=False)
           embed.add_field(name="更新内容", value="・helpの修正と安定性向上\nエラーメッセージの追加", inline=False)
           embed.set_footer(text=f"更新日：{Updatedate}")
           await message.reply(embed=embed)
       elif message.content == 'gen!rehelp':
           embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}コマンド一覧 ＞ 限界リアクション機能について ", description="この機能についての説明や...", color=0xffffff)
           embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
           embed.add_field(name="**Q**.これは何や...?", value="**A**.限界リアクション機能とは、「無理」「極限」などといった__「限界」に関係する文をリアクションでかわいく見せる__機能のことです。", inline=True)    
           await message.reply(embed=embed)
       elif message.content == 'gen!help':
           embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}コマンド一覧 ", description="コマンド種類別にヘルプをまとめたや...", color=0xffffff)
           embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
           embed.add_field(name="限界リアクション機能について", value="gen!rehelp", inline=True)
           embed.add_field(name="ユーティリティ", value="gen!toolhelp", inline=True)
           embed.add_field(name="お楽しみ", value="gen!playhelp", inline=True)
           embed.add_field(name="グローバルチャット", value="gen!globalhelp", inline=True)
           embed.add_field(name="リソース", value="gen!resohelp", inline=True)
           embed.add_field(name="ライセンス情報", value="gen!license", inline=True)
           embed.set_footer(text=f"バージョン {Version}")
           await message.reply(embed=embed)
       
       elif message.content.startswith("gen!shorturl "):
           timer = message.content[13:]
           geturl = f"https://is.gd/create.php?format=simple&format=json&url={timer}"
           res = requests.get(geturl)
           json = res.json()
           se = json['shorturl']
           await message.reply(f"is.gdでURLを短縮しました！\n{se}")
       # gen!timer
       elif message.content.startswith("gen!timer "):
           timer = int(message.content[10:])
           await message.reply(f"タイマーを{timer}秒にセットしたや...")
           await asyncio.sleep(timer)
           reply = f'{message.author.mention} {timer}秒経ったや... これ以上待つのは限界や...' # 返信メッセージの作成
           await message.reply(reply)
       #mension
       elif client.user in message.mentions: # 話しかけられたかの判定
           await reply2(message) # 返信する非同期関数を実行
       # gen!gc_help 
       elif message.content == 'gen!globalhelp':       
              await message.reply('・参加するには任意のチャンネルの名前を 限界やちゃっと に設定してください。 \n ・以下の行為は禁止とさせて頂きます。ご了承下さい。 \n 他人を傷つけるような事を発言 \n スパム、荒らし投稿 \n NSFWに繋がる恐れのある画像、発言 \n 宣伝(Bot管理者が許可した物は除く) \n Botに負荷をかける行為 \n セルフBotの使用 \n このような行為が発見された場合規制を行います。ルールを守ってご利用ください。')
              print('gen!gc_helpが実行されました。')


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
       # dice
       elif message.content == "gen!dice":
           dice = random.randint(1, 6)
           await message.reply(f"🎲{dice}や...!")
       # dice
       elif message.content.startswith("gen!cdice "):
           ms = int(message.content[10:])
           dice = random.randint(1, ms)
           await message.reply(f"🎲{dice}や...!")
       # dice
       elif message.content == "gen!roulette":
           roulette = random.randint(1, 100)
           await message.reply(f"{roulette}や...!")
       # cointoss
       elif message.content == "gen!cointoss":
           cointoss = random.randint(0, 1)
           if cointoss == 1:
               await message.reply("📀表や...")
           elif cointoss == 0:
               await message.reply("💿裏や...")
#       elif message.content == "gen!add":
#          if message.author.guild_permissions.administrator:
#              if str(message.guild.id) in data1:
#                  f = open('serverid.txt', 'r')
#                  data3 = f.read()
#                  print(data3)
#                  deleted = re.sub(str(message.guild.id),"", data3, 1)
#                  with open("serverid.txt","w", encoding = "utf_8") as f:
#                      f.write(deleted)
#                      f.close
#                  await message.reply('このサーバーは既に有効になっていた為、無効化しました。')
#                  return
#              f = open('serverid.txt', 'r')
#              data2 = f.read()
#              f.close()
#              print(data2)
#              file = "serverid.txt"
#              with open(file,"w", encoding = "utf_8") as f:
#                  f.write(f"{data2},{message.guild.id}")
#                  f.close
#              await message.reply('挨拶機能を有効にしました。\n 無効化する場合はこのコマンドをもう一度実行してください')
#          else:
#              await message.reply('管理者権限がありませんw')
       elif message.content.startswith("gen!say "):
           msg1 = message.content[8:]
           msg = msg1.replace('@','＠')
           await message.channel.send(msg)
           if "@" in message.content:
               await message.reply('セキュリティ上の理由でアットマークを大文字に変換したや...')
       # sisoku
       elif message.content.startswith("gen!calc+"):
           moto = int(message.content.split()[-2])
           saki = int(message.content.split()[-1])
           kekka = moto + saki
           await message.reply(f"計算結果：\n {kekka}")
              # sisoku
       elif message.content.startswith("gen!calc-"):
           moto = int(message.content.split()[-2])
           saki = int(message.content.split()[-1])
           kekka = moto - saki
           await message.reply(f"計算結果：\n {kekka}")
               # sisoku
       elif message.content.startswith("gen!calc*"):
           moto = int(message.content.split()[-2])
           saki = int(message.content.split()[-1])
           kekka = moto * saki
           await message.reply(f"計算結果：\n {kekka}")
               # sisoku
       elif message.content.startswith("gen!calc/"):
           moto = int(message.content.split()[-2])
           saki = int(message.content.split()[-1])
           kekka = moto / saki
           await message.reply(f"計算結果：\n {kekka}")
                  # sisoku
       elif message.content.startswith("gen!calc."):
           moto = int(message.content.split()[-2])
           saki = int(message.content.split()[-1])
           kekka = moto // saki
           await message.reply(f"計算結果：\n {kekka}")
               # sisoku
       elif message.content.startswith("gen!calc%"):
           moto = int(message.content.split()[-2])
           saki = int(message.content.split()[-1])
           kekka = moto % saki
           await message.reply(f"計算結果：\n {kekka}")
       elif message.content.startswith("gen!embed"):
           titles = message.content.split()[-2]
           nan = message.content.split()[-1]
           embed=discord.Embed(title=titles, description=nan)
           await message.reply(embed=embed)
               #gen!arithmetic
       elif message.content == 'gen!calc':
              await message.reply('🥽四則演算コマンドリスト \n コマンドの使用例(足し算の場合):gen!calc+ 99 1 \n >計算結果：100 \n ======== \n gen!calc+ 足し算 \n gen!calc- 引き算 \n gen!calc* 掛け算  \n gen!calc/ 割り算 \n gen!calc. 小数点以下切り捨ての割り算 \n gen!calc% 割り算あまり')
       # ds
       elif message.content.startswith("gen!ds "):
           ds = message.content[7:]
           ds1 = ds.replace('@','＠')
           await message.reply(f"https://disboard.org/ja/search?keyword={ds1}")
       # gen!getinvitelink
       elif message.content.startswith("gen!getin "):
           if message.mentions:
               return
           di = message.content[10:]
           adi = f"https://discord.com/api/oauth2/authorize?client_id={di}&permissions=0&scope=applications.commands%20bot"
           embed=discord.Embed(title="発行", color=0xffffff)
           embed.add_field(name="招待リンクを作成しました！", value=adi, inline=False)
           await message.reply(embed=embed)
       # userinfo
       elif message.content.startswith("gen!getuserinfo "):
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
       # userinfo
       elif message.content == "gen!getserverinfo":
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
       #surl
       elif message.content.startswith("gen!sdlurl "):
           dl = message.content[11:]
           udrl = f'https://s.kantantools.com/api/v2/action/shorten?url={dl}'
           response = requests.get(udrl)
           dlk = response.text
           await message.reply(f"{dlk}\nファイルのダウンロードリンクを短縮しました！")
       #unzip
       elif message.content.startswith("gen!urlunzip "):
           anziping = message.content[13:]
           anzip = requests.get(anziping).url
           await message.reply(anzip)
       elif message.content.startswith("gen!emoji "):
           emoji = message.content[10:]
           match = re.match('^<:.+:([0-9]+)>', emoji) or re.match('^<a:.+:([0-9]+)>', emoji)
           if not match:
               return await message.reply("これはカスタム絵文字ではないかもしれないんや...")
           emoji = client.get_emoji(int(match.groups()[0]))
           if not emoji:
               return await message.reply("絵文字が取得できなかったんや...")
           await message.reply(str(emoji.url))
       elif message.content == 'gen!random':
           df = pd.read_csv('genkaiya.csv')
           images = df['url']
           image_url = random.choice(images)
           await message.reply(image_url)
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
       #じゃんけん
       elif message.content == "gen!janken":
            await message.reply("最初はグー、じゃんけん ※ぐー、ちょき、ぱー、の中から発言してや...")

            jkbot = random.choice(("ぐー", "ちょき", "ぱー"))
            draw = "引き分けや..."
            wn = "君の勝ちや..."
            lst = random.choice(("僕の勝ちや...！やったやwwwwwwwwwww","僕の勝ちや..."))

            def jankencheck(m):
                return (m.author == message.author) and (m.content in ['ぐー', 'ちょき', 'ぱー'])

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

            await message.reply(judge)
   except ValueError:
            embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}エラー", description="エラーが発生したのでコマンドを停止したや...", color=0xffffff)
            embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
            embed.add_field(name="詳細や...", value=f"引数エラーが発生しました。\nコマンドの使い方はあっていますか？", inline=False)
            await message.reply(embed=embed)
   except discord.errors.Forbidden:
            embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}エラー", description="エラーが発生したのでコマンドを停止したや...", color=0xffffff)
            embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
            embed.add_field(name="詳細や...", value=f"権限エラーが発生しました。\nBotの権限を見直してください。", inline=False)
            await message.reply(embed=embed)
   except:
            embed=discord.Embed(title=f"限界やちゃんBot{Genkaiya_emoji}エラー", description="エラーが発生したのでコマンドを停止したや...", color=0xffffff)
            embed.set_thumbnail(url="https://i.gyazo.com/126fb5f6de8c78c3c139f97d5cd8c0bf.png")
            embed.add_field(name="詳細や...", value=f"不明なエラーが発生しました。\n詳しくは gen!resohelp からサポートサーバーに参加してください。", inline=False)
            await message.reply(embed=embed)
# TOKEN の 指定
client.run(Token)
