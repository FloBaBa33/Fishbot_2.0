import asyncio
import asyncpg
import datetime
import discord
from discord.ext import commands
from Modul.Secret import Secret

intents = discord.Intents.all()
cogs = ["Modul.Admin", "Modul.Commands", "Modul.Events", "Modul.Level"]


bot = commands.Bot(command_prefix=commands.when_mentioned_or("."), case_insensitive=True, help_command=None, intents=intents)
bot.remove_command("help")


async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database="lvlDB", user="postgres", password=Secret.db_password)


async def date_checker():
    print("datechecker startet")
    channel = bot.get_channel(int(Secret.Main_channel))
    date = datetime.datetime.now()
    while True:
        if date.hour == 8 and date.minute == 0 and date.second == 0:
            await channel.send(f"Einen wunderschönen {date.day}.{date.month} euch allen!")
            await asyncio.sleep(86400)
        elif date.second != 0:
            if date.second in [10, 20, 30, 40, 50]:
                await asyncio.sleep(10)
            elif date.second in [5, 15, 25, 35, 45, 55]:
                await asyncio.sleep(5)
            elif date.second not in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]:
                await asyncio.sleep(1)
        elif date.minute != 0:
            if date.minute in [10, 20, 30, 40, 50]:
                print("10 min warten")
                await asyncio.sleep(600)
            elif date.minute in [5, 15, 25, 35, 45, 55]:
                print("5 min warten")
                await asyncio.sleep(300)
            elif date.minute not in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]:
                print("1 min warten")
                await asyncio.sleep(60)
        elif date.hour != 8:
            if date.hour in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]:
                print("1 Stunden warten")
                await asyncio.sleep(3600)
            elif date.hour in [2,6,10, 14, 18, 22]:
                print("2 Stunden warten")
                await asyncio.sleep(7200)
            elif date.hour in [4, 12, 20]:
                print("4 Stunden warten")
                await asyncio.sleep(14400)
            elif date.hour in [0, 16]:
                print("8 Stunden warten")
                await asyncio.sleep(28800)


# todo rollenvergabe, birthdaybot, twitchankündigungen

@bot.event
async def on_ready():
    print(f"***********\nloggt in as:\n{bot.user.name}\n***********")
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except:
            pass
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="nach dem Server"))
    await date_checker()


@bot.command(name="modul")
async def modul(ctx, arg=None, extension=None):
    if arg == "load":
        bot.load_extension(f"Module.{extension}")
        await ctx.author.send(f'das Modul:"{extension}" wurde gestartet')
    elif arg == "unload":
        bot.unload_extension(f"Module.{extension}")
        await ctx.author.send(f'das Modul:"{extension}" wurde beendet')
    elif arg == "reload":
        bot.unload_extension(f"Module.{extension}")
        await asyncio.sleep(5)
        bot.load_extension(f"Module.{extension}")
        await ctx.author.send(f'das Modul:"{extension}" wurde neugestartet')
    elif arg or extension is None:
        embed = discord.Embed(
            color=discord.Colour.dark_purple()
        )
        embed.set_author(name="Module")
        embed.add_field(name="Dies sind die Module", value="Sie können einzeln geladen werden", inline=False)
        embed.add_field(name="Level", value="Mit diesem Modul erhalten User", inline=False)
        embed.add_field(name="Commands", value="In diesem Modul sind ein paar Commands enthalten", inline=False)
        embed.add_field(name="Events", value="In deisem Modul sind Nachrichten basierte Events enthalten", inline=False)
        embed.add_field(name="Admin", value="Ein paar Admincommands", inline=False)
        embed.add_field(name="Voice", value="Ein Modul für temporäre Voicechannel", inline=False)
        await ctx.author.send(embed=embed)

bot.loop.run_until_complete(create_db_pool())
Token = Secret.Token
bot.run(Token)
