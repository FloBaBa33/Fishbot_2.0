import discord
from discord.ext import commands
from random import randrange
from Secret import Secret


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def join(self, member):
        server = member.guild.id
        if server == Secret.Server_id:
            channel_id = Secret.Eingansportal
            channel = self.bot.get_channel(channel_id)
            nachricht = discord.Embed(
                color=discord.Colour.purple()
            )
            nachricht.add_field(name="Herzlich Willkommen im Katzenkorb", value="Bitte ließ dir zuerst die Regeln "
                                                                                "durch und wähle dann in dem Channel "
                                                                                "'Rollenvergabe' die für dich "
                                                                                "relevanten Rollen aus.\n\n\nBei "
                                                                                "Fragen wende dich bitte an das "
                                                                                "Serverteam")
            embed = discord.Embed(
                color=discord.Colour.dark_green()
            )
            embed.set_author(name="Neues Kätzchen")
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Name", value=member.name, inline=False)
            await member.create_dm()
            await member.dm_channel.send(embed=nachricht)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        number = randrange(0,100)
        await self.bot.process_commands(message)
        if message.author.bot is False:
            if "http" in message.content:
                if not message.content.startswith("https://tenor.com"):
                    if message.channel.id == Secret.Main_channel:
                        await message.delete()
            else:
                pass
            if number == 3:
                try:
                    await message.add_reaction("🐱")
                except: pass


def setup(bot):
    bot.add_cog(Event(bot))
    print("--> Event")
