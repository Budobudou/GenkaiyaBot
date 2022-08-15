import discord,sys

client = discord.Client()
# Token file read.
Token = open('token.txt', 'r').read()
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
        helpcmd = f"限界やBot コマンドリスト\n`gen!help` 今実行したコマンドや...\n`gen!ping` Pingを測るコマンドや...\n`gen!license` ライセンス情報を表示するや...\n`gen!add [メンション]` 指定されたユーザーの全てのメッセージを限界にするコマンドや... \n\nバージョン情報:{Version}"
        await message.channel.send(helpcmd)
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
        await message.reply(user_id_mention+"を追加しました。")
client.run(Token)