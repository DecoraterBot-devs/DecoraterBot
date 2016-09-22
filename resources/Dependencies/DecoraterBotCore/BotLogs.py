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
import os
import discord
import io
import sys
import os.path
import asyncio
import logging
import json
import ctypes


class BotData:
    """
        This class is for Internal use only!!!
    """
    def __init__(self):
        self.sepa = os.sep
        self.bits = ctypes.sizeof(ctypes.c_voidp)
        self.platform = None
        if self.bits == 4:
            self.platform = 'x86'
        elif self.bits == 8:
            self.platform = 'x64'
        self.path = sys.path[0]
        if self.path.find('\\AppData\\Local\\Temp') != -1:
            self.path = sys.executable.strip(
                'DecoraterBot.{0}.{1}.{2.name}-{3.major}{3.minor}{3.micro}.exe'.format(self.platform, sys.platform,
                                                                                       sys.implementation,
                                                                                       sys.version_info))

        try:
            self.consoledatafile = io.open('{0}{1}resources{1}ConfigData{1}ConsoleWindow.json'.format(self.path,
                                                                                                      self.sepa))
            self.consoletext = json.load(self.consoledatafile)
            self.consoledatafile.close()
        except FileNotFoundError:
            print('ConsoleWindow.json is not Found. Cannot Continue.')
            sys.exit(2)
        try:
            self.LogDataFile = io.open('{0}{1}resources{1}ConfigData{1}LogData.json'.format(self.path, self.sepa))
            self.LogData = json.load(self.LogDataFile)
            self.LogDataFile.close()
        except FileNotFoundError:
            print(str(self.consoletext['Missing_JSON_Errors'][2]))
            sys.exit(2)

    def set_up_loggers(self, loggers=None):
        """
        Logs Events from discord and/or asyncio stuff.
        :param loggers: Name of the logger(s) to use.
        :return: Nothing.
        """
        if loggers is not None:
            if loggers == 'discord':
                logger = logging.getLogger('discord')
                logger.setLevel(logging.DEBUG)
                handler = logging.FileHandler(filename='{0}{1}resources{1}Logs{1}discordpy.log'.format(self.path,
                                                                                                       self.sepa),
                                              encoding='utf-8', mode='w')
                handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
                logger.addHandler(handler)
            elif loggers == 'asyncio':
                asynciologger = logging.getLogger('asyncio')
                asynciologger.setLevel(logging.DEBUG)
                asynciologgerhandler = logging.FileHandler(filename='{0}{1}resources{1}Logs{1}asyncio.log'.format(
                    self.path, self.sepa), encoding='utf-8', mode='w')
                asynciologgerhandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
                asynciologger.addHandler(asynciologgerhandler)

    def logs_code(self, message):
        """
            :param message: Message Object
        """
        logs001 = str(self.LogData['On_Message_Logs'][0]).format(message.author.name, message.author.id,
                                                                 str(message.timestamp), message.content)
        logspm = logs001
        logsservers = None
        if message.channel.is_private is False:
            logs003 = str(self.LogData['On_Message_Logs'][1]).format(message.author.name, message.author.id,
                                                                     str(message.timestamp),
                                                                     message.channel.server.name,
                                                                     message.channel.name, message.content)
            logsservers = logs003
        if message.content is not None:
            logfile = '{0}{1}resources{1}Logs{1}log.txt'.format(self.path, self.sepa)
            try:
                file = io.open(logfile, 'a', encoding='utf-8')
                size = os.path.getsize(logfile)
                if size >= 32102400:
                    file.seek(0)
                    file.truncate()
                if message.channel.is_private is True:
                    file.write(logspm)
                else:
                    file.write(logsservers)
                file.close()
            except PermissionError:
                return

    def edit_logs_code(self, before, after):
        """
        Logs Edited messages.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        old = str(before.content)
        new = str(after.content)
        logfile = '{0}{1}resources{1}Logs{1}edit log.txt'.format(self.path, self.sepa)
        usr_name = before.author.name
        usr_id = before.author.id
        msg_time = str(before.timestamp)
        editlog001 = str(self.LogData['On_Message_Logs'][0]).format(usr_name, usr_id, msg_time, old, new)
        edit_log_pm = editlog001
        editlogservers = None
        if before.channel.is_private is False:
            svr_name = before.channel.server.name
            chl_name = before.channel.name
            editlog003 = str(self.LogData['On_Message_Logs'][1]).format(usr_name, usr_id, msg_time, svr_name,
                                                                        chl_name, old, new)
            editlogservers = editlog003
        try:
            file = io.open(logfile, 'a', encoding='utf-8')
            size = os.path.getsize(logfile)
            if size >= 32102400:
                file.seek(0)
                file.truncate()
                try:
                    if before.content == after.content:
                        self.resolve_embed_logs_code(before)
                    else:
                        try:
                            file.write(editlogservers)
                        except PermissionError:
                            return
                        file.close()
                except Exception as e:
                    str(e)  # Empty string that is not used nor assigned to a variable. (for now)
                    if before.channel.is_private is False:
                        print(str(self.LogData['On_Edit_Logs_Error'][0]))
                    else:
                        if before.content == after.content:
                            self.resolve_embed_logs_code(before)
                        else:
                            file.write(edit_log_pm)
                        file.close()
        except PermissionError:
            return

    def delete_logs_code(self, message):
        """
        Logs Deleted Messages.
        :param message: Messages.
        :return: Nothing.
        """
        dellogs001 = str(self.LogData['On_Message_Logs'][0]).format(message.author.name, message.author.id,
                                                                    str(message.timestamp), message.content)
        dellogspm = dellogs001
        dellogsservers = None
        if message.channel.is_private is False:
            dellogs003 = str(self.LogData['On_Message_Logs'][1]).format(message.author.name, message.author.id,
                                                                        str(message.timestamp),
                                                                        message.channel.server.name,
                                                                        message.channel.name, message.content)
            dellogsservers = dellogs003
        if message.content is not None:
            try:
                logfile = '{0}{1}resources{1}Logs{1}delete log.txt'.format(self.path, self.sepa)
                file = io.open(logfile, 'a', encoding='utf-8')
                size = os.path.getsize(logfile)
                if size >= 32102400:
                    file.seek(0)
                    file.truncate()
                if message.channel.is_private is True:
                    file.write(dellogspm)
                else:
                    file.write(dellogsservers)
                file.close()
            except PermissionError:
                return

    def resolve_embed_logs_code(self, before):
        """
        helps with determining if the messages was edited or a embed instead.
        :param before: Messages.
        :return: Nothing.
        """
        if before.channel.is_private is True:
            data = str(self.LogData['Embed_Logs'][0])
        else:
            data = str(self.LogData['Embed_Logs'][1])
        logfile = '{0}{1}resources{1}Logs{1}embeds.txt'.format(self.path, self.sepa)
        try:
            file2 = io.open(logfile, 'a', encoding='utf-8')
            size = os.path.getsize(logfile)
            if size >= 32102400:
                file2.seek(0)
                file2.truncate()
            file2.write(data + "\n")
        except PermissionError:
            return

    @asyncio.coroutine
    def send_logs_code(self, client, message):
        """
        Sends Sent Lessages.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        logs001 = str(self.LogData['Send_On_Message_Logs'][0]).format(message.author.name, message.author.id,
                                                                      str(message.timestamp),
                                                                      message.channel.server.name, message.channel.name,
                                                                      message.content)
        sndmsglogs = logs001
        try:
            yield from client.send_message(discord.Object(id='153055192873566208'), sndmsglogs)
        except discord.errors.NotFound:
            return
        except discord.errors.HTTPException:
            return

    @asyncio.coroutine
    def send_edit_logs_code(self, client, before, after):
        """
        Sends Edited Messages.
        :param client: Discord Client.
        :param before: Messages.
        :param after: Messages.
        :return: Nothing.
        """
        old = str(before.content)
        new = str(after.content)
        editlog001 = str(self.LogData['Send_On_Message_Edit_Logs'][0]).format(before.author.name, before.author.id,
                                                                              str(before.timestamp),
                                                                              before.channel.server.name,
                                                                              before.channel.name, old, new)
        sendeditlogs = editlog001
        if before.content != after.content:
            try:
                yield from client.send_message(discord.Object(id='153055192873566208'), sendeditlogs)
            except discord.errors.NotFound:
                return
            except discord.errors.HTTPException:
                return

    @asyncio.coroutine
    def send_delete_logs_code(self, client, message):
        """

        :rtype: None
        """
        dellogs001 = str(self.LogData['Send_On_Message_Delete_Logs'][0]).format(message.author.name, message.author.id,
                                                                                str(message.timestamp),
                                                                                message.channel.server.name,
                                                                                message.channel.name, message.content)
        senddeletelogs = dellogs001
        try:
            yield from client.send_message(discord.Object(id='153055192873566208'), senddeletelogs)
        except discord.errors.NotFound:
            return
        except discord.errors.HTTPException:
            return

    @asyncio.coroutine
    def on_bot_error_code(self, funcname, tbinfo, err):
        """
        Handles Event Bot Errors
        :param funcname: Function names that Had a .
        :param tbinfo: Original Traceback.
        :param err: RAW traceback Error Data.
        :return: Nothing.
        """
        if bool(funcname):
            if bool(tbinfo):
                exception_data = 'Ignoring exception caused at {0}:\n{1}'.format(funcname, tbinfo)
                logfile = '{0}{1}resources{1}Logs{1}error_log.txt'.format(self.path, self.sepa)
                try:
                    file = io.open(logfile, 'a', encoding='utf-8')
                    size = os.path.getsize(logfile)
                    if size >= 32102400:
                        file.seek(0)
                        file.truncate()
                    file.write(exception_data)
                    file.close()
                except PermissionError:
                    return
            else:
                raise err
        else:
            raise err

    def gamelog_code(self, message, desgame):
        """
        Logs the bot's game settings.
        :param message: Messages.
        :param desgame: Game Name.
        :return: Nothing.
        """
        gmelogdata01 = str(self.LogData['On_Message_Logs'][0]).format(message.author.name, desgame, message.author.id)
        gmelogspm = gmelogdata01
        if message.channel.is_private is False:
            gmelog001 = str(self.LogData['On_Message_Logs'][1]).format(message.author.name, desgame, message.author.id)
            gmelogsservers = gmelog001
            logfile = '{0}{1}resources{1}Logs{1}gamelog.txt'.format(self.path, self.sepa)
            try:
                file = io.open(logfile, 'a', encoding='utf-8')
                size = os.path.getsize(logfile)
                if size >= 32102400:
                    file.seek(0)
                    file.truncate()
                if message.channel.is_private is True:
                    file.write(gmelogspm)
                else:
                    file.write(gmelogsservers)
                file.close()
            except PermissionError:
                return

    @asyncio.coroutine
    def onban_code(self, member):
        """
        Logs Bans.
        :param member: Members.
        :return: Nothing.
        """
        mem_name = member.name
        mem_id = member.id
        mem_dis = member.discriminator
        mem_svr_name = member.server.name
        ban_log_data = str(self.LogData['Ban_Logs'][0]).format(mem_name, mem_id, mem_dis, mem_svr_name)
        logfile = '{0}{1}resources{1}Logs{1}bans.txt'.format(self.path, self.sepa)
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(ban_log_data)
        file.close()

    @asyncio.coroutine
    def onavailable_code(self, server):
        """
        Logs available Servers.
        :param server: Servers.
        :return: Nothing.
        """
        available_log_data = str(self.LogData['On_Server_Available'][0]).format(server)
        logfile = '{0}{1}resources{1}Logs{1}available_servers.txt'.format(self.path, self.sepa)
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(available_log_data)
        file.close()

    @asyncio.coroutine
    def onunavailable_code(self, server):
        """
        Logs Unavailable Servers.
        :param server: Servers.
        :return: Nothing.
        """
        unavailable_log_data = str(self.LogData['On_Server_Unavailable'][0]).format(server)
        logfile = '{0}{1}resources{1}Logs{1}unavailable_servers.txt'.format(self.path, self.sepa)
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(unavailable_log_data)
        file.close()

    @asyncio.coroutine
    def onunban_code(self, server, user):
        """
        Logs Unbans.
        :param server: Server.
        :param user: Users.
        :return: Nothing.
        """
        unban_log_data = str(self.LogData['Unban_Logs'][0]).format(user.name, user.id, user.discriminator,
                                                                   server.name)
        logfile = '{0}{1}resources{1}Logs{1}unbans.txt'.format(self.path, self.sepa)
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(unban_log_data)
        file.close()

    @asyncio.coroutine
    def ongroupjoin_code(self, channel, user):
        """
        logs group join.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @asyncio.coroutine
    def ongroupremove_code(self, channel, user):
        """
        Removed from group.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        # TODO: Impliment this.
        pass

    @asyncio.coroutine
    def onkick_code(self, member):
        """

        :rtype: None
        """
        mem_name = member.name
        mem_id = member.id
        mem_dis = member.discriminator
        mem_svr_name = member.server.name
        kick_log_data = str(self.LogData['Kick_Logs'][0]).format(mem_name, mem_id, mem_dis, mem_svr_name)
        logfile = '{0}{1}resources{1}Logs{1}kicks.txt'.format(self.path, self.sepa)
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(kick_log_data)
        file.close()


class BotLogs:
    """
    Main Bot logging Class.
    """
    def __init__(self):
        self.bot = BotData()

    def set_up_discord_logger(self):
        """
        Sets up the Discord Logger.
        :return: Nothing.
        """
        self.bot.set_up_loggers(loggers='discord')

    def set_up_asyncio_logger(self):
        """
        Sets up the asyncio Logger.
        :return: Nothing.
        """
        self.bot.set_up_loggers(loggers='asyncio')

    def logs(self, message):
        """
        Logs Sent Messages.
        :param message: Messages.
        :return: Nothing.
        """
        self.bot.logs_code(message)

    def edit_logs(self, before, after):
        """
        Logs Edited Messages.
        :param before: Messages.
        :param after: Messages.
        :return: Nothing.
        """
        self.bot.edit_logs_code(before, after)

    def delete_logs(self, message):
        """
        Logs Deleted Messages.
        :param message: Messages.
        :return: Nothing.
        """
        self.bot.delete_logs_code(message)

    def resolve_embed_logs(self, before):
        """
        Resolves if the message was edited or not.
        :param before: Messages.
        :return: Nothing.
        """
        self.bot.resolve_embed_logs_code(before)

    @asyncio.coroutine
    def send_logs(self, client, message):
        """
        Sends Sent Messages.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.send_logs_code(client, message)

    @asyncio.coroutine
    def send_edit_logs(self, client, before, after):
        """
        Sends Edited Messages.
        :param client: Discord Client.
        :param before: Messages.
        :param after: Messages.
        :return: Nothing.
        """
        yield from self.bot.send_edit_logs_code(client, before, after)

    @asyncio.coroutine
    def send_delete_logs(self, client, message):
        """
        Sends Deleted Messages.
        :param client: Discord Client.
        :param message: Messages.
        :return: Nothing.
        """
        yield from self.bot.send_delete_logs_code(client, message)

    @asyncio.coroutine
    def on_bot_error(self, funcname, tbinfo, err):
        """
            This Function is for Internal Bot use only.
            It is for catching any Errors and writing them to a file.

            Usage
            =====
            :param funcname: Must be a string with the name of the function that caused a Error.
                raises the Errors that happened if empty string or None is given.
            :param tbinfo: string data of the traceback info. Must be a string for this to not Error itself.
                raises the Errors that happened if empty string or None is given.
            :param err: Error Data from Traceback. (RAW)
        """
        yield from self.bot.on_bot_error_code(funcname, tbinfo, err)

    def gamelog(self, message, desgame):
        """
        Logs Game Names.
        :param message: Messages.
        :param desgame: Game Name.
        :return: Nothing.
        """
        self.bot.gamelog_code(message, desgame)

    @asyncio.coroutine
    def onban(self, member):
        """
        Logs Bans.
        :param member: Members.
        :return: Nothing.
        """
        yield from self.bot.onban_code(member)

    @asyncio.coroutine
    def onavailable(self, server):
        """
        Logs Available Servers.
        :param server:
        :return: Nothing.
        """
        yield from self.bot.onavailable_code(server)

    @asyncio.coroutine
    def onunavailable(self, server):
        """
        Logs Unavailable Servers
        :param server: Servers.
        :return: Nothing.
        """
        yield from self.bot.onunavailable_code(server)

    @asyncio.coroutine
    def onunban(self, server, user):
        """
        Logs Unbans.
        :param server: Server.
        :param user: Users.
        :return: Nothing.
        """
        yield from self.bot.onunban_code(server, user)

    @asyncio.coroutine
    def ongroupjoin(self, channel, user):
        """
        Logs group join.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from self.bot.ongroupjoin_code(channel, user)

    @asyncio.coroutine
    def ongroupremove(self, channel, user):
        """
        Logs group remove.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        yield from self.bot.ongroupremove_code(channel, user)

    @asyncio.coroutine
    def onkick(self, member):
        """
        Logs Kicks.
        :param member: Members.
        :return: Nothing.
        """
        yield from self.bot.onkick_code(member)
