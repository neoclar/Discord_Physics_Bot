import discord
from discord.ext import commands
from discord import app_commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="...")
    async def hello(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("И тебе привет!")


    @app_commands.command(name="notif", description="Команда-конструктор оповещений")
    @app_commands.describe(title='Заголовок оповещения',
                           text_up='Текст над выделенной частью. По умолчанию: "@everyone"',
                           title_comment='Текст под заголовком',
                           subtitle1='Подзаголовок 1',
                           subtitle1_comment='Текст под подзаголовком 1',
                           subtitle2='Подзаголовок 1',
                           subtitle2_comment='Текст под подзаголовком 1',
                           subtitle3='Подзаголовок 1',
                           subtitle3_comment='Текст под подзаголовком 1',
                           color='Цвет у веделенной части оповещения. Нужно указывать в формате RGB',
                           channel='Канал, на который будет отправлено оповещение')
    # @app_commands.choices(channel=[app_commands.Choice(name='bot_channel', value='1'), app_commands.Choice(name='bot_channel', value='2')]) # [channel for channel in self.bot.get_all_channels()]
    # @if not message.author.bot and not True in [role in self.bot.roles_without_mute for role in [role.name for role in message.author.roles]]:
    # @app_commands.checks.has_permissions()
    async def notif(self, interaction: discord.Interaction,
                    title: str,
                    text_up: str = '@everyone',
                    title_comment: str | None = None,
                    subtitle1: str | None = '',
                    subtitle1_comment: str | None = '',
                    subtitle2: str | None = '',
                    subtitle2_comment: str | None = '',
                    subtitle3: str | None = '',
                    subtitle3_comment: str | None = None,
                    color: str | None = '217, 105, 0',
                    channel: str | None = 'bot_channel') -> None: # typing.Union[str, app_commands.Choice[str]]
        if True in [role in self.bot.roles_notif for role in [role.name for role in interaction.user.roles]]:
            color_list = list(map(int, color.split(', ')))
            embed = discord.Embed(title=title, description=title_comment, colour=discord.Colour(0).from_rgb(color_list[0], color_list[1], color_list[2]))
            embed.add_field(name=subtitle1, value=subtitle1_comment, inline=False)
            embed.add_field(name=subtitle2, value=subtitle2_comment, inline=False)
            embed.add_field(name=subtitle3, value=subtitle3_comment, inline=False)
            channel_to_send = discord.utils.get(self.bot.get_all_channels(), name=channel)
            if channel_to_send==None:
                await interaction.response.send_message(content='Не получилось найти такой канал!', ephemeral=True)
            else:
                await channel_to_send.send(content=text_up, embed=embed)
                await interaction.response.send_message(content='Выполнено!')
        else:
            await interaction.response.send_message(content='Отказано в доступе!', ephemeral=True)





async def setup(bot):
    await bot.add_cog(Commands(bot))
    print("import 'commands' is successful")