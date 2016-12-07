# coding=utf-8
"""
The MIT License (MIT)

Copyright (c) 2015-2016 AraHaan

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import json
import platform
import random
import subprocess
import sys
import traceback
import discord
from discord.ext import commands
try:
    import TinyURL
    disabletinyurl = False
except ImportError:
    print_data_001 = 'TinyURL for Python 3.x was not installed.\n'
    print_data_001 += 'It can be found at: https://github.com/AraHaan/TinyURL\n'
    print_data_001 += 'Disabled the tinyurl command for now.'
    print(print_data_001)
    disabletinyurl = True
    TinyURL = None


class BotCommands:
    """
    Basic Message Commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.disabletinyurl = disabletinyurl
        self.version = str(self.bot.consoletext['WindowVersion'][0])
        self.rev = str(self.bot.consoletext['Revision'][0])
        self.sourcelink = str(self.bot.botmessages['source_command_data'][0])
        self.othercommands = str(self.bot.botmessages['commands_command_data'][1])
        self.commandstuff = str(self.bot.botmessages['commands_command_data'][4])
        self.botcommands = str(
            self.bot.botmessages['commands_command_data'][0]) + self.othercommands + self.commandstuff
        self.botcommands_without_other_stuff = str(
            self.bot.botmessages['commands_command_data'][0]) + self.othercommands
        self.othercommandthings = str(self.bot.botmessages['commands_command_data'][4]) + str(
            self.bot.botmessages['commands_command_data'][5])
        self.botcommandswithturl_01 = str(self.bot.botmessages['commands_command_data'][3]) + self.othercommandthings
        self.botcommandswithtinyurl = self.botcommands_without_other_stuff + self.botcommandswithturl_01
        self.changelog = str(self.bot.botmessages['changelog_data'][0])
        self.info = "``" + str(self.bot.consoletext['WindowName'][0]) + self.version + self.rev + "``"
        self.botcommandsPM = str(self.bot.botmessages['commands_command_data'][2])
        self.commandturlfix = str(self.bot.botmessages['commands_command_data'][5])
        self.botcommandsPMwithtinyurl = self.botcommandsPM + str(
            self.bot.botmessages['commands_command_data'][3]) + self.commandturlfix
        self.sent_prune_error_message = False
        self.tinyurlerror = False
        self.link = None
        self.member_list = []
        self.hook_url = None
        self.payload = {}
        self.header = {}

    @commands.command(name='attack', pass_context=True, no_pm=True)
    async def attack_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Message Context.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            for user in ctx.message.mentions:
                await self.bot.send_message(user, content=str(self.bot.botmessages['attack_command_data'][0]))
                break
            else:
                await self.bot.send_message(ctx.message.author,
                                            content=str(self.bot.botmessages['attack_command_data'][1]))

    @commands.command(name='coin', pass_context=True, no_pm=True)
    async def coin_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            msg = random.randint(0, 1)
            if msg == 0:
                heads_coin = "{0}{1}resources{1}images{1}coins{1}Heads.png".format(self.bot.path, self.bot.sepa)
                try:
                    await self.bot.send_file(ctx.message.channel, heads_coin)
                except discord.errors.Forbidden:
                    try:
                        message_data = str(self.bot.botmessages['coin_command_data'][0])
                        await self.bot.send_message(ctx.message.channel, content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
            if msg == 1:
                tails_coin = "{0}{1}resources{1}images{1}coins{1}Tails.png".format(self.bot.path, self.bot.sepa)
                try:
                    await self.bot.send_file(ctx.message.channel, tails_coin)
                except discord.errors.Forbidden:
                    try:
                        message_data = str(self.bot.botmessages['coin_command_data'][0])
                        await self.bot.send_message(ctx.message.channel, content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.group(name='color', pass_context=True, no_pm=True)
    async def color_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        if ctx.invoked_subcommand is None:
            return

    @color_command.command(name='pink', pass_context=True, no_pm=True)
    async def pink_subcommand(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        desrole = ctx.message.content[
                  len(self.bot.bot_prefix + "color " + self.bot.bot_prefix + "pink "):].strip()
        role2 = discord.utils.find(lambda role: role.name == desrole, ctx.message.channel.server.roles)
        try:
            await self.bot.edit_role(ctx.message.channel.server, role2, color=discord.Colour(int('ff3054', 16)))
        except discord.errors.Forbidden:
            try:
                message_data = str(self.bot.botmessages['color_command_data'][0])
                await self.bot.send_message(ctx.message.channel, content=message_data)
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
        except discord.errors.HTTPException:
            return
        except AttributeError:
            return

    @color_command.command(name='brown', pass_context=True, no_pm=True)
    async def brown_subcommand(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        desrole = ctx.message.content[
                  len(self.bot.bot_prefix + "color " + self.bot.bot_prefix + "brown "):].strip()
        role2 = discord.utils.find(lambda role: role.name == desrole, ctx.message.channel.server.roles)
        try:
            await self.bot.edit_role(ctx.message.channel.server, role2, color=discord.Colour(int('652d2d', 16)))
        except discord.errors.Forbidden:
            try:
                message_data = str(self.bot.botmessages['color_command_data'][0])
                await self.bot.send_message(ctx.message.channel, content=message_data)
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
        except discord.errors.HTTPException:
            pass
        except AttributeError:
            pass

    @commands.command(name='eval', pass_context=True, no_pm=True)
    async def eval_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id == self.bot.owner_id:
            debugcode = ctx.message.content[len(self.bot.bot_prefix + "eval "):].strip()
            if debugcode.rfind('await self.bot.send_message(ctx.message.channel, content=') is not -1:
                debugcode = debugcode[len("await self.bot.send_message(ctx.message.channel, content="):].strip()
                debugcode = debugcode.strip(")")
                if debugcode.find("'") is not -1:
                    debugcode = debugcode.strip("'")
                elif debugcode.find('"') is not -1:
                    debugcode = debugcode.strip('"')
                if debugcode.find('ctx.message.author.mention') is not -1:
                    debugcode = debugcode.replace('ctx.message.author.mention + "', ctx.message.author.mention)
                    await self.bot.send_message(ctx.message.channel, content=debugcode)
            else:
                botowner = discord.utils.find(lambda member: member.id == self.bot.owner_id,
                                              ctx.message.channel.server.members)
                try:
                    try:
                        debugcode = eval(debugcode)
                    except SystemExit:
                        pass
                    debugcode = "```py\n" + str(debugcode) + "\n```"
                    try:
                        await self.bot.send_message(ctx.message.channel, content=debugcode)
                    except discord.errors.Forbidden:
                        msgdata = str(self.bot.botmessages['eval_command_data'][0])
                        message_data = msgdata.format(ctx.message.channel.server.name, ctx.message.channel.name)
                        await self.bot.send_message(botowner, content=message_data)
                        await self.bot.send_message(botowner, content=debugcode)
                    except discord.errors.HTTPException:
                        if len(debugcode) > 2000:
                            result_info = str(self.bot.botmessages['eval_command_data'][1])
                            await self.bot.send_message(ctx.message.channel, content=result_info)
                except Exception as e:
                    str(e)
                    debugcode = traceback.format_exc()
                    debugcode = str(debugcode)
                    try:
                        await self.bot.send_message(ctx.message.channel, content="```py\n" + debugcode + "\n```")
                    except discord.errors.Forbidden:
                        msgdata = str(self.bot.botmessages['eval_command_data'][0])
                        message_data = msgdata.format(ctx.message.channel.server.name, ctx.message.channel.name)
                        await self.bot.send_message(botowner, content=message_data)
                        await self.bot.send_message(botowner, content="```py\n" + debugcode + "\n```")
        else:
            try:
                result_info = str(self.bot.botmessages['eval_command_data'][2])
                await self.bot.send_message(ctx.message.channel, content=result_info)
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='debug', pass_context=True, no_pm=True)
    async def debug_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id == self.bot.owner_id:
            debugcode_new = "# coding=utf-8\n" + ctx.message.content[len(self.bot.bot_prefix + "debug "):].strip()
            botowner = discord.utils.find(lambda member: member.id == self.bot.owner_id,
                                          ctx.message.channel.server.members)
            try:
                evalcodefile = '{0}{1}resources{1}exec_files{1}exec_temp.py'.format(self.bot.path, self.bot.sepa)
                eval_temp_code = open(evalcodefile, 'w+', encoding='utf-8')
                debugcode_new += '\n'
                eval_temp_code.write(debugcode_new)
                eval_temp_code.close()
                execoutputfile = '{0}{1}resources{1}exec_files{1}exec_output_temp.txt'.format(self.bot.path,
                                                                                              self.bot.sepa)
                eval_temp_result_output = open(execoutputfile, 'w', encoding='utf-8')
                out = eval_temp_result_output
                p = subprocess.Popen("{0}{1}python {2}".format(sys.path[4], self.bot.sepa, evalcodefile),
                                     stdout=out,
                                     stderr=out, shell=True)
                p.wait()
                eval_temp_result_output.close()
                eval_temp_result_read = open(execoutputfile, encoding='utf-8')
                eval_result = eval_temp_result_read.read()
                if eval_result is not '':
                    debugcode = eval_result
                else:
                    debugcode = 'None'
                eval_temp_result_read.close()
                try:
                    await self.bot.send_message(ctx.message.channel, content="```py\n" + debugcode + "\n```")
                except discord.errors.Forbidden:
                    msgdata = str(self.bot.botmessages['eval_command_data'][0])
                    message_data = msgdata.format(ctx.message.channel.server.name, ctx.message.channel.name)
                    await self.bot.send_message(botowner, content=message_data)
                    await self.bot.send_message(botowner, content="```py\n" + debugcode + "\n```")
                except discord.errors.HTTPException:
                    if len(debugcode) > 2000:
                        result_info = str(self.bot.botmessages['eval_command_data'][1])
                        await self.bot.send_message(ctx.message.channel, content=result_info)
            except Exception as e:
                str(e)
                debugcode = traceback.format_exc()
                debugcode = str(debugcode)
                try:
                    await self.bot.send_message(ctx.message.channel, content="```py\n" + debugcode + "\n```")
                except discord.errors.Forbidden:
                    msgdata = str(self.bot.botmessages['eval_command_data'][0])
                    message_data = msgdata.format(ctx.message.channel.server.name, ctx.message.channel.name)
                    await self.bot.send_message(botowner, content=message_data)
                    await self.bot.send_message(botowner, content="```py\n" + debugcode + "\n```")
        else:
            try:
                result_info = str(self.bot.botmessages['debug_command_data'][0])
                await self.bot.send_message(ctx.message.channel, content=result_info)
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    # This command below is not working well.

    @commands.command(name='game', pass_context=True, no_pm=False)
    async def game_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        elif ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            desgame, desgametype, stream_url, desgamesize = self.bot.game_command_helper(ctx)
            if desgamesize < 1:
                await self.bot.send_message(ctx.message.channel, 'No game name was provided.')
            elif desgametype is not None:
                if self.bot.log_games:
                    self.bot.DBLogs.gamelog(ctx, desgame)
                await self.bot.change_presence(
                    game=discord.Game(name=desgame, type=desgametype, url=stream_url), status='online')
                try:
                    await self.bot.send_message(ctx.message.channel, content=str(
                        self.bot.botmessages['game_command_data'][0]).format(desgame).replace("idle", "streaming"))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
            elif desgametype is None:
                if self.bot.log_games:
                    self.bot.DBLogs.gamelog(ctx, desgame)
                await self.bot.change_presence(game=discord.Game(name=desgame), status='idle')
                try:
                    await self.bot.send_message(ctx.message.channel, content=str(
                        self.bot.botmessages['game_command_data'][0]).format(desgame))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='remgame', pass_context=True, no_pm=False)
    async def remgame_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            game_name = str(self.bot.consoletext['On_Ready_Game'][0])
            stream_url = "https://twitch.tv/decoraterbot"
            await self.bot.change_presence(game=discord.Game(name=game_name, type=1, url=stream_url))
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(self.bot.botmessages['remgame_command_data'][0]))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='join', pass_context=True, no_pm=False)
    async def join_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            if self.bot.is_official_bot:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(self.bot.botmessages['join_command_data'][3]))
            else:
                code = ctx.message.content[len(self.bot.bot_prefix + "join "):].strip()
                if code == '':
                    url = None
                else:
                    url = code
                if url is not None:
                    try:
                        await self.bot.accept_invite(url)
                        msg_data = str(self.bot.botmessages['join_command_data'][0])
                        await self.bot.send_message(ctx.message.channel, content=msg_data)
                    except discord.errors.NotFound:
                        msg_data = str(self.bot.botmessages['join_command_data'][1])
                        await self.bot.send_message(ctx.message.channel, content=msg_data)
                else:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['join_command_data'][2]))

    @commands.command(name='kill', pass_context=True, no_pm=False)
    async def kill_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            data = ctx.message.content[len(self.bot.bot_prefix + "kill "):].strip()
            if ctx.message.channel.is_private:
                msg = random.randint(1, 4)
                if msg == 1:
                    message_data = str(self.bot.botmessages['kill_command_data'][0]).format(ctx.message.author)
                    await self.bot.send_message(ctx.message.channel, content=message_data)
                if msg == 2:
                    message_data = str(self.bot.botmessages['kill_command_data'][1]).format(ctx.message.author)
                    await self.bot.send_message(ctx.message.channel, content=message_data)
                if msg == 3:
                    message_data = str(self.bot.botmessages['kill_command_data'][2]).format(ctx.message.author)
                    await self.bot.send_message(ctx.message.channel, content=message_data)
                if msg == 4:
                    message_data = str(self.bot.botmessages['kill_command_data'][3]).format(ctx.message.author)
                    await self.bot.send_message(ctx.message.channel, content=message_data)
            else:
                if data.rfind(self.bot.user.name) != -1:
                    try:
                        msg_data = str(self.bot.botmessages['kill_command_data'][4])
                        await self.bot.send_message(ctx.message.channel, content=msg_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                else:
                    msg = random.randint(1, 4)
                    for disuser in ctx.message.mentions:
                        if ctx.message.author == disuser:
                            try:
                                msg_data = str(self.bot.botmessages['kill_command_data'][4])
                                await self.bot.send_message(ctx.message.channel, content=msg_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                            break
                        if self.bot.user == disuser:
                            try:
                                msg_data = str(self.bot.botmessages['kill_command_data'][4])
                                await self.bot.send_message(ctx.message.channel, content=msg_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                            break
                        user = discord.utils.find(lambda member: member.name == disuser.name,
                                                  ctx.message.channel.server.members)
                        if msg == 1:
                            try:
                                msgdata = str(self.bot.botmessages['kill_command_data'][5]).format(ctx.message.author,
                                                                                                   user)
                                message_data = msgdata
                                await self.bot.send_message(ctx.message.channel, content=message_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                            break
                        if msg == 2:
                            try:
                                msgdata = str(self.bot.botmessages['kill_command_data'][6]).format(ctx.message.author,
                                                                                                   user)
                                message_data = msgdata
                                await self.bot.send_message(ctx.message.channel, content=message_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                            break
                        if msg == 3:
                            try:
                                msgdata = str(self.bot.botmessages['kill_command_data'][7]).format(ctx.message.author,
                                                                                                   user)
                                message_data = msgdata
                                await self.bot.send_message(ctx.message.channel, content=message_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                            break
                        if msg == 4:
                            try:
                                msgdata = str(self.bot.botmessages['kill_command_data'][8]).format(ctx.message.author,
                                                                                                   user)
                                message_data = msgdata
                                await self.bot.send_message(ctx.message.channel, content=message_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                            break
                    else:
                        if msg == 1:
                            try:
                                message_data = str(self.bot.botmessages['kill_command_data'][0]).format(
                                    ctx.message.author)
                                await self.bot.send_message(ctx.message.channel, content=message_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                        if msg == 2:
                            try:
                                message_data = str(self.bot.botmessages['kill_command_data'][1]).format(
                                    ctx.message.author)
                                await self.bot.send_message(ctx.message.channel, content=message_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                        if msg == 3:
                            try:
                                message_data = str(self.bot.botmessages['kill_command_data'][2]).format(
                                    ctx.message.author)
                                await self.bot.send_message(ctx.message.channel, message_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                        if msg == 4:
                            try:
                                message_data = str(self.bot.botmessages['kill_command_data'][3]).format(
                                    ctx.message.author)
                                await self.bot.send_message(ctx.message.channel, content=message_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='ignorechannel', pass_context=True, no_pm=False)
    async def ignorechannel_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id not in self.bot.ignoreslist["channels"]:
            try:
                self.bot.ignoreslist["channels"].append(ctx.message.channel.id)
                json.dump(self.bot.ignoreslist, open("{0}{1}resources{1}ConfigData{1}IgnoreList.json".format(
                    self.bot.path, self.bot.sepa), "w"))
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['Ignore_Channel_Data'][0]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
            except Exception as e:
                str(e)
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['Ignore_Channel_Data'][1]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='unignorechannel', pass_context=True, no_pm=False)
    async def unignorechannel_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            try:
                ignored = self.bot.ignoreslist["channels"]
                ignored.remove(ctx.message.channel.id)
                json.dump(self.bot.ignoreslist, open("{0}{1}resources{1}ConfigData{1}IgnoreList.json".format(
                    self.bot.path, self.bot.sepa), "w"))
                msg_info = str(self.bot.botmessages['Unignore_Channel_Data'][0])
                try:
                    await self.bot.send_message(ctx.message.channel, content=msg_info)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
            except Exception as e:
                str(e)
                msg_info = str(self.bot.botmessages['Unignore_Channel_Data'][1])
                try:
                    await self.bot.send_message(ctx.message.channel, content=msg_info)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='ban', pass_context=True, no_pm=True)
    async def ban_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander', ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            for disuser in ctx.message.mentions:
                listdata = ctx.message.channel.server.members
                member2 = discord.utils.find(lambda member: member.name == disuser.name, listdata)
                try:
                    await self.bot.ban(member2, delete_message_days=7)
                    try:
                        message_data = str(self.bot.botmessages['ban_command_data'][0]).format(member2)
                        await self.bot.send_message(ctx.message.channel, content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                except discord.Forbidden:
                    try:
                        await self.bot.send_message(ctx.message.channel, content=str(
                            self.bot.botmessages['ban_command_data'][1]))
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                except discord.HTTPException:
                    try:
                        await self.bot.send_message(ctx.message.channel, content=str(
                            self.bot.botmessages['ban_command_data'][2]))
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                break
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['ban_command_data'][3]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(self.bot.botmessages['ban_command_data'][4]))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='softban', pass_context=True, no_pm=True)
    async def softban_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander', ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            for disuser in ctx.message.mentions:
                memberlist = ctx.message.channel.server.members
                member2 = discord.utils.find(lambda member: member.name == disuser.name, memberlist)
                try:
                    await self.bot.ban(member2, delete_message_days=7)
                    await self.bot.unban(member2.server, member2)
                    try:
                        message_data = str(self.bot.botmessages['softban_command_data'][0]).format(member2)
                        await self.bot.send_message(ctx.message.channel, content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                except discord.Forbidden:
                    try:
                        msg_data = str(self.bot.botmessages['softban_command_data'][1])
                        await self.bot.send_message(ctx.message.channel, content=msg_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                except discord.HTTPException:
                    try:
                        msg_data = str(self.bot.botmessages['softban_command_data'][2])
                        await self.bot.send_message(ctx.message.channel, content=msg_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                break
            else:
                try:
                    await self.bot.send_message(ctx.message.channel, content=str(
                        self.bot.botmessages['softban_command_data'][3]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(self.bot.botmessages['softban_command_data'][4]))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='kick', pass_context=True, no_pm=True)
    async def kick_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander', ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            for disuser in ctx.message.mentions:
                memberlist = ctx.message.channel.server.members
                member2 = discord.utils.find(lambda member: member.name == disuser.name, memberlist)
                try:
                    await self.bot.kick(member2)
                    try:
                        message_data = str(self.bot.botmessages['kick_command_data'][0]).format(member2)
                        await self.bot.send_message(ctx.message.channel, content=message_data)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                except discord.Forbidden:
                    try:
                        await self.bot.send_message(ctx.message.channel, content=str(
                            self.bot.botmessages['kick_command_data'][1]))
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                except discord.HTTPException:
                    try:
                        await self.bot.send_message(ctx.message.channel, content=str(
                            self.bot.botmessages['kick_command_data'][2]))
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                break
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['kick_command_data'][3]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(self.bot.botmessages['kick_command_data'][4]))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='commands', pass_context=True, no_pm=False)
    async def commands_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            if ctx.message.channel.is_private:
                if self.disabletinyurl:
                    await self.bot.send_message(ctx.message.channel, content=self.botcommandsPM)
                else:
                    await self.bot.send_message(ctx.message.channel, content=self.botcommandsPMwithtinyurl)
            else:
                if self.disabletinyurl:
                    try:
                        if self.bot.pm_commands_list:
                            await self.bot.send_message(ctx.message.author, content=self.botcommands)
                        else:
                            await self.bot.send_message(ctx.message.channel, content=self.botcommands)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                else:
                    try:
                        if self.bot.pm_commands_list:
                            await self.bot.send_message(ctx.message.author, content=self.botcommandswithtinyurl)
                            msgdata = str(self.bot.botmessages['commands_command_data'][6])
                            message_data = msgdata.format(ctx.message.author.mention)
                            try:
                                await self.bot.send_message(ctx.message.channel, content=message_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                        else:
                            await self.bot.send_message(ctx.message.channel, content=self.botcommandswithtinyurl)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='changelog', pass_context=True, no_pm=False)
    async def changelog_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=self.changelog.format(self.version + self.rev))
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='raid', pass_context=True, no_pm=True)
    async def raid_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            if ctx.message.channel.is_private:
                return
            else:
                result = ctx.message.content.replace("::raid", "")
                if result.startswith(" "):
                    result = result[len(" "):].strip()
                try:
                    message_data = str(self.bot.botmessages['raid_command_data'][0]).format(result)
                    await self.bot.send_message(ctx.message.channel, content=message_data)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='update', pass_context=True, no_pm=True)
    async def update_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            if ctx.message.channel.is_private:
                return
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.bot.botmessages['update_command_data'][0]).format(
                                                    self.info))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='Libs', pass_context=True, no_pm=False)
    async def libs_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            libs = str(self.bot.botmessages['Libs_command_data'][0])
            try:
                await self.bot.send_message(ctx.message.channel, content=libs)
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='source', pass_context=True, no_pm=False)
    async def source_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            try:
                msgdata = self.sourcelink.format(ctx.message.author)
                message_data = msgdata
                await self.bot.send_message(ctx.message.channel, content=message_data)
            except discord.errors.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='type', pass_context=True, no_pm=False)
    async def type_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            await self.bot.send_typing(ctx.message.channel)

    @commands.command(name='pyversion', pass_context=True, no_pm=True)
    async def pyversion_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            if ctx.message.channel.is_private:
                return
            else:
                python_platform = None
                if self.bot.bits == 8:
                    python_platform = "64-Bit"
                elif self.bot.bits == 4:
                    python_platform = "32-Bit"
                vers = "```py\nPython v{0} {1}```".format(platform.python_version(), python_platform)
                try:
                    await self.bot.send_message(ctx.message.channel, content=vers)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='AgarScrub', pass_context=True, no_pm=True)
    async def agarscrub_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        try:
            reply = 'https://imgflip.com/i/12yq2n'
            await self.bot.send_message(ctx.message.channel, content=reply)
        except discord.errors.Forbidden:
            await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='stats', pass_context=True, no_pm=True)
    async def stats_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        server_count = str(len(self.bot.servers))
        member_count = str(len(set([member for member in self.bot.get_all_members()])))
        textchannels_count = str(len(set(
            [channel for channel in self.bot.get_all_channels() if channel.type == discord.ChannelType.text])))
        formatted_data = str(
            self.bot.botmessages['stats_command_data'][0]).format(server_count, member_count, textchannels_count)
        await self.bot.send_message(ctx.message.channel, content=formatted_data)

    @commands.command(name='rs', pass_context=True, no_pm=False)
    async def rs_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        filename1 = '{0}{1}resources{1}images{1}elsword{1}RS.jpg'.format(self.bot.path, self.bot.sepa)
        file_object = open(filename1, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='as', pass_context=True, no_pm=False)
    async def as_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        filename2 = '{0}{1}resources{1}images{1}elsword{1}AS.jpg'.format(self.bot.path, self.bot.sepa)
        file_object = open(filename2, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='ai', pass_context=True, no_pm=False)
    async def ai_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        filename3 = '{0}{1}resources{1}images{1}elsword{1}AI.jpg'.format(self.bot.path, self.bot.sepa)
        file_object = open(filename3, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='lk', pass_context=True, no_pm=False)
    async def lk_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        filename4 = '{0}{1}resources{1}images{1}elsword{1}LK.jpg'.format(self.bot.path, self.bot.sepa)
        file_object = open(filename4, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='vp', pass_context=True, no_pm=False)
    async def vp_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        filename5 = '{0}{1}resources{1}images{1}elsword{1}VP.jpg'.format(self.bot.path, self.bot.sepa)
        file_object = open(filename5, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='ws', pass_context=True, no_pm=False)
    async def ws_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        filename6 = '{0}{1}resources{1}images{1}elsword{1}WS.jpg'.format(self.bot.path, self.bot.sepa)
        file_object = open(filename6, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='meme', pass_context=True, no_pm=False)
    async def meme_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        desdata = ctx.message.content[len(self.bot.bot_prefix + 'meme'):].strip()
        meme_error = False
        desdata = str(desdata)
        toptext = None
        bottext = None
        pic = None
        msg_mention_list_len = len(ctx.message.mentions) - 1
        if msg_mention_list_len == -1:
            msg_mention_list_len = 0
        if msg_mention_list_len > 0:
            if desdata.startswith(ctx.message.mentions[msg_mention_list_len].mention):
                desdata = desdata.replace(" | ", "\n").replace('-', '--').replace(' ', '-')
                desdata = desdata.splitlines()
                try:
                    pic = ctx.message.mentions[msg_mention_list_len].avatar_url
                except IndexError:
                    meme_error = True
                    msgdata = str(self.bot.botmessages['meme_command_data'][0])
                    await self.bot.send_message(ctx.message.channel, content=msgdata)
                if not meme_error:
                    try:
                        toptext = desdata[1].replace('_', '__').replace('?', '~q').replace(
                            '%', '~p').replace('#', '~h').replace('/', '~s')
                        for x in ctx.message.mentions:
                            toptext = toptext.replace(x.mention, x.name)
                        toptext = toptext.replace('<', '').replace('>', '').replace('@', '')
                    except IndexError:
                        meme_error = True
                        msgdata = str(self.bot.botmessages['meme_command_data'][1])
                        await self.bot.send_message(ctx.message.channel, content=msgdata)
                if not meme_error:
                    try:
                        bottext = desdata[2].replace('_', '__').replace(
                            '?', '~q').replace('%', '~p').replace('#', '~h').replace('/', '~s')
                        for x in ctx.message.mentions:
                            bottext = bottext.replace(x.mention, x.name)
                        bottext = bottext.replace('<', '').replace('>', '').replace('@', '')
                    except IndexError:
                        meme_error = True
                        msgdata = str(self.bot.botmessages['meme_command_data'][2])
                        await self.bot.send_message(ctx.message.channel, content=msgdata)
                if not meme_error:
                    rep = "http://memegen.link/custom/{0}/{1}.jpg?alt={2}".format(toptext, bottext, pic)
                    await self.bot.send_message(ctx.message.channel, content=rep)
        else:
            desdata = desdata.replace(" | ", "\n").replace('-', '--').replace(' ', '-')
            desdata = desdata.splitlines()
            try:
                pic = str(desdata[0])
            except IndexError:
                meme_error = True
                msgdata = str(self.bot.botmessages['meme_command_data'][0])
                await self.bot.send_message(ctx.message.channel, content=msgdata)
            if not meme_error:
                try:
                    toptext = desdata[1].replace('_', '__').replace('?', '~q').replace(
                        '%', '~p').replace('#', '~h').replace('/', '~s')
                    for x in ctx.message.mentions:
                        toptext = toptext.replace(x.mention, x.name)
                    toptext = toptext.replace('<', '').replace('>', '').replace('@', '')
                except IndexError:
                    meme_error = True
                    msgdata = str(self.bot.botmessages['meme_command_data'][1])
                    await self.bot.send_message(ctx.message.channel, content=msgdata)
            if not meme_error:
                try:
                    bottext = desdata[2].replace('_', '__').replace('?', '~q').replace(
                        '%', '~p').replace('#', '~h').replace('/', '~s')
                    for x in ctx.message.mentions:
                        bottext = bottext.replace(x.mention, x.name)
                    bottext = bottext.replace('<', '').replace('>', '').replace('@', '')
                except IndexError:
                    meme_error = True
                    msgdata = str(self.bot.botmessages['meme_command_data'][2])
                    await self.bot.send_message(ctx.message.channel, content=msgdata)
            if not meme_error:
                rep = "http://memegen.link/{0}/{1}/{2}.jpg".format(pic, toptext, bottext)
                await self.bot.send_message(ctx.message.channel, content=rep)

    @commands.command(name='discrim', pass_context=True, no_pm=True)
    async def discrim_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        for member in self.bot.get_all_members():
            if member.discriminator == ctx.message.author.discriminator:
                if member != ctx.message.author:
                    self.member_list.append(member.name)
        if len(self.member_list) > 0:
            await self.bot.send_message(ctx.message.channel,
                                        content=(
                                            "Found {0} members with the same discriminator of {1}: ```{2}```."
                                        ).format(
                                            len(self.member_list), ctx.message.author.discriminator,
                                            self.member_list))
            self.member_list.clear()
        else:
            await self.bot.send_message(ctx.message.channel, content="Sorry, no members share your discriminator.")

    @commands.command(name='prune', pass_context=True, no_pm=True)
    async def prune_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            self.sent_prune_error_message = False
            role2 = discord.utils.find(lambda role: role.name == 'Bot Commander', ctx.message.channel.server.roles)
            """
            if ctx.message.author.id == owner_id:
                opt = ctx.message.content[len(_bot_prefix + "prune "):].strip()
                num = 1
                if opt:
                    try:
                        num = int(opt)
                    except:
                        return
                await self.prune_command_iterater_helper(ctx, num)
            else:
            """
            if role2 in ctx.message.author.roles:
                opt = ctx.message.content[len(self.bot.bot_prefix + "prune "):].strip()
                num = 1
                if opt:
                    try:
                        num = int(opt)
                    except Exception as e:
                        str(e)
                        return
                await self.prune_command_iterater_helper(ctx, num)
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['prune_command_data'][1]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='say', pass_context=True, no_pm=False)
    async def say_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            say = ctx.message.content[len(self.bot.bot_prefix + "say "):].strip()
            if say.rfind(self.bot.bot_prefix) != -1:
                message_data = str(self.bot.botmessages['say_command_data'][0]).format(ctx.message.author)
                await self.bot.send_message(ctx.message.channel, content=message_data)
            elif say.rfind("@") != -1:
                message_data = str(self.bot.botmessages['say_command_data'][1]).format(ctx.message.author)
                await self.bot.send_message(ctx.message.channel, content=message_data)
            else:
                try:
                    await self.bot.send_message(ctx.message.channel, content=say)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                except discord.errors.HTTPException:
                    return

    @commands.command(name='clear', pass_context=True, no_pm=True)
    async def clear_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            await self.clear_command_iterater_helper(ctx)

    @commands.command(name='botban', pass_context=True, no_pm=True)
    async def botban_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id == self.bot.owner_id:
            if len(ctx.message.mentions) < 1:
                try:
                    await self.bot.send_message(ctx.message.channel, content=str(
                        self.bot.botmessages['bot_ban_command_data'][2]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
            else:
                if ctx.message.mentions[0].id not in self.bot.banlist['Users']:
                    try:
                        self.bot.banlist['Users'].append(ctx.message.mentions[0].id)
                        json.dump(self.bot.banlist,
                                  open("{0}{1}resources{1}ConfigData{1}BotBanned.json".format(
                                      self.bot.path, self.bot.sepa), "w"))
                        try:
                            message_data = str(
                                self.bot.botmessages['bot_ban_command_data'][0]).format(
                                ctx.message.mentions[0])
                            await self.bot.send_message(ctx.message.channel, content=message_data)
                        except discord.errors.Forbidden:
                            await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                        except Exception as e:
                            str(e)
                            try:
                                messagedata = str(
                                    self.bot.botmessages['bot_ban_command_data'][1]).format(
                                    ctx.message.mentions[0])
                                message_data = messagedata + str(
                                    self.bot.botmessages['bot_ban_command_data'][2])
                                await self.bot.send_message(ctx.message.channel, content=message_data)
                            except discord.errors.Forbidden:
                                await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='botunban', pass_context=True, no_pm=True)
    async def botunban_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id == self.bot.owner_id:
            if len(ctx.message.mentions) < 1:
                try:
                    await self.bot.send_message(ctx.message.channel, content=str(
                        self.bot.botmessages['bot_unban_command_data'][2]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
            else:
                if ctx.message.mentions[0].id in self.bot.banlist['Users']:
                    try:
                        tobotunban = self.bot.banlist['Users']
                        tobotunban.remove(ctx.message.mentions[0].id)
                        json.dump(self.bot.banlist,
                                  open("{0}{1}resources{1}ConfigData{1}BotBanned.json".format(
                                      self.bot.path, self.bot.sepa), "w"))
                        try:
                            message_data = str(
                                self.bot.botmessages['bot_unban_command_data'][0]).format(
                                ctx.message.mentions[0])
                            await self.bot.send_message(ctx.message.channel, content=message_data)
                        except discord.errors.Forbidden:
                            await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                    except Exception as e:
                        str(e)
                        try:
                            messagedata = str(
                                self.bot.botmessages['bot_unban_command_data'][1]).format(
                                ctx.message.mentions[0])
                            message_data = messagedata + str(
                                self.bot.botmessages['bot_unban_command_data'][2])
                            await self.bot.send_message(ctx.message.channel, content=message_data)
                        except discord.errors.Forbidden:
                            await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='userinfo', pass_context=True, no_pm=True)
    async def userinfo_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            for disuser in ctx.message.mentions:
                username = disuser.name
                seenin = set(
                    [member.server.name for member in self.bot.get_all_members() if
                     member.name == username])
                seenin = str(len(seenin))
                if str(disuser.game) != 'None':
                    desuser = disuser
                    msgdata_1 = str(self.bot.botmessages['userinfo_command_data'][0]).format(desuser, seenin)
                    message_data = msgdata_1
                    data = message_data
                else:
                    desuser = disuser
                    msgdata_1 = str(self.bot.botmessages['userinfo_command_data'][0]).format(desuser, seenin)
                    message_data = msgdata_1.replace("Playing ", "")
                    data = message_data
                try:
                    await self.bot.send_message(ctx.message.channel, content=data)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
                break
            else:
                seenin = set(
                    [member.server.name for member in self.bot.get_all_members()
                     if member.name == ctx.message.author.name])
                seenin = str(len(seenin))
                if str(ctx.message.author.game) != 'None':
                    msgdata_1 = str(self.bot.botmessages['userinfo_command_data'][0]).format(
                        ctx.message.author, seenin)
                    message_data = msgdata_1
                    data = message_data
                else:
                    msgdata_1 = str(self.bot.botmessages['userinfo_command_data'][0]).format(
                        ctx.message.author, seenin)
                    message_data = msgdata_1.replace("Playing ", "")
                    data = message_data
                try:
                    await self.bot.send_message(ctx.message.channel, content=data)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    # This command has been optimized for TinyURL3 0.1.7

    @commands.command(name='tinyurl', pass_context=True, no_pm=False)
    async def tinyurl_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if self.disabletinyurl:
            return
        else:
            url = ctx.message.content[len(self.bot.bot_prefix + "tinyurl "):].strip()
            if '<' and '>' in url:
                url = url.strip('<')
                url = url.strip('>')
            try:
                self.link = TinyURL.create_one(url)
                self.tinyurlerror = False
            except TinyURL.errors.URLError:
                self.tinyurlerror = True
                try:
                    await self.bot.send_message(ctx.message.channel, content=str(
                        self.bot.botmessages['tinyurl_command_data'][2]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
            except TinyURL.errors.InvalidURL:
                self.tinyurlerror = True
                try:
                    result = str(self.bot.botmessages['tinyurl_command_data'][1])
                    await self.bot.send_message(ctx.message.channel, content=result)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)
            if not self.tinyurlerror:
                self.link = str(self.link)
                result = str(self.bot.botmessages['tinyurl_command_data'][0]).format(self.link)
                try:
                    await self.bot.send_message(ctx.message.channel, content=result)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    # Unused but too lazy to remove this.
    # Might make this more universal with per server config on these.

    @commands.command(name='giveme', pass_context=True, no_pm=True)
    async def giveme_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.channel.server and ctx.message.channel.server.id == "81812480254291968":
            desrole = ctx.message.content[len(self.bot.bot_prefix + "giveme "):].strip()
            role2 = discord.utils.find(lambda role: role.name == 'Muted', ctx.message.channel.server.roles)
            role3 = discord.utils.find(lambda role: role.name == 'Students', ctx.message.channel.server.roles)
            if 'admin' in desrole:
                if 'Muted' in ctx.message.author.roles:
                    await self.bot.add_roles(ctx.message.author, role2)
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['giveme_command_data'][0]))
                else:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['giveme_command_data'][5]))
            elif 'student' in desrole:
                if 'Students' in ctx.message.author.roles:
                    await self.bot.add_roles(ctx.message.author, role3)
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['giveme_command_data'][1]))
                else:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['giveme_command_data'][6]))
        else:
            if ctx.message.channel.server and ctx.message.channel.server.id == "127233852182626304":
                desrole = ctx.message.content[len(self.bot.bot_prefix + "giveme "):].strip()
                rolelist = ctx.message.channel.server.roles
                role2 = discord.utils.find(lambda role: role.name == '3rd Party Developer', rolelist)
                role3 = discord.utils.find(lambda role: role.name == 'Streamer', rolelist)
                if 'dev' in desrole:
                    if role2 not in ctx.message.author.roles:
                        await self.bot.add_roles(ctx.message.author, role2)
                        await self.bot.send_message(ctx.message.channel, content=str(
                            self.bot.botmessages['giveme_command_data'][2]))
                    else:
                        await self.bot.send_message(ctx.message.channel, content=str(
                            self.bot.botmessages['giveme_command_data'][7]))
                elif 'stream' in desrole:
                    if role3 not in ctx.message.author.roles:
                        await self.bot.add_roles(ctx.message.author, role3)
                        await self.bot.send_message(ctx.message.channel, content=str(
                            self.bot.botmessages['giveme_command_data'][3]))
                    else:
                        await self.bot.send_message(ctx.message.channel, content=str(
                            self.bot.botmessages['giveme_command_data'][8]))
            else:
                try:
                    await self.bot.send_message(ctx.message.channel, content=str(
                        self.bot.botmessages['giveme_command_data'][4]))
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='remove', pass_context=True, no_pm=True)
    async def remove_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.channel.server and ctx.message.channel.server.id == "127233852182626304":
            desrole = ctx.message.content[len(self.bot.bot_prefix + "remove "):].strip()
            rolelist = ctx.message.channel.server.roles
            role2 = discord.utils.find(lambda role: role.name == '3rd Party Developer', rolelist)
            role3 = discord.utils.find(lambda role: role.name == 'Streamer', rolelist)
            if 'dev' in desrole:
                if role2 in ctx.message.author.roles:
                    await self.bot.remove_roles(ctx.message.author, role2)
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['remove_command_data'][0]))
                else:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['remove_command_data'][2]))
            elif 'stream' in desrole:
                if role3 in ctx.message.author.roles:
                    await self.bot.remove_roles(ctx.message.author, role3)
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['remove_command_data'][1]))
                else:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(self.bot.botmessages['remove_command_data'][3]))
        else:
            return

    # Helpers.

    '''
    Sorry guys if you have python 3.5 or 3.6 you can uncomment this.
    This is because python 3.4 would still detect this as a SyntaxError.
    '''
    '''
    if self.PY35:
        async def prune_command_iterater_helper(self, ctx, num):
            """
            Prunes Messages.
            :param ctx: Message Context.
            :param num:
            :return: Nothing.
            """
            try:
                await self.bot.purge_from(ctx.message.channel, limit=num + 1)
            except discord.HTTPException:
                if self.sent_prune_error_message is False:
                    self.sent_prune_error_message = True
                    await self.bot.send_message(ctx.message.channel, content=str(self.bot.botmessages['prune_command_data'][0]))
                else:
                    return

        async def clear_command_iterater_helper(self, ctx):
            """
            Clears the bot's messages.
            :param ctx: Message Context.
            :return: Nothing.
            """
            try:
                await self.bot.purge_from(ctx.message.channel, limit=100,
                                          check=lambda e: e.author == ctx.message.server.me)
            except discord.HTTPException:
                return
    else:
    '''
    '''
    Indent this code as well if you want this to work only in Python 3.5+ as well.
    Although you do not have to as this Syntax is valid in 3.5+ or should be. the async def is also optional.
    '''

    async def prune_command_iterater_helper(self, ctx, num):
        """
        Prunes Messages.
        :param self:
        :param ctx: Message Context.
        :param num:
        :return: Nothing.
        """
        try:
            await self.bot.purge_from(ctx.message.channel, limit=num + 1)
        except discord.HTTPException:
            if self.sent_prune_error_message is False:
                self.sent_prune_error_message = True
                await self.bot.send_message(ctx.message.channel,
                                            content=str(self.bot.botmessages['prune_command_data'][0]))
            else:
                return

    async def clear_command_iterater_helper(self, ctx):
        """
        Clears the bot's messages.
        :param self:
        :param ctx: Message Context.
        :return: Nothing.
        """

        try:
            await self.bot.purge_from(ctx.message.channel, limit=100,
                                      check=lambda e: e.author == ctx.message.server.me)
        except discord.HTTPException:
            return


def setup(bot):
    """
    Normal commands.
    """
    bot.add_cog(BotCommands(bot))
