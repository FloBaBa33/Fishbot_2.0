from discord.ext import commands

Emptychannel = 1


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        global Emptychannel
        if not before.channel:
            print(f"{member} jointe {after.channel}")
        elif before.channel is not None:
            if before.channel != after.channel and len(before.channel.members) == 0:
                Emptychannel = Emptychannel + 1
                if Emptychannel > 1:
                    await before.channel.delete()
                    Emptychannel = Emptychannel - 1
        elif after.channel is not None and before.channel != after.channel and len(after.channel.members) == 1:
            if Emptychannel == 1:
                await after.channel.clone(name="Katzen-Talk")
            else:
                Emptychannel = Emptychannel - 1


def setup(bot):
    bot.add_cog(Voice(bot))
    print("--> Voice loaded")
