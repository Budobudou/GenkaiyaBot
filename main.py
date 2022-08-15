import discord

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
    if '限界' in message.content:
        await message.add_reaction("<genkaiya:1003377706521600042>")
    elif message.content == '!ping':
        raw_ping = client.latency
        ping = round(raw_ping * 1000)
        await message.reply("Pong!\nBotのPing値は" + str(ping) + "msです。")

client.run("Token")
