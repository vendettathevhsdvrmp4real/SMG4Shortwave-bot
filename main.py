import discord
from discord.ext import commands
import asyncio

TOKEN = ""
STREAM_URL = "http://streams.printf.cc:8000/buzzer.ogg"  # UVB-76 stream

intents = discord.Intents.default()
intents.message_content = True  # Needed if you want to handle messages

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def uvb76(ctx):
    if ctx.author.voice is None:
        await ctx.send("Join a voice channel first.")
        return

    channel = ctx.author.voice.channel
    vc = await channel.connect()

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    vc.play(discord.FFmpegPCMAudio(STREAM_URL, **ffmpeg_options))

    await ctx.send(f"Streaming UVB-76 in {channel.name}...")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

bot.run(TOKEN)
