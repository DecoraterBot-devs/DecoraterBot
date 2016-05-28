# coding=utf-8
import discord
import io
import traceback
import sys
import os.path
import asyncio
import json
try:
    consoledatafile = io.open(sys.path[0] + '\ConfigData\ConsoleWindow.json', 'r')
    consoletext = json.load(consoledatafile)
except FileNotFoundError:
    print('ConsoleWindow.json is not Found. Cannot Continue.')
    sys.exit(2)
try:
    LogDataFile = io.open(sys.path[0] + '\ConfigData\LogData.json', 'r')
    LogData = json.load(LogDataFile)
except FileNotFoundError:
    print(str(consoletext['Missing_JSON_Errors'][2]))
    sys.exit(2)


class BotLogs:
    # noinspection PyUnboundLocalVariable
    def logs(client, message):
        # noinspection PyPep8Naming
        Logs001 = str(LogData['On_Message_Logs'][0]) + message.author.name + str(LogData['On_Message_Logs'][1])
        # noinspection PyPep8Naming
        Logs002 = message.author.id + str(LogData['On_Message_Logs'][2]) + str(message.timestamp)
        # noinspection PyPep8Naming
        LogsPM001 = str(LogData['On_Message_Logs'][3]) + message.content + "\n"
        # noinspection PyPep8Naming
        LogsPM = Logs001 + Logs002 + LogsPM001
        if message.channel.is_private is False:
            logs_003_data = str(LogData['On_Message_Logs'][4])
            # noinspection PyPep8Naming
            Logs003 = logs_003_data + message.channel.server.name + str(LogData['On_Message_Logs'][5])
            # noinspection PyPep8Naming
            Logs004 = message.channel.name + str(LogData['On_Message_Logs'][3]) + message.content
            # noinspection PyPep8Naming
            Logs005 = "\n"
            # noinspection PyPep8Naming
            LogsServers = Logs001 + Logs002 + Logs003 + Logs004 + Logs005
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

    def edit_logs(client, before, after):
        old = str(before.content)
        new = str(after.content)
        logfile = sys.path[0] + '\\resources\\Logs\\edit log.txt'
        editlog001 = str(LogData['On_Message_Logs'][0]) + before.author.name + str(LogData['On_Message_Logs'][1])
        editlog002 = before.author.id + str(LogData['On_Message_Logs'][2]) + str(before.timestamp)
        # noinspection PyPep8Naming
        editlogPM001 = str(LogData['On_Message_Edit_Logs'][0]) + old + str(LogData['On_Message_Edit_Logs'][1]) + new
        # noinspection PyPep8Naming
        editlogPM002 = "\n"
        # noinspection PyPep8Naming
        edit_log_PM = editlog001 + editlog002 + editlogPM001 + editlogPM002
        if before.channel.is_private is False:
            editlog003 = str(LogData['On_Message_Logs'][4]) + before.channel.server.name
            editlog004 = str(LogData['On_Message_Logs'][5])
            editlog005 = before.channel.name + str(LogData['On_Message_Edit_Logs'][0]) + old
            editlog006 = str(LogData['On_Message_Edit_Logs'][1]) + new
            eld = "\n"
            # noinspection PyPep8Naming
            editlogServers = editlog001 + editlog002 + editlog003 + editlog004 + editlog005 + editlog006 + eld
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
                            # noinspection PyUnboundLocalVariable
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

    def delete_logs(client, message):
        dellogs001 = str(LogData['On_Message_Logs'][0]) + message.author.name + str(LogData['On_Message_Logs'][1])
        dellogs002 = message.author.id + str(LogData['On_Message_Logs'][2]) + str(message.timestamp)
        # noinspection PyPep8Naming
        dellogsPM001 = str(LogData['On_Message_Logs'][3]) + message.content + "\n"
        # noinspection PyPep8Naming
        dellogsPM = dellogs001 + dellogs002 + dellogsPM001
        dellogs003 = str(LogData['On_Message_Logs'][4]) + message.channel.server.name
        dellogs004 = str(LogData['On_Message_Logs'][5])
        dellogs005 = message.channel.name + str(LogData['On_Message_Logs'][3]) + message.content
        dellogs006 = '\n'
        # noinspection PyPep8Naming
        dellogsServers = dellogs001 + dellogs002 + dellogs003 + dellogs004 + dellogs005 + dellogs006
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

    # noinspection PyUnusedLocal
    def _resolve_embed_logs(client, before, after):
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

    async def send_logs(client, message):
        # noinspection PyPep8Naming
        Logs001 = str(LogData['On_Message_Logs'][0]) + message.author.name + str(LogData['On_Message_Logs'][1])
        # noinspection PyPep8Naming
        Logs002 = message.author.id + str(LogData['On_Message_Logs'][2]) + str(message.timestamp)
        # noinspection PyPep8Naming
        Logs003 = str(LogData['On_Message_Logs'][4]) + message.channel.server.name + str(LogData['On_Message_Logs'][5])
        # noinspection PyPep8Naming
        Logs004 = message.channel.name + str(LogData['On_Message_Logs'][3]) + message.content
        sndmsglogs001 = str(LogData['Send_On_Message_Logs'][0])
        sndmsglogs = Logs001 + Logs002 + Logs003 + Logs004 + sndmsglogs001
        try:
            await client.send_message(discord.Object(id='153055192873566208'), sndmsglogs)
        except discord.errors.NotFound:
            return

    # noinspection PyUnusedLocal
    async def send_edit_logs(client, before, after):
        old = str(before.content)
        new = str(after.content)
        editlog001 = str(LogData['On_Message_Logs'][0]) + before.author.name + str(LogData['On_Message_Logs'][1])
        editlog002 = before.author.id + str(LogData['On_Message_Logs'][2]) + str(before.timestamp)
        editlog003 = str(LogData['On_Message_Logs'][4]) + before.channel.server.name
        editlog004 = str(LogData['On_Message_Logs'][5])
        editlog005 = before.channel.name + str(LogData['On_Message_Edit_Logs'][0]) + old
        editlog006 = str(LogData['On_Message_Edit_Logs'][1]) + new
        sel = str(LogData['Send_On_Message_Edit_Logs'][0])
        sendeditlogs = editlog001 + editlog002 + editlog003 + editlog004 + editlog005 + editlog006 + sel
        if before.content != after.content:
            try:
                await client.send_message(discord.Object(id='153055192873566208'), sendeditlogs)
            except discord.errors.NotFound:
                return

    async def send_delete_logs(client, message):
        dellogs001 = str(LogData['On_Message_Logs'][0]) + message.author.name + str(LogData['On_Message_Logs'][1])
        dellogs002 = message.author.id + str(LogData['On_Message_Logs'][2]) + str(message.timestamp)
        dellogs003 = str(LogData['On_Message_Logs'][4]) + message.channel.server.name
        dellogs004 = str(LogData['On_Message_Logs'][5])
        dellogs005 = message.channel.name + str(LogData['On_Message_Logs'][3]) + message.content
        snddellogs001 = str(LogData['Send_On_Message_Delete_Logs'][0])
        senddeletelogs = dellogs001 + dellogs002 + dellogs003 + dellogs004 + dellogs005 + snddellogs001
        try:
            await client.send_message(discord.Object(id='153055192873566208'), senddeletelogs)
        except discord.errors.NotFound:
            return

    def gamelog(client, message, desgame):
        gmelogdata01 = str(LogData['On_Message_Logs'][0]) + message.author.name + str(LogData['Game_Logs'][0]) + desgame
        gmelogdata02 = '. (' + message.author.id + ")"
        # noinspection PyPep8Naming
        gmelogPM001 = "(PM)\n"
        # noinspection PyPep8Naming
        gmelogsPM = gmelogdata01 + gmelogdata02 + gmelogPM001
        gmelog001 = "(Servers)\n"
        # noinspection PyPep8Naming
        gmelogsServers = gmelogdata01 + gmelogdata02 + gmelog001
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

    async def onban(client, member):
        logfile = sys.path[0] + '\\resources\\Logs\\bans.txt'
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(member.name + str(LogData['Ban_Logs'][0]) + member.discriminator + str(LogData['Ban_Logs'][1]) +
                   member.server.name + '.\n')

    async def onunban(server, user):
        logfile = sys.path[0] + '\\resources\\Logs\\unbans.txt'
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(user.name + str(LogData['Unban_Logs'][0]) + server.name + '.\n')

    async def onkick(client, member):
        logfile = sys.path[0] + '\\resources\\Logs\\kicks.txt'
        file = io.open(logfile, 'a', encoding='utf-8')
        size = os.path.getsize(logfile)
        if size >= 32102400:
            file.truncate()
        file.write(member.name + str(LogData['Kick_Logs'][0]) + member.discriminator + str(LogData['Kick_Logs'][1]) +
                   member.server.name + '.\n')
