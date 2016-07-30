# coding=utf-8
"""
    DecoraterBot's source is protected by Cheese.lab industries Inc. Even though it is Open Source
    any and all users waive the right to say that this bot's code was stolen when it really was not.
    Me @Decorater the only core developer of this bot do not take kindly to those false Allegations.
    it would piss any DEVELOPER OFF WHEN THEY SPEND ABOUT A YEAR CODING STUFF FROM SCRATCH AND THEN BE ACCUSED OF SHIT LIKE THIS.
    
    So, do not do it. If you do Cheese.lab Industries Inc. Can and Will do after you for such cliams that it deems untrue.
    
    Cheese.lab industries Inc. Belieces in the rights of Original Developers of bots. They do not take kindly to BULLSHIT.
    
    Any and all Developers work all the time, many of them do not get paid for their hard work.
    
    I am one of those who did not get paid even though I am the original Developer I coded this bot from the bottom with no lines of code at all.
    
    And how much money did I get from it for my 11 months or so of working on it? None- yeah thats right 0$ how pissed can someone be?
    Exactly I have over stretched my relatives money that they paid for Internet and power for my computer so that way I can code my bot.
    
    However shit does go out of the Fan with a possible 600$ or more that my Laptop Drastically needs to Repairs as it is 10 years old and is falling apart
    
    I am half tempted myself to pulling this bot from github and making it on patrion that boobot is also on to help me with my development needs.
    
    So, as such I accept issue requests, but please do not give me bullshit I hate it as it makes everything worse than the way it is.
    
    You do have the right however to:
        -> Contribute to the bot's development.
        -> fix bugs.
        -> add commands.
        -> help finish the per server config (has issues)
        -> update the Voice commands to be better (and not use globals which is 1 big thing that kills it).

    But keep in mind any and all Changes you make can and will be property of Cheese.lab Industries Inc.
"""
import discord
import io
import sys
import os.path
import asyncio
import logging
import json

try:
    consoledatafile = io.open(sys.path[0] + '\\resources\\ConfigData\\ConsoleWindow.json', 'r')
    consoletext = json.load(consoledatafile)
except FileNotFoundError:
    print('ConsoleWindow.json is not Found. Cannot Continue.')
    sys.exit(2)
try:
    LogDataFile = io.open(sys.path[0] + '\\resources\\ConfigData\\LogData.json', 'r')
    LogData = json.load(LogDataFile)
except FileNotFoundError:
    print(str(consoletext['Missing_JSON_Errors'][2]))
    sys.exit(2)


class bot_data:
    """
        This class is for Internal use only!!!
    """
    def __init__(self):
        pass

    def set_up_discord_logger_code(self):
        logger = logging.getLogger('discord')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename=sys.path[0] + '\\resources\\Logs\\discordpy.log', encoding='utf-8',
                                      mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)

    def set_up_asyncio_logger_code(self):
        asynciologger = logging.getLogger('asyncio')
        asynciologger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename=sys.path[0] + '\\resources\\Logs\\asyncio.log', encoding='utf-8',
                                      mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        asynciologger.addHandler(handler)

    def logs_code(self, client, message):
        """
            :type client: Discord.py Client object
            :param message: Message Object
        """
        Logs001 = str(LogData['On_Message_Logs'][0]).format(message.author.name, message.author.id,
                                                            str(message.timestamp), message.content)
        LogsPM = Logs001
        LogsServers = None
        if message.channel.is_private is False:
            Logs003 = str(LogData['On_Message_Logs'][1]).format(message.author.name, message.author.id,
                                                                str(message.timestamp), message.channel.server.name,
                                                                message.channel.name, message.content)
            LogsServers = Logs003
        if message.content is not None:
            logfile = sys.path[0] + '\\resources\\Logs\\log.txt'
            try:
                file = io.open(logfile, 'a', encoding='utf-8')
                size = os.path.getsize(logfile)
                if size >= 32102400:
                    file.seek(0)
                    file.truncate()
                if message.channel.is_private is True:
                    file.write(LogsPM)
                else:
                    file.write(LogsServers)
            except PermissionError:
                return

    def edit_logs_code(self, client, before, after):
        old = str(before.content)
        new = str(after.content)
        logfile = sys.path[0] + '\\resources\\Logs\\edit log.txt'
        usr_name = before.author.name
        usr_id = before.author.id
        msg_time = str(before.timestamp)
        editlog001 = str(LogData['On_Message_Logs'][0]).format(usr_name, usr_id, msg_time, old, new)
        edit_log_PM = editlog001
        editlogServers = None
        if before.channel.is_private is False:
            svr_name = before.channel.server.name
            chl_name = before.channel.name
            editlog003 = str(LogData['On_Message_Logs'][1]).format(usr_name, usr_id, msg_time, svr_name,
                                                                   chl_name, old, new)
            editlogServers = editlog003
        try:
            file = io.open(logfile, 'a', encoding='utf-8')
            size = os.path.getsize(logfile)
            if size >= 32102400:
                file.seek(0)
                file.truncate()
                try:
                    if before.content == after.content:
                        self._resolve_embed_logs_code(client, before, after)
                    else:
                        try:
                            file.write(editlogServers)
                        except PermissionError:
                            return
                except:
                    if before.channel.is_private is False:
                        print(str(LogData['On_Edit_Logs_Error'][0]))
                    else:
                        if before.content == after.content:
                            self._resolve_embed_logs_code(client, before, after)
                        else:
                            file.write(edit_log_PM)
        except PermissionError:
            return

    def delete_logs_code(self, client, message):
        dellogs001 = str(LogData['On_Message_Logs'][0]).format(message.author.name, message.author.id,
                                                               str(message.timestamp), message.content)
        dellogsPM = dellogs001
        dellogsServers = None
        if message.channel.is_private is False:
            dellogs003 = str(LogData['On_Message_Logs'][1]).format(message.author.name, message.author.id,
                                                                   str(message.timestamp),
                                                                   message.channel.server.name,
                                                                   message.channel.name, message.content)
            dellogsServers = dellogs003
        if message.content is not None:
            try:
                logfile = sys.path[0] + '\\resources\\Logs\\delete log.txt'
                file = io.open(logfile, 'a', encoding='utf-8')
                size = os.path.getsize(logfile)
                if size >= 32102400:
                    file.seek(0)
                    file.truncate()
                if message.channel.is_private is True:
                    file.write(dellogsPM)
                else:
                    file.write(dellogsServers)
            except PermissionError:
                return

    def _resolve_embed_logs_code(self, client, before, after):
        if before.channel.is_private is True:
            data = str(LogData['Embed_Logs'][0])
        else:
            data = str(LogData['Embed_Logs'][1])
        logfile = sys.path[0] + '\\resources\\Logs\\embeds.txt'
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
        Logs001 = str(LogData['Send_On_Message_Logs'][0]).format(message.author.name, message.author.id,
                                                                 str(message.timestamp),
                                                                 message.channel.server.name, message.channel.name,
                                                                 message.content)
        sndmsglogs = Logs001
        try:
            yield from client.send_message(discord.Object(id='153055192873566208'), sndmsglogs)
        except discord.errors.NotFound:
            return

    @asyncio.coroutine
    def send_edit_logs_code(self, client, before, after):
        old = str(before.content)
        new = str(after.content)
        editlog001 = str(LogData['Send_On_Message_Edit_Logs'][0]).format(before.author.name, before.author.id,
                                                                         str(before.timestamp),
                                                                         before.channel.server.name,
                                                                         before.channel.name, old, new)
        sendeditlogs = editlog001
        if before.content != after.content:
            try:
                yield from client.send_message(discord.Object(id='153055192873566208'), sendeditlogs)
            except discord.errors.NotFound:
                return

    @asyncio.coroutine
    def send_delete_logs_code(self, client, message):
        dellogs001 = str(LogData['Send_On_Message_Delete_Logs'][0]).format(message.author.name, message.author.id,
                                                                           str(message.timestamp),
                                                                           message.channel.server.name,
                                                                           message.channel.name, message.content)
        senddeletelogs = dellogs001
        try:
            yield from client.send_message(discord.Object(id='153055192873566208'), senddeletelogs)
        except discord.errors.NotFound:
            return

    @asyncio.coroutine
    def on_bot_error_code(self, funcname, tbinfo):
        if bool(funcname):
            if bool(tbinfo):
                exception_data = 'Ignoring exception caused at {0}:\n{1}'.format(funcname, tbinfo)
                logfile = sys.path[0] + '\\resources\\Logs\\error_log.txt'
                try:
                    file = io.open(logfile, 'a', encoding='utf-8')
                    size = os.path.getsize(logfile)
                    if size >= 32102400:
                        file.seek(0)
                        file.truncate()
                    file.write(exception_data)
                except PermissionError:
                    return
            else:
                raise
        else:
            raise

    def gamelog_code(self, client, message, desgame):
        gmelogdata01 = str(LogData['On_Message_Logs'][0]).format(message.author.name, desgame, message.author.id)
        gmelogsPM = gmelogdata01
        if message.channel.is_private is False:
            gmelog001 = str(LogData['On_Message_Logs'][1]).format(message.author.name, desgame, message.author.id)
            gmelogsServers = gmelog001
            logfile = sys.path[0] + '\\resources\\Logs\\gamelog.txt'
            try:
                file = io.open(logfile, 'a', encoding='utf-8')
                size = os.path.getsize(logfile)
                if size >= 32102400:
                    file.seek(0)
                    file.truncate()
                if message.channel.is_private is True:
                    file.write(gmelogsPM)
                else:
                    file.write(gmelogsServers)
            except PermissionError:
                return

    @asyncio.coroutine
    def onban_code(self, client, member):
        mem_name = member.name
        mem_id = member.id
        mem_dis = member.discriminator
        mem_svr_name = member.server.name
        ban_log_data = str(LogData['Ban_Logs'][0]).format(mem_name, mem_id, mem_dis, mem_svr_name)
        logfile = sys.path[0] + '\\resources\\Logs\\bans.txt'
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(ban_log_data)

    @asyncio.coroutine
    def onavailable_code(self, server):
        available_log_data = str(LogData['On_Server_Available'][0]).format(server)
        logfile = sys.path[0] + '\\resources\\Logs\\available_servers.txt'
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(available_log_data)

    @asyncio.coroutine
    def onunavailable_code(self, server):
        unavailable_log_data = str(LogData['On_Server_Unavailable'][0]).format(server)
        logfile = sys.path[0] + '\\resources\\Logs\\unavailable_servers.txt'
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(unavailable_log_data)

    @asyncio.coroutine
    def onunban_code(self, server, user):
        unban_log_data = str(LogData['Unban_Logs'][0]).format(user.name, user.id, user.discriminator, server.name)
        logfile = sys.path[0] + '\\resources\\Logs\\unbans.txt'
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(unban_log_data)

    @asyncio.coroutine
    def ongroupjoin_code(self, channel, user):
        # TODO: Impliment this.
        pass

    @asyncio.coroutine
    def ongroupremove_code(self, channel, user):
        # TODO: Impliment this.
        pass

    @asyncio.coroutine
    def onkick_code(self, client, member):
        mem_name = member.name
        mem_id = member.id
        mem_dis = member.discriminator
        mem_svr_name = member.server.name
        kick_log_data = str(LogData['Kick_Logs'][0]).format(mem_name, mem_id, mem_dis, mem_svr_name)
        logfile = sys.path[0] + '\\resources\\Logs\\kicks.txt'
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(kick_log_data)


class BotLogs:
    def __init__(self):
        self.bot = bot_data()

    def set_up_discord_logger(self):
        self.bot.set_up_discord_logger_code()

    def set_up_asyncio_logger(self):
        self.bot.set_up_asyncio_logger_code()

    def logs(self, client, message):
        self.bot.logs_code(client, message)

    def edit_logs(self, client, before, after):
        self.bot.edit_logs_code(client, before, after)

    def delete_logs(self, client, message):
        self.bot.delete_logs_code(client, message)

    def _resolve_embed_logs(self, client, before, after):
        self.bot._resolve_embed_logs_code(client, before, after)

    @asyncio.coroutine
    def send_logs(self, client, message):
        yield from self.bot.send_logs_code(client, message)

    @asyncio.coroutine
    def send_edit_logs(self, client, before, after):
        yield from self.bot.send_edit_logs_code(client, before, after)

    @asyncio.coroutine
    def send_delete_logs(self, client, message):
        yield from self.bot.send_delete_logs_code(client, message)

    @asyncio.coroutine
    def on_bot_error(self, funcname, tbinfo):
        """
            This Function is for Internal Bot use only.
            It is for catching any Errors and writing them to a file.

            Usage
            =====
            :param funcname: Must be a string with the name of the function that caused a Error.
                raises the Errors that happened if empty string or None is given.
            :param tbinfo: string data of the traceback info. Must be a string for this to not Error itself.
                raises the Errors that happened if empty string or None is given.
        """
        yield from self.bot.on_bot_error_code(funcname, tbinfo)

    def gamelog(self, client, message, desgame):
        self.bot.gamelog_code(client, message, desgame)

    @asyncio.coroutine
    def onban(self, client, member):
        yield from self.bot.onban_code(client, member)

    @asyncio.coroutine
    def onavailable(self, server):
        yield from self.bot.onavailable_code(server)

    @asyncio.coroutine
    def onunavailable(self, server):
        yield from self.bot.onunavailable_code(server)

    @asyncio.coroutine
    def onunban(self, server, user):
        yield from self.bot.onunban_code(server, user)

    @asyncio.coroutine
    def ongroupjoin(self, channel, user):
        yield from self.bot.ongroupjoin_code(channel, user)

    @asyncio.coroutine
    def ongroupremove(self, channel, user):
        yield from self.bot.ongroupremove_code(channel, user)

    @asyncio.coroutine
    def onkick(self, client, member):
        yield from self.bot.onkick_code(client, member)
