# coding=utf-8
"""
Bug Reporting plugin for DecoraterBot.

This is for getting DecoraterBot's new bugtracker.
"""

import discord
from discord.ext import commands


class Report:
    """
    Report Commands Extension.
    """
    def __init__(self, bot):
        self.bot = bot

    def botcommand(self):
        """Stores all command names in a dictionary."""
        self.bot.commands_list.append('report')

    def __unload(self):
        """
        Clears registered commands.
        """
        self.bot.commands_list.remove('report')

    @commands.command(name='report', pass_context=True, no_pm=True)
    async def report_command(self, ctx):
        await self.bot.send_message(ctx.message.channel,
                                    "To report issues for DecoraterBot please "
                                    "go to: <https://bitbucket.org/AraHaan/"
                                    "decoraterbot/issues>")

def setup(bot):
    """
    DecoraterBot's Bug Reporting Plugin.
    """
    new_cog = Report(bot)
    new_cog.botcommand()
    bot.add_cog(new_cog)
