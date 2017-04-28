# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import sys
import logging
import json
import os

import discord

__all__ = ['BotLogger']


# Some loggers lack the ability to get the server
# the event fired on.


class BotLogger:
    """
    Main Bot logging Class.
    """
    def __init__(self, bot):
        self.bot = bot
        try:
            self.LogDataFile = open('{0}{1}resources{1}'
                                    'ConfigData{1}LogData.{2}.'
                                    'json'.format(self.bot.path, self.bot.sepa,
                                                  self.bot.BotConfig.language))
            self.LogData = json.load(self.LogDataFile)
            self.LogDataFile.close()
        except FileNotFoundError:
            print(str(self.bot.consoletext['Missing_JSON_Errors'][2]))
            sys.exit(2)

    def log_writter(self, filename, data):
        """
        Log file writter.

        This is where all the common
        log file writes go to.
        """
        str(self)
        file = open(filename, 'a', encoding='utf-8')
        size = os.path.getsize(filename)
        if size >= 32102400:
            file.seek(0)
            file.truncate()
        file.write(data)
        file.close()

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
                        self.bot.path, self.bot.sepa), encoding='utf-8', mode='w')
                handler.setFormatter(logging.Formatter(
                    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
                logger.addHandler(handler)
            elif loggers == 'asyncio' and self.bot is not None:
                self.bot.loop.set_debug(True)
                asynciologger = logging.getLogger('asyncio')
                asynciologger.setLevel(logging.DEBUG)
                asynciologgerhandler = logging.FileHandler(
                    filename='{0}{1}resources{1}Logs{1}asyncio.log'.format(
                        self.bot.path, self.bot.sepa), encoding='utf-8', mode='w')
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

    def log_data_reader(entry, index, *args):
        """
        log data reader that also
        does the needed formatting.

        method specifically to fix the
        stupid Codacy duplication bug.
        """
        return str(self.LogData[entry][index]).format(
            *args)

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
                self.bot.path, self.bot.sepa)
            try:
                if message.channel.is_private is True:
                    self.log_writter(logfile, logspm)
                else:
                    self.log_writter(logfile, logsservers)
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
        logfile = '{0}{1}resources{1}Logs{1}edit_log.log'.format(self.bot.path,
                                                                 self.bot.sepa)
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
            try:
                if before.content == after.content:
                    self.resolve_embed_logs(before)
                else:
                    try:
                        self.log_writter(logfile, editlogservers)
                    except PermissionError:
                        return
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
                        self.log_writter(logfile, edit_log_pm)
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
                    self.bot.path, self.bot.sepa)
                if message.channel.is_private is True:
                    self.log_writter(logfile, dellogspm)
                else:
                    self.log_writter(logfile, dellogsservers)
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
        logfile = '{0}{1}resources{1}Logs{1}embeds.log'.format(self.bot.path,
                                                               self.bot.sepa)
        try:
            self.log_writter(logfile, data + "\n")
        except PermissionError:
            return

    async def send_logs(self, message):
        """
        Sends Sent Messages.
        :param message: Messages.
        :return: Nothing.
        """
        logs001 = self.log_data_reader(
            'Send_On_Message_Logs', 0,
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
        dellogs001 = self.log_data_reader(
            'Send_On_Message_Delete_Logs', 0,
            message.author.name, message.author.id, str(message.timestamp),
            message.channel.server.name, message.channel.name,
            message.content)
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
                    self.bot.path, self.bot.sepa)
                try:
                    self.log_writter(logfile, exception_data)
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
        logfile = '{0}{1}resources{1}Logs{1}gamelog.log'.format(self.bot.path,
                                                                self.bot.sepa)
        try:
            if ctx.message.channel.is_private is True:
                self.log_writter(logfile, gmelogspm)
            else:
                self.log_writter(logfile, gmelogsservers)
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
        logfile = '{0}{1}resources{1}Logs{1}bans.log'.format(self.bot.path,
                                                             self.bot.sepa)
        self.log_writter(logfile, ban_log_data)

    async def send_ban_logs(self, channel, member):
        """
        sends the ban log data to a specific channel.
        """
        ban_log_data = str(self.LogData['Send_Ban_Logs'][0]).format(
            member.name, member.id, member.discriminator)
        try:
            await self.bot.send_message(
                channel, content=ban_log_data)
        except discord.errors.NotFound:
            return
        except discord.errors.HTTPException:
            return

    def onavailable(self, server):
        """
        Logs Available Servers.
        :param server:
        :return: Nothing.
        """
        available_log_data = str(
            self.LogData['On_Server_Available'][0]).format(server)
        logfile = '{0}{1}resources{1}Logs{1}available_servers.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, available_log_data)

    def onunavailable(self, server):
        """
        Logs Unavailable Servers
        :param server: Servers.
        :return: Nothing.
        """
        unavailable_log_data = str(
            self.LogData['On_Server_Unavailable'][0]).format(server)
        logfile = '{0}{1}resources{1}Logs{1}unavailable_servers.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, unavailable_log_data)

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
        logfile = '{0}{1}resources{1}Logs{1}unbans.log'.format(self.bot.path,
                                                               self.bot.sepa)
        self.log_writter(logfile, unban_log_data)

    async def send_unban_logs(self, channel, user):
        """
        sends the unban log data to a specific channel.
        """
        unban_log_data = str(self.LogData['Send_Unban_Logs'][0]).format(
            user.name, user.id, user.discriminator)
        try:
            await self.bot.send_message(
                channel, content=unban_log_data)
        except discord.errors.NotFound:
            return
        except discord.errors.HTTPException:
            return

    def ongroupjoin(self, channel, user):
        """
        Logs group join.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        mem_name = user.name
        mem_id = user.id
        mem_dis = user.discriminator
        mem_channel_name = channel.name
        group_join_log_data = str(self.LogData['Group_Join_Logs'][0]).format(
            mem_name, mem_id, mem_dis, mem_channel_name)
        logfile = '{0}{1}resources{1}Logs{1}group_join.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, group_join_log_data)

    def ongroupremove(self, channel, user):
        """
        Logs group remove.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        mem_name = user.name
        mem_id = user.id
        mem_dis = user.discriminator
        mem_channel_name = channel.name
        group_remove_log_data = str(self.LogData['Group_Remove_Logs'][0]).format(
            mem_name, mem_id, mem_dis, mem_channel_name)
        logfile = '{0}{1}resources{1}Logs{1}group_remove.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, group_remove_log_data)

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

    def onvoicestateupdate(self, before, after):
        """
        Logs When someone updates their voice state.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        mem_name = before.user.name
        mem_id = before.user.id
        mem_dis = before.user.discriminator
        before_channel_name = before.channel.name
        after_channel_name = after.channel.name
        voice_update_log_data = str(self.LogData['voice_update'][0]).format(
            mem_name, mem_id, mem_dis, before_channel_name,
            after_channel_name)
        logfile = '{0}{1}resources{1}Logs{1}voice_update.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, voice_update_log_data)

    def onchanneldelete(self, channel):
        """
        Logs Channel Deletion.
        :param channel: Channel.
        """
        channel_delete_log_data = str(self.LogData['channel_delete'][0]).format(
            channel.name, channel.id)
        logfile = '{0}{1}resources{1}Logs{1}channel_delete.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, channel_delete_log_data)

    def onchannelcreate(self, channel):
        """
        Logs Channel Creation.
        :param channel: Channel.
        """
        channel_create_log_data = str(self.LogData['channel_create'][0]).format(
            channel.name, channel.id)
        logfile = '{0}{1}resources{1}Logs{1}channel_create.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, channel_create_log_data)

    def onchannelupdate(self, before, after):
        """
        Logs Channel Updates.
        :param before: Channel before.
        :param after: Channel after.
        :return: Nothing.
        """
        # change of permittions trigger this???
        channel_update_log_data = str(self.LogData['channel_update'][0]).format(
            before.name, before.id, after.name)
        logfile = '{0}{1}resources{1}Logs{1}channel_update.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, channel_update_log_data)

    def onmemberupdate(self, before, after):
        """
        Logs Member Updates.
        :param before: Member before.
        :param after: Member after.
        :return: Nothing.
        """
        # change of permittions trigger this???
        member_update_log_data = str(self.LogData['member_update'][0]).format(
            before.name, before.id, after.name)
        logfile = '{0}{1}resources{1}Logs{1}member_update.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, member_update_log_data)

    def onserverjoin(self, server):
        """
        Logs server Joins.
        :param server: Server.
        :return: Nothing.
        """
        server_join_log_data = str(self.LogData['server_join'][0]).format(
            self.bot.user.name, self.bot.user.id, server.name)
        logfile = '{0}{1}resources{1}Logs{1}server_join.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, server_join_log_data)

    def onserverremove(self, server):
        """
        Logs server Removes.
        :param server: Server.
        :return: Nothing.
        """
        server_remove_log_data = str(self.LogData['server_remove'][0]).format(
            self.bot.user.name, self.bot.user.id, server.name)
        logfile = '{0}{1}resources{1}Logs{1}server_remove.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, server_remove_log_data)

    def onserverupdate(self, before, after):
        """
        Logs Server Updates.
        :param before: Server before.
        :param after: Server after.
        :return: Nothing.
        """
        server_update_log_data = str(self.LogData['server_update'][0]).format(
            before.name, before.id, after.name)
        logfile = '{0}{1}resources{1}Logs{1}server_update.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, server_update_log_data)

    def onserverrolecreate(self, role):
        """
        Logs role Creation.
        :param role: Role.
        :return: Nothing.
        """
        role_create_log_data = str(self.LogData['role_create'][0]).format(
            role.name, role.id)
        logfile = '{0}{1}resources{1}Logs{1}role_create.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, role_create_log_data)

    def onserverroledelete(self, role):
        """
        Logs role Deletion.
        :param role: Role.
        :return: Nothing.
        """
        role_delete_log_data = str(self.LogData['role_delete'][0]).format(
            role.name, role.id)
        logfile = '{0}{1}resources{1}Logs{1}role_delete.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, role_delete_log_data)

    def onserverroleupdate(self, before, after):
        """
        Logs Role updates.
        :param before: Role before.
        :param after: Role after.
        :return: Nothing.
        """
        # change of permittions trigger this???
        role_update_log_data = str(self.LogData['role_update'][0]).format(
            before.name, before.id, after.name)
        logfile = '{0}{1}resources{1}Logs{1}role_update.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, role_update_log_data)

    def onsocketrawreceive(self, msg):
        """
        Logs socket Raw recieves.
        :param msg: Message from socket.
        :return: Nothing.
        """
        type(self)
        type(msg)
        # TODO: Implement this.

    def onsocketrawsend(self, payload):
        """
        Logs socket raw sends.
        :param payload: Payload that was sent.
        :return: Nothing.
        """
        type(self)
        type(payload)
        # TODO: Implement this.

    def onresumed(self):
        """
        Logs when bot resumes.
        :return: Nothing.
        """
        type(self)
        # TODO: Implement this.

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

    def onmemberjoin(self, member):
        """
        Logs Member Joins.
        :param member: Member.
        :return: Nothing.
        """
        type(self)
        type(member)
        # TODO: Implement this.

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
        logfile = '{0}{1}resources{1}Logs{1}kicks.log'.format(self.bot.path,
                                                              self.bot.sepa)
        self.log_writter(logfile, kick_log_data)
