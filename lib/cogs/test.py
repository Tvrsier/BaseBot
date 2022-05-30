from disnake.ext.commands import *

class test(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content:
            await message.channel.send(f'{message.content}')

    @command()
    async def test(self, ctx):
        await ctx.send('test')

def setup(bot):
    bot.add_cog(test(bot))