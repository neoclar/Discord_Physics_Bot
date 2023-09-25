import discord
from discord.ext import commands

class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.clear_db.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged as {self.bot._application.name}!')
        # await self.bot.wait_until_ready()
        self.bot.channel = discord.utils.get(self.bot.get_all_channels(), name='bot_channel')
        await self.bot.tree.sync()
        await self.bot.channel.send(embed=discord.Embed(title='Бот готов к работе!', colour=discord.Colour(0).from_rgb(64, 237, 197)))
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('ломание законов физики'))
        # await self.bot.wait_until_ready()



async def setup(bot):
    await bot.add_cog(Init(bot))
    print("import 'init' is successful")