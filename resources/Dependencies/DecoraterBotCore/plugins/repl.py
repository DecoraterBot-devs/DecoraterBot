# coding=utf-8
"""
repl plugin for DecoraterBot.
"""

import traceback
import inspect
from contextlib import redirect_stdout
import io

import discord
from discord.ext import commands


class REPL:
    """
    repl Plugin class.
    """
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()

    def botcommand(self):
        """Stores all command names in a dictionary."""
        self.bot.commands_list.append('repl')

    def __unload(self):
        """
        Clears registered commands.
        """
        self.bot.commands_list.remove('repl')

    @staticmethod
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @staticmethod
    def get_syntax_error(e):
        """Gets SyntaxErrors."""
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(
            e, '^', type(e).__name__)

    @commands.command(pass_context=True, hidden=True)
    async def repl(self, ctx):
        """adds / removes a repl session."""
        if ctx.message.author.id != self.bot.discord_user_id:
            return
        code = None
        msg = ctx.message

        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': msg,
            'server': msg.server,
            'channel': msg.channel,
            'author': msg.author,
            'last': None,
        }

        if msg.channel.id in self.sessions:
            await self.bot.say('Already running a REPL session in this '
                               'channel. Exit it with `quit`.')
            return

        self.sessions.add(msg.channel.id)
        await self.bot.say('Enter code to execute or evaluate. `exit()` or '
                           '`quit` to exit.')
        while True:
            response = await self.bot.wait_for_message(
                author=msg.author, channel=msg.channel,
                check=lambda m: m.content.startswith('`'))

            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await self.bot.say('Exiting.')
                self.sessions.remove(msg.channel.id)
                return

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await self.bot.say(self.get_syntax_error(e))
                    continue

            variables['message'] = response

            fmt = None
            stdout = io.StringIO()

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                str(e)  # to shut PyCharm up.
                value = stdout.getvalue()
                fmt = '{}{}\n'.format(value, traceback.format_exc())
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = '{}{}\n'.format(value, result)
                    variables['last'] = result
                elif value:
                    fmt = '{}\n'.format(value)

            try:
                if fmt is not None:
                    if len(fmt) > 2000:
                        for i in range(0, len(fmt), 1990):
                            await self.bot.send_message(msg.channel,
                                                        '```py\n{}```'.format(
                                                            fmt[i:i+1990]))
                    else:
                        await self.bot.send_message(msg.channel,
                                                    '```py\n{}```'.format(fmt))
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await self.bot.send_message(msg.channel,
                                            'Unexpected error: `{}`'.format(e))


def setup(bot):
    """Adds plugin commands."""
    new_cog = REPL(bot)
    new_cog.botcommand()
    bot.add_cog(new_cog)
