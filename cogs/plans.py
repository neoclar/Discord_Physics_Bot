import sys
sys.path.append("..")
import discord
from discord.ext import commands, tasks
import datetime
from random import randint, choice


class Plans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.good_morning.start()

    @tasks.loop(time=datetime.time(hour=4, minute=15, tzinfo=datetime.timezone.utc)) # Было 22, а принимал 19 => hour = 4
    async def good_morning(self):
        print('Good morning!')
        if datetime.date.today().isoweekday() < 6:
            embed = discord.Embed(title='Доброе Утро!', description='Пора идти в школу!', colour=discord.Colour(0).from_rgb(randint(0, 256), randint(0, 256), randint(0, 256)))
            # random_num = randint(1, 3)
            # file = discord.File(f"images/good_morning/{random_num}.png", filename="image.png")
            # embed.set_image(url=f"attachment://{random_num}.png")
            images = ['https://cdn.discordapp.com/attachments/873309724743991388/1154418231973519422/1.png',
                    'https://cdn.discordapp.com/attachments/873309724743991388/1154418232384573550/2.png',
                    'https://cdn.discordapp.com/attachments/873309724743991388/1154418233135341588/3.png',
                    'https://cdn.discordapp.com/attachments/873309724743991388/1154496797587275896/4.png',
                    'https://cdn.discordapp.com/attachments/873309724743991388/1154780340431368383/5.png']
            random_image = choice(images)
            embed.set_image(url=random_image)
            embed.set_footer(text=f'Мем №{images.index(random_image)+1}.')
            # embed.set_thumbnail(url=choice(images))
            channel = discord.utils.get(self.bot.get_all_channels(), name='bot_channel')
            await channel.send(content='@everyone', embed=embed)



async def setup(bot):
    await bot.add_cog(Plans(bot))
    print("import 'plans' is successful")
