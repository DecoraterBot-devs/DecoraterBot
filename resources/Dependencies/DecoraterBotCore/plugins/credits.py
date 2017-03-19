# coding=utf-8
"""
credits plugin for DecoraterBot.
"""
import traceback

from discord.ext import commands


class Credits:
    """
    Credits Commands Plugin Class.
    """
    def __init__(self, bot):
        self.bot = bot

    def botcommand(self):
        """Stores all command names in a dictionary."""
        self.bot.commands_list.append('credits')
        self.bot.commands_list.append('givecredits')
        self.bot.commands_list.append('balance')

    def __unload(self):
        """
        Clears registered commands.
        """
        self.bot.commands_list.remove('credits')
        self.bot.commands_list.remove('givecredits')
        self.bot.commands_list.remove('balance')

    @commands.command(name='credits', pass_context=True)
    async def credits_command(self, ctx):
        """
        ::credits Command for DecoraterBot.
        """
        try:
            current_credits = 0
            try:
                current_credits = self.bot.credits.getcredits(
                    str(ctx.message.author.id), 'credits')
            except (KeyError, TypeError):
                pass
            self.bot.credits.setcredits(
                str(ctx.message.author.id), 'credits', current_credits + 500)
            await self.bot.send_message(
                    ctx.message.channel,
                    ":atm:  |  {0}, you received your :dollar: 500 daily "
                    "credits!".format(
                        ctx.message.author.name))
        except Exception as ex:
            str(ex)
            await self.bot.send_message(
                    ctx.message.channel,
                    "Error: ```py\n{0}```".format(traceback.format_exc()))

    @commands.command(name='givecredits', pass_context=True)
    async def givecredits_command(self, ctx):
        """
        ::givecredits Command for DecoraterBot.
        """
        try:
            current_credits = 0
            try:
                current_credits = self.bot.credits.getcredits(
                    str(ctx.message.author.id), 'credits')
            except (KeyError, TypeError):
                pass
            self.bot.credits.setcredits(
                str(ctx.message.author.id), 'credits',
                current_credits + 5000000)
            await self.bot.send_message(
                    ctx.message.channel,
                    ":atm:  |  {0}, you received :dollar: 5000000 "
                    "credits!".format(ctx.message.author.name))
        except Exception as ex:
            str(ex)
            await self.bot.send_message(
                    ctx.message.channel,
                    "Error: ```py\n{0}```".format(traceback.format_exc()))

    @commands.command(name='balance', pass_context=True)
    async def balance_command(self, ctx):
        """
        ::balance Command for DecoraterBot.
        """
        try:
            current_credits = 0
            try:
                current_credits = self.bot.credits.getcredits(
                    str(ctx.message.author.id), 'credits')
            except (KeyError, TypeError):
                pass
            await self.bot.send_message(
                    ctx.message.channel,
                    "{0}, you have {1} credits!".format(
                        ctx.message.author.name, current_credits))
        except Exception as ex:
            str(ex)
            await self.bot.send_message(
                    ctx.message.channel,
                    "Error: ```py\n{0}```".format(traceback.format_exc()))


def setup(bot):
    """
    DecoraterBot's Credits Plugin.
    """
    new_cog = Credits(bot)
    new_cog.botcommand()
    bot.add_cog(new_cog)
