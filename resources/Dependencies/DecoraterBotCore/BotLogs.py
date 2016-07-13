# coding=utf-8
import discord
import io
import traceback
import sys
import os.path
import asyncio
import logging
import json
from discord.ext import commands

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


class BotLogs:
    def __init__(self, client):
        nothing = None

    class bot:
        """
            This class is for Internal use only!!!
        """

        @classmethod
        def set_up_discord_logger_code(self):
            logger = logging.getLogger('discord')
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(filename=sys.path[0] + '\\resources\\Logs\\discordpy.log', encoding='utf-8', mode='w')
            handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
            logger.addHandler(handler)

        @classmethod
        def set_up_asyncio_logger_code(self):
            asynciologger = logging.getLogger('asyncio')
            handler = logging.FileHandler(filename=sys.path[0] + '\\resources\\Logs\\asyncio.log', encoding='utf-8', mode='w')
            handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
            asynciologger.addHandler(handler)

        @classmethod
        def logs_code(self, client, message):
            Logs001 = str(LogData['On_Message_Logs'][0]).format(message.author.name, message.author.id, str(message.timestamp), message.content)
            LogsPM = Logs001
            if message.channel.is_private is False:
                Logs003 = str(LogData['On_Message_Logs'][1]).format(message.author.name, message.author.id, str(message.timestamp), message.channel.server.name, message.channel.name, message.content)
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

        @classmethod
        def edit_logs_code(self, client, before, after):
            old = str(before.content)
            new = str(after.content)
            logfile = sys.path[0] + '\\resources\\Logs\\edit log.txt'
            editlog001 = str(LogData['On_Message_Logs'][0]).format(before.author.name, before.author.id, str(before.timestamp), old, new)
            edit_log_PM = editlog001
            if before.channel.is_private is False:
                editlog003 = str(LogData['On_Message_Logs'][1]).format(before.author.name, before.author.id, str(before.timestamp), before.channel.server.name, before.channel.name, old, new)
                editlogServers = editlog003
            try:
                file = io.open(logfile, 'a', encoding='utf-8')
                size = os.path.getsize(logfile)
                if size >= 32102400:
                    file.seek(0)
                    file.truncate()
                    try:
                        if before.content == after.content:
                            _resolve_embed_logs(client, before, after)
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
                                _resolve_embed_logs(client, before, after)
                            else:
                                file.write(edit_log_PM)
            except PermissionError:
                return

        @classmethod
        def delete_logs_code(self, client, message):
            dellogs001 = str(LogData['On_Message_Logs'][0]).format(message.author.name, message.author.id, str(message.timestamp), message.content)
            dellogsPM = dellogs001
            if message.channel.is_private is False:
                dellogs003 = str(LogData['On_Message_Logs'][1]).format(message.author.name, message.author.id, str(message.timestamp), message.channel.server.name, message.channel.name, message.content)
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

        @classmethod
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

        @classmethod
        @asyncio.coroutine
        def send_logs_code(self, client, message):
            Logs001 = str(LogData['Send_On_Message_Logs'][0]).format(message.author.name, message.author.id, str(message.timestamp), message.channel.server.name, message.channel.name, message.content)
            sndmsglogs = Logs001
            try:
                yield from client.send_message(discord.Object(id='153055192873566208'), sndmsglogs)
            except discord.errors.NotFound:
                return

        @classmethod
        @asyncio.coroutine
        def send_edit_logs_code(self, client, before, after):
            old = str(before.content)
            new = str(after.content)
            editlog001 = str(LogData['Send_On_Message_Edit_Logs'][0]).format(before.author.name, before.author.id, str(before.timestamp), before.channel.server.name, before.channel.name, old, new)
            sendeditlogs = editlog001
            if before.content != after.content:
                try:
                    yield from client.send_message(discord.Object(id='153055192873566208'), sendeditlogs)
                except discord.errors.NotFound:
                    return

        @classmethod
        @asyncio.coroutine
        def send_delete_logs_code(self, client, message):
            dellogs001 = str(LogData['Send_On_Message_Delete_Logs'][0]).format(message.author.name, message.author.id, str(message.timestamp), message.channel.server.name, message.channel.name, message.content)
            senddeletelogs = dellogs001
            try:
                yield from client.send_message(discord.Object(id='153055192873566208'), senddeletelogs)
            except discord.errors.NotFound:
                return

        @classmethod
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

        @classmethod
        def onban_code(self, client, member):
            ban_log_data = str(LogData['Ban_Logs'][0]).format(member.name, member.discriminator, member.server.name)
            logfile = sys.path[0] + '\\resources\\Logs\\bans.txt'
            file = io.open(logfile, 'a', encoding='utf-8')
            size = os.path.getsize(logfile)
            if size >= 32102400:
                file.truncate()
            file.write(ban_log_data)

        @classmethod
        @asyncio.coroutine
        def onavailable_code(self, server):
            available_log_data = str(LogData['On_Server_Available'][0]).format(server)
            logfile = sys.path[0] + '\\resources\\Logs\\available_servers.txt'
            file = io.open(logfile, 'a', encoding='utf-8')
            size = os.path.getsize(logfile)
            if size >= 32102400:
                file.truncate()
            file.write(available_log_data)

        @classmethod
        @asyncio.coroutine
        def onunavailable_code(self, server):
            unavailable_log_data = str(LogData['On_Server_Unavailable'][0]).format(server)
            logfile = sys.path[0] + '\\resources\\Logs\\unavailable_servers.txt'
            file = io.open(logfile, 'a', encoding='utf-8')
            size = os.path.getsize(logfile)
            if size >= 32102400:
                file.truncate()
            file.write(unavailable_log_data)

        @classmethod
        def onunban_code(self, server, user):
            unban_log_data = str(LogData['Unban_Logs'][0]).format(user.name, user.discriminator, server.name)
            logfile = sys.path[0] + '\\resources\\Logs\\unbans.txt'
            file = io.open(logfile, 'a', encoding='utf-8')
            size = os.path.getsize(logfile)
            if size >= 32102400:
                file.truncate()
            file.write(unban_log_data)

        @classmethod
        def onkick_code(self, client, member):
            kick_log_data = str(LogData['Kick_Logs'][0]).format(member.name, member.discriminator, member.server.name)
            logfile = sys.path[0] + '\\resources\\Logs\\kicks.txt'
            file = io.open(logfile, 'a', encoding='utf-8')
            size = os.path.getsize(logfile)
            if size >= 32102400:
                file.truncate()
            file.write(kick_log_data)

    @classmethod
    def set_up_discord_logger(self):
        self.bot.set_up_discord_logger_code()

    @classmethod
    def set_up_asyncio_logger(self):
        self.bot.set_up_asyncio_logger_code()

    @classmethod
    def logs(self, client, message):
        self.bot.logs_code(client, message)

    @classmethod
    def edit_logs(self, client, before, after):
        self.bot.edit_logs_code(client, before, after)

    @classmethod
    def delete_logs(self, client, message):
        self.bot.delete_logs_code(client, message)

    @classmethod
    def _resolve_embed_logs(self, client, before, after):
        self.bot._resolve_embed_logs_code(client, before, after)

    @classmethod
    @asyncio.coroutine
    def send_logs(self, client, message):
        yield from self.bot.send_logs_code(client, message)

    @classmethod
    @asyncio.coroutine
    def send_edit_logs(self, client, before, after):
        yield from self.bot.send_edit_logs_code(client, before, after)

    @classmethod
    @asyncio.coroutine
    def send_delete_logs(self, client, message):
        yield from self.bot.send_delete_logs_code(client, message)

    @classmethod
    def gamelog(self, client, message, desgame):
        self.bot.gamelog_code(client, message, desgame)

    @classmethod
    def onban(self, client, member):
        self.bot.onban_code(client, member)

    @classmethod
    @asyncio.coroutine
    def onavailable(self, server):
        yield from self.bot.onavailable_code(server)

    @classmethod
    @asyncio.coroutine
    def onunavailable(self, server):
        yield from self.bot.onunavailable_code(server)

    @classmethod
    def onunban(self, server, user):
        self.bot.onunban_code(server, user)

    @classmethod
    def onkick(self, client, member):
        self.bot.onkick_code(client, member)
