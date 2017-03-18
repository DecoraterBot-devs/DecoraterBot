# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import os
import sys
import logging
import json

import discord

__all__ = ['BotLogger']


class BotLogger:
    """
    Main Bot logging Class.
    """
    def __init__(self, bot):
        self.sepa = os.sep
        self.bot = bot
        self.path = sys.path[0]
        self.BotConfig = self.bot.BotConfig

        try:
            self.consoledatafile = open('{0}{1}resources{1}ConfigData'
                                        '{1}ConsoleWindow.{2}.'
                                        'json'.format(self.path, self.sepa,
                                                      self.BotConfig.language))
            self.consoletext = json.load(self.consoledatafile)
            self.consoledatafile.close()
        except FileNotFoundError:
            print('ConsoleWindow.{0}.json is not Found. '
                  'Cannot Continue.'.format(self.BotConfig.language))
            sys.exit(2)
        try:
            self.LogDataFile = open('{0}{1}resources{1}'
                                    'ConfigData{1}LogData.{2}.'
                                    'json'.format(self.path, self.sepa,
                                                  self.BotConfig.language))
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
                handler = logging.FileHandler(
                    filename='{0}{1}resources{1}Logs{1}discordpy.log'.format(
                        self.path, self.sepa), encoding='utf-8', mode='w')
                handler.setFormatter(logging.Formatter(
                    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
                logger.addHandler(handler)
            elif loggers == 'asyncio' and self.bot is not None:
                self.bot.loop.set_debug(True)
                asynciologger = logging.getLogger('asyncio')
                asynciologger.setLevel(logging.DEBUG)
                asynciologgerhandler = logging.FileHandler(
                    filename='{0}{1}resources{1}Logs{1}asyncio.log'.format(
                        self.path, self.sepa), encoding='utf-8', mode='w')
                asynciologgerhandler.setFormatter(logging.Formatter(
                    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
                asynciologger.addHandler(asynciologgerhandler)

    def set_up_discord_logger(self):
        """
        Sets up the Discord Logger.
        :return: Nothing.
        """
        self.set_up_loggers(loggers='discord')

    def set_up_asyncio_logger(self):
        """
        Sets up the asyncio Logger.
        :return: Nothing.
        """
        self.set_up_loggers(loggers='asyncio')

    def logs(self, message):
        """
        Logs Sent Messages.
        :param message: Messages.
        :return: Nothing.
        """
        logs001 = str(self.LogData['On_Message_Logs'][0]).format(
            message.author.name, message.author.id, str(
                message.timestamp), message.content)
        logspm = logs001
        logsservers = None
        if message.channel.is_private is False:
            logs003 = str(self.LogData['On_Message_Logs'][1]).format(
                message.author.name, message.author.id, str(
                    message.timestamp), message.channel.server.name,
                message.channel.name, message.content)
            logsservers = logs003
        if message.content is not None:
            logfile = '{0}{1}resources{1}Logs{1}log.log'.format(
                self.path, self.sepa)
            try:
                file = open(logfile, 'a', encoding='utf-8')
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

    def edit_logs(self, before, after):
        """
        Logs Edited Messages.
        :param before: Messages.
        :param after: Messages.
        :return: Nothing.
        """
        old = str(before.content)
        new = str(after.content)
        logfile = '{0}{1}resources{1}Logs{1}edit_log.log'.format(self.path,
                                                                 self.sepa)
        usr_name = before.author.name
        usr_id = before.author.id
        msg_time = str(before.timestamp)
        editlog001 = str(self.LogData['On_Message_Logs'][0]).format(usr_name,
                                                                    usr_id,
                                                                    msg_time,
                                                                    old, new)
        edit_log_pm = editlog001
        editlogservers = None
        if before.channel.is_private is False:
            svr_name = before.channel.server.name
            chl_name = before.channel.name
            editlog003 = str(self.LogData['On_Message_Logs'][1]).format(
                usr_name, usr_id, msg_time, svr_name,
                chl_name, old, new)
            editlogservers = editlog003
        try:
            file = open(logfile, 'a', encoding='utf-8')
            size = os.path.getsize(logfile)
            if size >= 32102400:
                file.seek(0)
                file.truncate()
                try:
                    if before.content == after.content:
                        self.resolve_embed_logs(before)
                    else:
                        try:
                            file.write(editlogservers)
                        except PermissionError:
                            return
                        file.close()
                except Exception as e:
                    # Empty string that is not used nor assigned
                    # to a variable. (for now)
                    str(e)
                    if before.channel.is_private is False:
                        print(str(self.LogData['On_Edit_Logs_Error'][0]))
                    else:
                        if before.content == after.content:
                            self.resolve_embed_logs(before)
                        else:
                            file.write(edit_log_pm)
                        file.close()
        except PermissionError:
            return

    def delete_logs(self, message):
        """
        Logs Deleted Messages.
        :param message: Messages.
        :return: Nothing.
        """
        dellogs001 = str(self.LogData['On_Message_Logs'][0]).format(
            message.author.name, message.author.id,
            str(message.timestamp), message.content)
        dellogspm = dellogs001
        dellogsservers = None
        if message.channel.is_private is False:
            dellogs003 = str(self.LogData['On_Message_Logs'][1]).format(
                message.author.name, message.author.id,
                str(message.timestamp),
                message.channel.server.name,
                message.channel.name, message.content)
            dellogsservers = dellogs003
        if message.content is not None:
            try:
                logfile = '{0}{1}resources{1}Logs{1}delete_log.log'.format(
                    self.path, self.sepa)
                file = open(logfile, 'a', encoding='utf-8')
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

    def resolve_embed_logs(self, before):
        """
        Resolves if the message was edited or not.
        :param before: Messages.
        :return: Nothing.
        """
        if before.channel.is_private is True:
            data = str(self.LogData['Embed_Logs'][0])
        else:
            data = str(self.LogData['Embed_Logs'][1])
        logfile = '{0}{1}resources{1}Logs{1}embeds.log'.format(self.path,
                                                               self.sepa)
        try:
            file2 = open(logfile, 'a', encoding='utf-8')
            size = os.path.getsize(logfile)
            if size >= 32102400:
                file2.seek(0)
                file2.truncate()
            file2.write(data + "\n")
        except PermissionError:
            return

    async def send_logs(self, message):
        """
        Sends Sent Messages.
        :param message: Messages.
        :return: Nothing.
        """
        logs001 = str(self.LogData['Send_On_Message_Logs'][0]).format(
            message.author.name, message.author.id,
            str(message.timestamp),
            message.channel.server.name, message.channel.name,
            message.content)
        sndmsglogs = logs001
        try:
            await self.bot.send_message(
                discord.Object(id='153055192873566208'), content=sndmsglogs)
        except discord.errors.NotFound:
            return
        except discord.errors.HTTPException:
            return

    async def send_edit_logs(self, before, after):
        """
        Sends Edited Messages.
        :param before: Messages.
        :param after: Messages.
        :return: Nothing.
        """
        old = str(before.content)
        new = str(after.content)
        editlog001 = str(self.LogData['Send_On_Message_Edit_Logs'][0]).format(
            before.author.name, before.author.id,
            str(before.timestamp),
            before.channel.server.name,
            before.channel.name, old, new)
        sendeditlogs = editlog001
        if before.content != after.content:
            try:
                await self.bot.send_message(
                    discord.Object(id='153055192873566208'),
                    content=sendeditlogs)
            except discord.errors.NotFound:
                return
            except discord.errors.HTTPException:
                return

    async def send_delete_logs(self, message):
        """
        Sends Deleted Messages.
        :param message: Messages.
        :return: Nothing.
        """
        dellogs001 = str(
            self.LogData['Send_On_Message_Delete_Logs'][0]).format(
            message.author.name, message.author.id,
            str(message.timestamp),
            message.channel.server.name,
            message.channel.name, message.content)
        senddeletelogs = dellogs001
        try:
            await self.bot.send_message(
                discord.Object(id='153055192873566208'),
                content=senddeletelogs)
        except discord.errors.NotFound:
            return
        except discord.errors.HTTPException:
            return

    def on_bot_error(self, funcname, tbinfo, err):
        """
            This Function is for Internal Bot use only.
            It is for catching any Errors and writing them to a file.

            Usage
            =====
            :param funcname: Must be a string with the name of the function
            that caused a Error.
                raises the Errors that happened if empty string or None is
                given.
            :param tbinfo: string data of the traceback info. Must be a
                string for this to not Error itself.
                raises the Errors that happened if empty string or None is
                given.
            :param err: Error Data from Traceback. (RAW)
        """
        if bool(funcname):
            if bool(tbinfo):
                exception_data = 'Ignoring exception caused at {0}:\n' \
                                 '{1}'.format(funcname, tbinfo)
                logfile = '{0}{1}resources{1}Logs{1}error_log.log'.format(
                    self.path, self.sepa)
                try:
                    file = open(logfile, 'a', encoding='utf-8')
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

    def gamelog(self, ctx, desgame):
        """
        Logs Game Names.
        :param ctx: Message Context.
        :param desgame: Game Name.
        :return: Nothing.
        """
        gmelogdata01 = str(self.LogData['Game_Logs'][0]).format(
            ctx.message.author.name, desgame,
            ctx.message.author.id)
        gmelogspm = gmelogdata01
        gmelogsservers = ""
        if ctx.message.channel.is_private is False:
            gmelog001 = str(self.LogData['Game_Logs'][1]).format(
                ctx.message.author.name, desgame,
                ctx.message.author.id)
            gmelogsservers = gmelog001
        logfile = '{0}{1}resources{1}Logs{1}gamelog.log'.format(self.path,
                                                                self.sepa)
        try:
            file = open(logfile, 'a', encoding='utf-8')
            size = os.path.getsize(logfile)
            if size >= 32102400:
                file.seek(0)
                file.truncate()
            if ctx.message.channel.is_private is True:
                file.write(gmelogspm)
            else:
                file.write(gmelogsservers)
            file.close()
        except PermissionError:
            return

    def onban(self, member):
        """
        Logs Bans.
        :param member: Members.
        :return: Nothing.
        """
        mem_name = member.name
        mem_id = member.id
        mem_dis = member.discriminator
        mem_svr_name = member.server.name
        ban_log_data = str(self.LogData['Ban_Logs'][0]).format(mem_name,
                                                               mem_id, mem_dis,
                                                               mem_svr_name)
        logfile = '{0}{1}resources{1}Logs{1}bans.log'.format(self.path,
                                                             self.sepa)
        file = open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(ban_log_data)
        file.close()

    def onavailable(self, server):
        """
        Logs Available Servers.
        :param server:
        :return: Nothing.
        """
        available_log_data = str(
            self.LogData['On_Server_Available'][0]).format(server)
        logfile = '{0}{1}resources{1}Logs{1}available_servers.log'.format(
            self.path, self.sepa)
        file = open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(available_log_data)
        file.close()

    def onunavailable(self, server):
        """
        Logs Unavailable Servers
        :param server: Servers.
        :return: Nothing.
        """
        unavailable_log_data = str(
            self.LogData['On_Server_Unavailable'][0]).format(server)
        logfile = '{0}{1}resources{1}Logs{1}unavailable_servers.log'.format(
            self.path, self.sepa)
        file = open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(unavailable_log_data)
        file.close()

    def onunban(self, server, user):
        """
        Logs Unbans.
        :param server: Server.
        :param user: Users.
        :return: Nothing.
        """
        unban_log_data = str(self.LogData['Unban_Logs'][0]
                             ).format(user.name, user.id, user.discriminator,
                                      server.name)
        logfile = '{0}{1}resources{1}Logs{1}unbans.log'.format(self.path,
                                                               self.sepa)
        file = open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(unban_log_data)
        file.close()

    def ongroupjoin(self, channel, user):
        """
        Logs group join.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        type(self)
        type(channel)
        type(user)
        # TODO: Implement this.
        pass

    def ongroupremove(self, channel, user):
        """
        Logs group remove.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        type(self)
        type(channel)
        type(user)
        # TODO: Implement this.
        pass

    def ontyping(self, channel, user, when):
        """
        Logs when a user is typing.
        :param channel: Channels.
        :param user: Users.
        :param when: Time.
        :return: Nothing.
        """
        type(self)
        type(channel)
        type(user)
        type(when)
        # TODO: Implement this.
        pass

    def onvoicestateupdate(self, before, after):
        """
        Logs When someone updates their voice state.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        type(self)
        type(before)
        type(after)
        # TODO: Implement this.
        pass

    def onchanneldelete(self, channel):
        """
        Logs Channel Deletion.
        :param channel: Channel.
        """
        type(self)
        type(channel)
        # TODO: Implement this.
        pass

    def onchannelcreate(self, channel):
        """
        Logs Channel Creation.
        :param channel: Channel.
        """
        type(self)
        type(channel)
        # TODO: Implement this.
        pass

    def onchannelupdate(self, before, after):
        """
        Logs Channel Updates.
        :param before: Channel before.
        :param after: Channel after.
        :return: Nothing.
        """
        type(self)
        type(before)
        type(after)
        # TODO: Implement this.
        pass

    def onmemberupdate(self, before, after):
        """
        Logs Member Updates.
        :param before: Member before.
        :param after: Member after.
        :return: Nothing.
        """
        type(self)
        type(before)
        type(after)
        # TODO: Implement this.
        pass

    def onserverjoin(self, server):
        """
        Logs server Joins.
        :param server: Server.
        :return: Nothing.
        """
        type(self)
        type(server)
        # TODO: Implement this.
        pass

    def onserverremove(self, server):
        """
        Logs server Removes.
        :param server: Server.
        :return: Nothing.
        """
        type(self)
        type(server)
        # TODO: Implement this.
        pass

    def onserverupdate(self, before, after):
        """
        Logs Server Updates.
        :param before: Server before.
        :param after: Server after.
        :return: Nothing.
        """
        type(self)
        type(before)
        type(after)
        # TODO: Implement this.
        pass

    def onserverrolecreate(self, role):
        """
        Logs role Creation.
        :param role: Role.
        :return: Nothing.
        """
        type(self)
        type(role)
        # TODO: Implement this.
        pass

    def onserverroledelete(self, role):
        """
        Logs role Deletion.
        :param role: Role.
        :return: Nothing.
        """
        type(self)
        type(role)
        # TODO: Implement this.
        pass

    def onserverroleupdate(self, before, after):
        """
        Logs Role updates.
        :param before: Role before.
        :param after: Role after.
        :return: Nothing.
        """
        type(self)
        type(before)
        type(after)
        # TODO: Implement this.
        pass

    def onsocketrawreceive(self, msg):
        """
        Logs socket Raw recieves.
        :param msg: Message from socket.
        :return: Nothing.
        """
        type(self)
        type(msg)
        # TODO: Implement this.
        pass

    def onsocketrawsend(self, payload):
        """
        Logs socket raw sends.
        :param payload: Payload that was sent.
        :return: Nothing.
        """
        type(self)
        type(payload)
        # TODO: Implement this.
        pass

    def onresumed(self):
        """
        Logs when bot resumes.
        :return: Nothing.
        """
        type(self)
        # TODO: Implement this.
        pass

    def onserveremojisupdate(self, before, after):
        """
        Logs Server emoji updates.
        :param before: Emoji before.
        :param after: Emoji after.
        :return: Nothing.
        """
        type(self)
        type(before)
        type(after)
        # TODO: Implement this.
        pass

    def onreactionadd(self, reaction, user):
        """
        Logs Reactions Added.
        :param reaction: Reaction.
        :param user: User.
        :return: Nothing.
        """
        type(self)
        type(reaction)
        type(user)
        # TODO: Implement this.
        pass

    def onreactionremove(self, reaction, user):
        """
        Logs Reaction Removals.
        :param reaction: Reaction.
        :param user: User.
        :return: Nothing.
        """
        type(self)
        type(reaction)
        type(user)
        # TODO: Implement this.
        pass

    def onreactionclear(self, message, reactions):
        """
        Logs Reaction clears.
        :param message: Message.
        :param reactions: Reactions.
        :return: Nothing.
        """
        type(self)
        type(message)
        type(reactions)
        # TODO: Implement this.
        pass

    def onmemberjoin(self, member):
        """
        Logs Member Joins.
        :param member: Member.
        :return: Nothing.
        """
        type(self)
        type(member)
        # TODO: Implement this.
        pass

    def onkick(self, member):
        """
        Logs Kicks.
        :param member: Members.
        :return: Nothing.
        """
        mem_name = member.name
        mem_id = member.id
        mem_dis = member.discriminator
        mem_svr_name = member.server.name
        kick_log_data = str(self.LogData['Kick_Logs'][0]).format(mem_name,
                                                                 mem_id,
                                                                 mem_dis,
                                                                 mem_svr_name)
        logfile = '{0}{1}resources{1}Logs{1}kicks.log'.format(self.path,
                                                              self.sepa)
        file = open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(kick_log_data)
        file.close()
