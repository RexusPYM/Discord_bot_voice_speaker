import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import nacl

from voice_acting import Requests

bot = commands.Bot(command_prefix="!", intents=discord.Intents().all())
request = Requests()


@bot.event
async def on_ready():
    print(f"Bot has logged in as {bot.user.name}")

#
# @bot.command()
# async def test(ctx, content, *, kek):
#     if ctx.author.voice:
#         voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#         if not voice_channel:
#             channel = ctx.author.voice.channel
#             voice_client = await channel.connect()
#         else:
#             await ctx.channel.send("Я тут уже")
#         await ctx.channel.send(f"{content} lalalaalala {kek}")
#     else:
#         await ctx.reply("Зайди в голосовой канал")


@bot.command()
async def list_voices(ctx):

    data = request.get_voices()

    if data["status"] == "success":
        char_voices = []

        # формирование паттерна сообщений
        for char_voice in data["content"]["voices"]:
            if char_voice["id_lang"] == 1:
                char_voices.append(
                    str({
                        "Id голоса": char_voice["voice_id"],
                        "Имя": char_voice["name"]["RU"],
                        "Описание": char_voice["description"]["RU"],
                    })
                )

        # формирование сообщений
        msg = []

        # for char_voice in char_voices:
        #     if len(str("\n".join(msg))) + len(str(char_voice)) < 2000:
        #         msg.append(char_voice)
        #         if char_voice == char_voices[len(char_voices) - 1]:
        #             await ctx.send(str("\n".join(msg)).replace("`", "'"))
        #     else:
        #         await ctx.send(str("\n".join(msg)).replace("`", "'"))
        #         msg.clear()
        #         msg.append(char_voice)
        #         if char_voice == char_voices[len(char_voices) - 1]:
        #             await ctx.send(str("\n".join(msg)).replace("`", "'"))

        for i in range(len(char_voices)):
            if len(str("\n".join(msg))) + len(str(char_voices[i])) < 2000:
                msg.append(char_voices[i])
                if i == len(char_voices) - 1:
                    await ctx.send(str("\n".join(msg)).replace("`", "'"))
            else:
                await ctx.send(str("\n".join(msg)).replace("`", "'"))
                msg.clear()
                msg.append(char_voices[i])
                if i == len(char_voices) - 1:
                    await ctx.send(str("\n".join(msg)).replace("`", "'"))

    elif data["status"] == "fail":
        await ctx.send(data["content"])


@bot.command()
async def voice(ctx, voice_id, *, content):

    print(f"Пользователь {ctx.author} сделал запрос с id голоса {voice_id} и сообщением {content}")

    if ctx.author.voice:
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()

        data = request.get_speech(data={
            "voice_id": int(voice_id),
            "text": content,
            "format": "mp3",
        })

        print(data)

        if data["status"] == "success":
            try:
                voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",
                                                         source=data["content"]["audio_url"]
                                                         ))
                await ctx.reply("Ща озвучу")
            except Exception as ex:
                await ctx.reply(f"Упс, чет не так")
        elif data["status"] == "fail":
            await ctx.send(data["content"])
    else:
        await ctx.reply("Зайди в голосовой канал")

#
# async def join(ctx):
#     if ctx.author.voice:
#         channel = ctx.author.voice.channel
#         return await channel.connect()
#     else:
#         await ctx.reply("Зайди в голосовой канал, братанчик")


load_dotenv("keys.env")
bot.run(os.getenv("TOKEN"))
