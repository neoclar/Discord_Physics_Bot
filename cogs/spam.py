import sys
sys.path.append("..")
import asyncio
import discord
from discord.ext import commands
from SQL import *
import datetime

class Everyone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        user_roles = [role.name for role in message.author.roles]
        if not message.author.bot and not True in [role in self.bot.roles_without_mute for role in user_roles]:
            # print(discord.member.Member.roles)
            # print(message.author.roles)#.has_any_role('Гоблинский'))
            messages_of_user = convert_dict(get(table='messages', where_obj='user_id', where_value=message.author.id))
            if not len(messages_of_user): # Для новых участников
                add_string(table='messages', user_id=message.author.id)
            if not None in list(messages_of_user.values()):
                print('Обнаружен многочисленный спам!')
                await self.ban(message, self.bot.ban_time['spam'], reason='Превышение лимита сообщений')
                await message.delete()
            else:
                none_message = list(messages_of_user.values()).index(None)
                change(table='messages', parameter=f'message{none_message}', set_obj=message.content, where_obj='user_id', where_value=message.author.id)
                messages = list(convert_dict(get(table='messages', where_obj='user_id', where_value=message.author.id)).values())
                messages.pop(0)
                messages = [x for x in messages if x is not None]
                # print(messages)
                if len(set(messages))<len(messages)-1:
                    print('Обнаружен повторяющийся спам!')
                    await self.ban(message, self.bot.ban_time['spam'], reason='Отправка повторяющегося сообщения')

    async def delete_message(self, message):
        await message.delete()

    async def ban(self, message, time_for_mute: datetime.timedelta, reason='Нарушение правил сервера'):
        await message.author.timeout(time_for_mute, reason=reason)
        messages = list(convert_dict(get(table='messages', where_obj='user_id', where_value=message.author.id)).values())
        author_id = messages.pop(0)
        messages = [x for x in messages if x is not None]
        del_mess_num = 0
        beautiful_mess=''
        async for message_h in message.channel.history(limit=10):
            if message_h.content in messages and message_h.author.id == author_id:
                del_mess_num+=1
                del_mess = message_h.content.replace("\n", "\n   ")
                beautiful_mess = f'{beautiful_mess}\n{del_mess_num}. "{del_mess}"'
                task = asyncio.create_task(self.delete_message(message_h))
                await task
        embed = discord.Embed(title='Причина:', description=reason, colour=discord.Colour(0).from_rgb(217, 105, 0))
        embed.add_field(name='Удалённые сообщения:', value=beautiful_mess)
        await self.bot.channel.send(content=f'Участник {message.author.mention} получил мут на 10 минут.', embed=embed)

# one = ['2', '2'] # user have
# two = ['4', '3'] # db have
# print(True in [role in two for role in one])


async def setup(bot):
    await bot.add_cog(Everyone(bot))
    print("import 'everyone' is successful")

