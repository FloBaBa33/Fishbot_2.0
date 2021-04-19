import discord
from discord.ext import commands
from Secret import Secret


class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        elif message.author.bot is True:
            return
        elif message.content.startswith("."):
            return
        else:
            if message.guild is not None:
                author_id = str(message.author.id)
                guild_id = str(message.guild.id)
                xp = int((len(message.content)-5)/3)
                if xp > 10:
                    xp = 10
                elif xp < 0:
                    xp = 0
                user = await self.bot.pg_con.fetch("SELECT * from users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
                if not user:
                    await self.bot.pg_con.execute("INSERT INTO users (user_id, guild_id, lvl, xp) VALUES ($1, $2, 1, 0)", author_id, guild_id)
                user = await self.bot.pg_con.fetchrow("SELECT * from users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
                await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user["xp"] + xp, author_id, guild_id)
                if await self.lvl_up(user, author_id, guild_id):
                    await message.channel.send(f"{message.author.mention} is now level {user['lvl'] + 1}")

    async def lvl_up(self, user, author_id, guild_id):
        cur_xp = user["xp"]
        cur_exp = user["lvl"]
        req = int(100*(1.25**(cur_exp+1)))
        if cur_xp >= req:
            await self.bot.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id = $2 AND guild_id = $3", cur_exp + 1,
                                          user["user_id"], user["guild_id"])
            await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user["xp"] - req, author_id, guild_id)
            return True
        else:
            return False

    @commands.command(aliases=["rank", "rang"])
    async def level(self, ctx, member: discord.Member = None):
        if ctx.guild is not None:
            if ctx.channel.id == Secret.Bot_channel:
                member = ctx.author if not member else member
                member_id = str(member.id)
                guild_id = str(ctx.guild.id)
                user = await self.bot.pg_con.fetch("SELECT * from users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)
                if not user:
                    await ctx.send("Member has no Levels")
                else:
                    embed = discord.Embed(color=member.color, timestanp=ctx.message.created_at)
                    embed.set_author(name=f"Level - {member}", icon_url=member.avatar_url)
                    embed.add_field(name="Level", value=user[0]["lvl"])
                    embed.add_field(name="XP", value=user[0]["xp"])
                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Level(bot))
    print("-->Level loaded")
