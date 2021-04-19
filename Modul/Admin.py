import discord
from discord.ext import commands
from Secret import Secret


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if ctx.guild.id == Secret.Server_id:
            await ctx.message.delete()
            for Rolle in ctx.author.roles:
                if Rolle.id in Secret.Server_team:
                    channel = self.bot.get_channel(Secret.Mod_channel)
                    if reason is None:
                        await channel.send(f"der User {member} wurde von {ctx.author.name} gekickt")
                        await member.send(f'Du wurdest vom Server: {ctx.guild.name} gekickt.\nDu kannst gerne wieder '
                                          f'kommen jedoch ließ die die Regeln nochmal genauer durch')
                    else:
                        await channel.send(f"der User {member} wurde von {ctx.author.name} gekickt\n der Grund war {reason}")
                        await member.send(f'Du wurdest vom Server: {ctx.guild.name} gekickt.\nDer Grund des Kicks war {reason}\nDu kannst gerne wieder kommen jedoch ließ die die Regeln nochmal genauer durch')
                    await member.kick(reason=reason)

    @commands.command()
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if ctx.guild.id == Secret.Server_id:
            await ctx.message.delete()
            for Rolle in ctx.author.roles:
                if Rolle.id in Secret.Admin_team:
                    channel = self.bot.get_channel(Secret.Mod_channel)
                    if reason is None:
                        await channel.send(f"der User {member} wurde von {ctx.author.name} gebannt")
                        await member.send(f'Du wurdest vom Server: {ctx.guild.name} gebannt.')
                    else:
                        await channel.send(f"der User {member} wurde von {ctx.author.name} gebannt\n der Grund war {reason}")
                        await member.send(f'Du wurdest vom Server: {ctx.guild.name} gebannt.\nDer Grund des Kicks war {reason}')
                    await member.ban(reason=reason)


def setup(bot):
    bot.add_cog(Admin(bot))
    print("--> Admin loaded")
