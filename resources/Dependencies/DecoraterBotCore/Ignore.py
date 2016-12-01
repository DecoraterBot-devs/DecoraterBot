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
import io
import json
import traceback
import discord
try:
    from . import BotPMError
except ImportError:
    print('Some Unknown thing happened which made a critical bot code file unable to be found.')
    BotPMError = None
from sasync import *

"""
    Since Commands Extension Rewrite was started this module may or may not have a purpouse anymore.

    Why?

    Because most (if not all) the data in this module could probably move to Core.py.
"""


class BotIgnores:
    """
    Bot Ignores Class.
    """
    def __init__(self, bot):
        self.bot = bot

    @async
    def ignore(self, message):
        """
        Listens for all Bot Commands.
        :param message: Message.
        :return: Nothing.
        """
        if message.channel.id not in self.bot.ignoreslist['channels']:
            try:
                if message.channel.is_private is not False:
                    yield from self.pm_commands(self.bot, message)
                elif message.channel.server and message.channel.server.id == "81812480254291968":
                    if message.author.id == self.bot.user.id:
                        return
                    elif message.channel.id == "153055192873566208":
                        yield from self.enable_all_commands(message)
                    elif message.channel.id == "87382611688689664":
                        yield from self.enable_all_commands(message)
                    else:
                        yield from self.enable_all_commands_with_send_logs(message)
                elif message.channel.server and message.channel.server.id == "71324306319093760":
                    if message.channel.id == '141489876200718336':
                        yield from self.cheesy_commands(message)
                    else:
                        # yield from self.everyone_mention_logger(message)
                        yield from self.enable_all_commands_with_logs(message)
                else:
                    yield from self.enable_all_commands_with_logs(message)
            except Exception as e:
                if self.bot.pm_command_errors:
                    if self.bot.discord_user_id is not None:
                        owner = self.bot.discord_user_id
                        exception_data2 = str(traceback.format_exc())
                        message_data = '```py\n{0}\n```'.format(exception_data2)
                        try:
                            yield from self.bot.send_message(discord.User(id=owner), content=message_data)
                        except discord.errors.Forbidden:
                            return
                        except discord.errors.HTTPException:
                            funcname = 'ignore'
                            tbinfo = str(traceback.format_exc())
                            yield from self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)
                    else:
                        return
                else:
                    funcname = 'ignore'
                    tbinfo = str(traceback.format_exc())
                    yield from self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)
        else:
            yield from self.ignored_channel_commands(message)

    @async
    def ignore_channel(self, message):
        """
        Makes the bot Ignore or not Ignore channels.
        :param message: Message.
        :return: Nothing.
        """
        if message.content.startswith(self.bot.bot_prefix + 'ignorechannel'):
            if message.channel.id not in self.bot.ignoreslist["channels"]:
                try:
                    self.bot.ignoreslist["channels"].append(message.channel.id)
                    json.dump(self.bot.ignoreslist, open("{0}{1}resources{1}ConfigData{1}IgnoreList.json".format(
                        self.bot.path, self.bot.sepa), "w"))
                    try:
                        yield from self.bot.send_message(message.channel,
                                                         content=str(self.bot.botmessages['Ignore_Channel_Data'][0]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error_old(self.bot, message)
                except Exception as e:
                    str(e)
                    try:
                        yield from self.bot.send_message(message.channel,
                                                         content=str(self.bot.botmessages['Ignore_Channel_Data'][1]))
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error_old(self.bot, message)
        if message.content.startswith(self.bot.bot_prefix + 'unignorechannel'):
            if message.channel.id in self.bot.ignoreslist["channels"]:
                try:
                    ignored = self.bot.ignoreslist["channels"]
                    ignored.remove(message.channel.id)
                    json.dump(self.bot.ignoreslist, open("{0}{1}resources{1}ConfigData{1}IgnoreList.json".format(
                        self.bot.path, self.bot.sepa), "w"))
                    msg_info = str(self.bot.botmessages['Unignore_Channel_Data'][0])
                    try:
                        yield from self.bot.send_message(message.channel, content=msg_info)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error_old(self.bot, message)
                except Exception as e:
                    str(e)
                    msg_info = str(self.bot.botmessages['Unignore_Channel_Data'][1])
                    try:
                        yield from self.bot.send_message(message.channel, content=msg_info)
                    except discord.errors.Forbidden:
                        yield from BotPMError.resolve_send_message_error_old(self.bot, message)

    @async
    def ignored_channel_commands(self, message):
        """
        Listens for the Commands that can be done in muted Channels.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.ignore_channel(message)
        yield from self.reload_command(message)

    @async
    def enable_all_commands(self, message):
        """
        Listens for all Bot Commands.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.DBCommands.prune(self.bot, message)
        yield from self.DBCommands.invite(self.bot, message)
        yield from self.DBCommands.kills(self.bot, message)
        yield from self.DBCommands.colors(self.bot, message)
        yield from self.DBCommands.games(self.bot, message)
        yield from self.DBCommands.attack(self.bot, message)
        yield from self.DBCommands.debug(self.bot, message)
        yield from self.DBCommands.other_commands(self.bot, message)
        yield from self.DBCommands.userdata(self.bot, message)
        yield from self.DBCommands.bot_say(self.bot, message)
        yield from self.DBCommands.randomcoin(self.bot, message)
        yield from self.DBCommands.mod_commands(self.bot, message)
        yield from self.DBCommands.bot_roles(self.bot, message)
        yield from self.DBCommands.more_commands(self.bot, message)
        yield from self.DBCommands.convert_url(self.bot, message)
        if not self.bot.disable_voice_commands:
            # Add the Voice Commands cog.
            yield from self.DBVoiceCommands.voice_stuff_new(self.bot, message)
        else:
            # In this case lets define a bool global to this class only to tell this to generate a
            # disabled version of the voice commands.
            self.bot._disable_voice_commands = True
            yield from self.DBVoiceCommands.voice_stuff_new_disabled(self.bot, message)
        yield from self.ignored_channel_commands(self.bot, message)

    @async
    def enable_all_commands_with_send_logs(self, message):
        """
        Listens for all Bot Commands.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.enable_all_commands(message)
        if self.bot.logging:
            yield from self.bot.DBLogs.send_logs(self.bot, message)

    @async
    def enable_all_commands_with_logs(self, message):
        """
        Listens for all Bot Commands.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.enable_all_commands(message)
        if self.bot.logging:
            self.bot.DBLogs.logs(message)

    @async
    def pm_commands(self, message):
        """
        Listens for all Bot Commands.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.DBCommands.scan_for_invite_url_only_pm(self.bot, message)
        yield from self.DBCommands.invite(self.bot, message)
        yield from self.DBCommands.kills(self.bot, message)
        yield from self.DBCommands.games(self.bot, message)
        yield from self.DBCommands.other_commands(self.bot, message)
        yield from self.DBCommands.bot_say(self.bot, message)
        yield from self.DBCommands.randomcoin(self.bot, message)
        yield from self.DBCommands.convert_url(self.bot, message)
        if self.bot.logging:
            self.bot.DBLogs.logs(message)

    @async
    def cheesy_commands(self, message):
        """
        Listens fCheese.lab Specific Server commands.
        :param message: Message.
        :return: Nothing.
        """
        yield from self.enable_all_commands_with_logs(self.bot, message)
        serveridslistfile = io.open('{0}{1}resources{1}ConfigData{1}serverconfigs{1}servers.json'.format(self.bot.path,
                                                                                                         self.bot.sepa))
        serveridslist = json.load(serveridslistfile)
        serveridslistfile.close()
        serverid = str(serveridslist['config_server_ids'][0])
        file_path = ('{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}verifications{0}'.format(
            self.bot.sepa, serverid))
        filename_1 = 'verifycache.json'
        filename_2 = 'verifycommand.json'
        filename_3 = 'verifyrole.json'
        filename_4 = 'verifymessages.json'
        filename_5 = 'verifycache.json'
        joinedlistfile = io.open(self.bot.path + file_path + filename_1)
        newlyjoinedlist = json.load(joinedlistfile)
        joinedlistfile.close()
        memberjoinverifymessagefile = io.open(self.bot.path + file_path + filename_2)
        memberjoinverifymessagedata = json.load(memberjoinverifymessagefile)
        memberjoinverifymessagefile.close()
        memberjoinverifyrolefile = io.open(self.bot.path + file_path + filename_3)
        memberjoinverifyroledata = json.load(memberjoinverifyrolefile)
        memberjoinverifyrolefile.close()
        memberjoinverifymessagefile2 = io.open(self.bot.path + file_path + filename_4)
        memberjoinverifymessagedata2 = json.load(memberjoinverifymessagefile2)
        memberjoinverifymessagefile2.close()
        role_name = str(memberjoinverifyroledata['verify_role_id'][0])
        msg_command = str(memberjoinverifymessagedata['verify_command'][0])
        try:
            if '>' or '<' or '`' in message.content:
                msgdata = message.content.replace('<', '').replace('>', '').replace('`', '')
            else:
                msgdata = message.content
            if msg_command == msgdata:
                if message.author.id in newlyjoinedlist['users_to_be_verified']:
                    yield from self.bot.delete_message(message)
                    role2 = discord.utils.find(lambda role: role.id == role_name, message.channel.server.roles)
                    msg_data = str(memberjoinverifymessagedata2['verify_messages'][1]).format(message.server.name)
                    yield from self.bot.add_roles(message.author, role2)
                    yield from self.bot.send_message(message.author, content=msg_data)
                    newlyjoinedlist['users_to_be_verified'].remove(message.author.id)
                    json.dump(newlyjoinedlist, open(self.bot.path + file_path + filename_5, "w"))
                else:
                    yield from self.bot.delete_message(message)
                    yield from self.bot.send_message(message.channel, content=str(
                        memberjoinverifymessagedata2['verify_messages'][2]))
            else:
                if message.author.id != self.bot.user.id:
                    if message.author.id in newlyjoinedlist['users_to_be_verified']:
                        yield from self.bot.delete_message(message)
                        yield from self.bot.send_message(message.channel, content=str(
                            memberjoinverifymessagedata2['verify_messages'][3]).format(message.author.mention))
        except NameError:
            yield from self.bot.send_message(message.channel, content=str(
                memberjoinverifymessagedata2['verify_messages'][4]).format(message.author.mention))
