import discord
import MeCab
client = discord.Client()
Token = "Your Token"

@client.event
async def on_ready():
    print("Login successful!")
    await client.change_presence(activity=discord.Game(name="限界やちゃん"))

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if isGenkaiya(message.content):
        await message.add_reaction("<genkaiya:1003377706521600042>")
    elif message.content == '!ping':
        raw_ping = client.latency
        ping = round(raw_ping * 1000)
        await message.reply("Pong!\nBotのPing値は" + str(ping) + "msです。")

def isGenkaiya(text):
    return ("限界" in MeCab.Tagger("-Owakati").parse(text).split())

client.run("Token")
