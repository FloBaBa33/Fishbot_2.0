import discord
from discord.ext import commands
from Secret import Secret


def check_channel(channel):
    return channel == Secret.Bot_channel


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h", "hilfe"])
    async def Hilfe(self,ctx):
        embed = discord.Embed(
            color=discord.Colour.dark_purple()
        )
        embed.set_author(name="Hilfe")
        embed.set_image(url="https://cdn.discordapp.com/attachments/663886522969358366/782701248449085450"
                            "/20190312_170913.png")
        embed.add_field(name="Name des Commands", value="Was macht der Command", inline=False)
        embed.add_field(name="level", value="gibt das aktuelle Level eines Users an", inline=False)
        embed.add_field(name="arzt / doc", value="schicke jdm zum Arzt", inline=False)
        embed.add_field(name="ip / server / server-ip", value="mit diesem Command könnt ihr die Ip des "
                                                              "Minecraftservers erfragen\ndieser Command geht nur in "
                                                              "dem Server Chat für den Server", inline=False)
        embed.add_field(name="Tapete / Comic / Comic-1", value="Ein netter Dialog zwischen einer Tapete und einer Wand", inline=False)
        embed.add_field(name="Wand / Comic-2", value="Ein weiterer Dialog zwischen der Tapete und der Wand", inline=False)
        embed.add_field(name="", value="", inline=False)
        if check_channel(ctx.channel.id) is False or ctx.guild is None:
            ctx.author.send(embed=embed)

    @commands.command(name="arzt", aliases=["doc"])
    async def Arzt(self, ctx, member:discord.Member=None):
        if member is None:
            await ctx.send(f"{str(ctx.author.mention)} geh zum Arzt!")
        else:
            await ctx.send(f"{str(member)} geh zum Arzt!")

    @commands.command(name="ip", aliases=["server", "server_ip", "server-ip"])
    async def mc_ip(self, ctx):
        if ctx.channel.id == Secret.Server_channel:
            ctx.author.send(f"Die Ip des Minecraft_Servers ist {Secret.Server_ip}")

    @commands.command(name="tapete", aliases=["comic", "comic1", "comic_1", "comic-1", "t"])
    async def Tapete(self, ctx):
        await ctx.send('Tapete: "Hallo Wand, na wie gehts?"\nWand: "Mir gehts ganz gut, du bist ja jetzt '
                       'rot-lila!"\nTapete: "ja, habe mich nun gefärbt. Toll nicht?"\nWand: "Ja is supi!"')

    @commands.command(name="wand", aliases=["comic2", "comic-2", "comic_2", "w"])
    async def Wand(self, ctx):
        await ctx.send('Tapete: "Hallo Wand hier spricht Tapete."\nWand: "Oh Hi Tapete, du bist lila!"\nTapete: "Klar '
                       'bin ich lila!"\nWand: "Ui, toll und wie gehts dir?"\nTapete: "Joar läuft... lila halt."')


def setup(bot):
    bot.add_cog(Commands(bot))
    print("--> Commands loaded")
