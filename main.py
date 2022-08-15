import discord,sys

client = discord.Client()
Token = "your token"
Version = "1.0 (Developer Preview)"
Genkaiya_emoji = "<:genkaiya:1008703726405562474>"
@client.event
async def on_ready():
    print("起動しました")
    await client.change_presence(activity=discord.Game(name="限界やちゃん"))

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if '限界' in message.content:
        await message.add_reaction("<:genkaiya:1008703726405562474>")
    elif message.content == 'gen!ping':
        raw_ping = client.latency
        ping = round(raw_ping * 1000)
        await message.reply("Pong!\nBotのPing値は" + str(ping) + "msです。")
    elif message.content == 'gen!license':
        await message.reply("限界やちゃんは Brain-Hackers により、Creative Commons BY-SA 4.0 でライセンスされています。\nhttps://github.com/brain-hackers/README/blob/main/assets.md")
    elif message.content == 'gen!exit':
        await message.channel.send("さよならー")
        sys.exit()
    elif message.content == 'gen!help':
        helpcmd = f"限界やBot コマンドリスト\ngen!help 今実行したコマンドや...\ngen!ping Pingを測るコマンドや...\ngen!license ライセンス情報を表示するや...\n\nバージョン情報:{Version}"
        await message.channel.send(helpcmd)
client.run(Token)