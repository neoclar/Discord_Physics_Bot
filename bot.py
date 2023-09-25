import os
import discord
from discord.ext import commands, tasks
import asyncio
from SQL import *

import datetime
class My_bot(commands.Bot):
    def init(self):
        self.remove_command("help")
        self.ban_time = {'spam': datetime.timedelta(seconds=10)}
        self.roles_without_mute = ['Гоблинский']
        self.roles_notif = ['Гоблинский']


    @tasks.loop(seconds=10.0)
    async def clear_db(self):
        for i in range(5): delete_column(table='messages', parameter='message'+str(i+1))

intents=discord.Intents().all()
intents.members = True
token = 'MTE1MjMzNTcxNzMyMjczMTYyMg.Gs5rnw.Hc15Qd0bnTirfsIfMeOVNnDesPUjTv1f2e9al8'
bot = My_bot(command_prefix='$', intents=intents)
bot.init()
# asyncio.run(bot.init())

@bot.command()
@commands.has_any_role('Гоблинский')
async def load(ctx, extensions):
    bot.load_extension(f'cogs.{extensions}')
    await ctx.send(f"load module: cogs.{extensions}")
    print(f"load module: cogs.{extensions}")

@bot.command()
@commands.has_any_role('Гоблинский')
async def unload(ctx, extensions):
    bot.unload_extension(f'cogs.{extensions}')
    await ctx.send(f"unload module: cogs.{extensions}")
    print(f"unload module: cogs.{extensions}")

@bot.command()
@commands.has_any_role('Гоблинский')
async def reload(ctx, extensions):
    bot.unload_extension(f'cogs.{extensions}')
    bot.load_extension(f'cogs.{extensions}')
    await ctx.send(f"reload module: cogs.{extensions}")
    await ctx.send(f"reload module: cogs.{extensions}")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
    

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

try: asyncio.run(main())
except KeyboardInterrupt: print('Бот остановлен')
# bot.run(token)
