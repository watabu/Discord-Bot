import discord
from discord.ext import commands
import config
import sys
import asyncio

bot = commands.Bot(command_prefix="!")
bot_role_id = 759253641227010088

@bot.event
async def on_ready():
    await greet()
    print("on_ready")

async def greet():
    CHANNEL_ID = 759032798769578009
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('おはようございます。')

@bot.event
async def on_disconnect():
    print("on_disconnect")
    await sys.exit()

@bot.event
async def on_message(message):
    #if message.author == bot.user or (bot_role_id in message.author.roles):
    if message.author.bot:
        #BOTからのメッセージには反応しない
        #無限ループを防ぐ
        return
    
    if "こんにちは" in message.content:
        await message.channel.send("こんにちは、" + message.author.name + "さん！")
    elif "Bot1" in message.content:
        await message.channel.send("はい、Bot1号です")

    NG_WORDS = ["月曜日", "連休", "単位"]
    for ng_word in NG_WORDS:
        if ng_word in message.content:
            #NGワードを検知したらテキストチャンネルに通知
            await message.channel.send(f"**{ng_word}**はNGワードです。")
            break
    
    #if message.content[0] == "/" :
        #await message.channel.send(get_data(message))
    
    await bot.process_commands(message)



@bot.command()
async def hello(ctx):
    #待機するメッセージのチェック関数
    def check_message_author(msg):
        return msg.author is ctx.author

    #あいさつする既存の処理
    await ctx.send(f" こんにちは、{ctx.author.name} さん。")
    await ctx.send("ご気分はいかがでしょうか？")
    try:
        #チェック関数に合格するようなメッセージを待つ
        msg = await bot.wait_for("message", check=check_message_author, timeout=10)
    except asyncio.TimeoutError:
        await ctx.send("タイムアウトしました。")
        return
    #受け取ったメッセージの内容を使って返信
    #await ctx.send(f"「{msg.content}」という気分なんですね。")
    embed = discord.Embed()
    embed.color = discord.Color.blue()
    embed.description = "あなたの気分を把握しました。"
    embed.add_field(name="あなたの気分 ", value=msg.content)
    await ctx.send(embed=embed)

@bot.command()
async def stop(ctx):
    await ctx.send("停止します。おやすみなさい。")
    await bot.logout()

@bot.command()
async def hello_reaction(ctx):
    #いいね、よくないねの絵文字
    thumbs_up = '\N{THUMBS UP SIGN}'
    thumbs_down = '\N{THUMBS DOWN SIGN}'

    #チェック関数
    def check_reaciton(reaciton, user):
        user_ok = (user == ctx.author)
        reaciton_ok = (reaciton.emoji == thumbs_up or 
            reaciton.emoji == thumbs_down)
        return user_ok and reaciton_ok

    #メッセージを送信
    await ctx.send(f"こんにちは、{ctx.author.name}さん。")
    msg = await ctx.send("いまの気分を選んでください。")
    #送信したメッセージにリアクションを付与
    await msg.add_reaction(thumbs_up)
    await msg.add_reaction(thumbs_down)
    #ユーザーからのリアクションを待つ
    reaction, user = await bot.wait_for("reaction_add",
        check=check_reaciton)
    #ユーザーのリアクションに応じてメッセージを変える
    feel = "良い気分" if reaction.emoji == thumbs_up else "良くない気分"
    await ctx.send(f"{feel}なんですね。")

    




def get_data(message):
    command = message.content
    data_table = {
        '/members': message.guild.members, # メンバーのリスト
        '/roles': message.guild.roles, # 役職のリスト
        '/text_channels': message.guild.text_channels, # テキストチャンネルのリスト
        '/voice_channels': message.guild.voice_channels, # ボイスチャンネルのリスト
        '/category_channels': message.guild.categories, # カテゴリチャンネルのリスト
    }
    return data_table.get(command, '無効なコマンドです')


bot.run(config.TOKEN)