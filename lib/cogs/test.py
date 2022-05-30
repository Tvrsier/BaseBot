from disnake.ext.commands import *

class Test(Cog): #This is the test cog
    def __init__(self, bot):#Create the constructor as you would do in a normal cog
        self.bot = bot

    @Cog.listener() #On message example
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content:
            await message.channel.send(f'{message.content}')

    @command()#Command example
    async def test(self, ctx):
        await ctx.send('test')

    @Cog.listener()#This listener is necessary to make every cog work
    async def on_ready(self):#Called when the cog is ready
        if not self.bot.ready:#If the parameter bot.ready is False then we will need to set this cog as ready to the Ready object in the bot
            self.bot.cogs_ready.ready_up("test") #Call the ready_up method from the Ready object and pass the name of the cog file as a parameter. The string is case sensitive

def setup(bot):#Create a setup function as you would do in a normal cog
    bot.add_cog(Test(bot))
