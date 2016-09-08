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
import ctypes
import sys
import time
import asyncio
import json
import traceback
import importlib
import io

class BotConfigVars:
    """
    Class for getting the Credentials.json config Values.
    """
    def __init__(self):
        sepa = os.sep
        PATH = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(sys.path[0], sepa)
        self.credsfile = io.open(PATH)
        self.credentials = json.load(self.credsfile)
        self.credsfile.close()

    @property
    def logging(self):
        """
        Function that returns weather to have normal logging or not.
        :return: Bool
        """
        value = self.credentials['logging']
        return value

    @property
    def logbans(self):
        """
        Returns weather to log bans or not.
        :return: Bool
        """
        value = self.credentials['logbans']
        return value

    @property
    def logunbans(self):
        """
        Returns weather to log unbans or not.
        :return: Bool
        """
        value = self.credentials['logunbans']
        return value

    @property
    def logkicks(self):
        """
        Returns weather to log kicks or not.
        :return: Bool
        """
        value = self.credentials['logkicks']
        return value

    @property
    def log_games(self):
        value = self.credentials['loggames']
        return value

    @property
    def discord_logger(self):
        """
        Returns weather to use the discord.py logger or not.
        :return: Bool
        """
        value = self.credentials['discord_py_logger']
        return value

    @property
    def asyncio_logger(self):
        """
        Returns weather to use the asyncio logger or not.
        :return: Bool
        """
        value = self.credentials['asyncio_logger']
        return value

    @property
    def log_available(self):
        """
        Returns weather to log available servers or not.
        :return: Bool
        """
        value = self.credentials['LogServerAvailable']
        return value

    @property
    def log_unavailable(self):
        """
        Returns weather to log unavailable servers or not.
        :return: Bool
        """
        value = self.credentials['LogServerUnavailable']
        return value

    @property
    def log_channel_create(self):
        """
        Returns weather to log Created Channels or not.
        :return: Bool
        """
        value = self.credentials['log_channel_create']
        return value

    @property
    def owner_id(self):
        value = str(self.credentials['ownerid'][0])
        if value == 'None':
            value = None
        return value

    @property
    def is_official_bot(self):
        value = self.credentials['Is_Official_Bot_Account']
        return value

    @property
    def log_ytdl(self):
        value = self.credentials['ytdl_logs']
        return value

    @property
    def pm_commands_list(self):
        value = self.credentials['PM_Commands']
        return value

    @property
    def log_channel_delete(self):
        """
        Returns weather to log Deleted Channels or not.
        :return: Bool
        """
        value = self.credentials['log_channel_delete']
        return value

    @property
    def log_channel_update(self):
        """
        Returns weather to log updated Channels or not.
        :return: Bool
        """
        value = self.credentials['log_channel_update']
        return value

    @property
    def log_member_update(self):
        """
        Returns weather to log member updates or not.
        :return: Bool
        """
        value = self.credentials['log_member_update']
        return value

    @property
    def log_server_join(self):
        """
        Returns weather to log Server Joins.
        :return: Bool
        """
        value = self.credentials['log_server_join']
        return value

    @property
    def log_server_remove(self):
        """
        Returns weather to log when a Server is removed.
        :return: Bool
        """
        value = self.credentials['log_server_remove']
        return value

    @property
    def log_server_update(self):
        """
        Returns weather to log when a Server is updated.
        :return: Bool
        """
        value = self.credentials['log_server_update']
        return value

    @property
    def log_server_role_create(self):
        """
        Returns weather to log when a role is created.
        :return: Bool
        """
        value = self.credentials['log_server_role_create']
        return value

    @property
    def log_server_role_delete(self):
        """
        Returns weather to log when a role was deleted.
        :return: Bool
        """
        value = self.credentials['log_server_role_delete']
        return value

    @property
    def log_server_role_update(self):
        """
        Returns weather to log when a role was updated.
        :return:
        """
        value = self.credentials['log_server_role_update']
        return value

    @property
    def log_group_join(self):
        """
        Returns weather to log group joins or not.
        :return: Bool
        """
        value = self.credentials['log_group_join']
        return value

    @property
    def log_group_remove(self):
        """
        Returns weather to log group removes or not.
        :return: Bool
        """
        value = self.credentials['log_group_remove']
        return value

    @property
    def log_error(self):
        """
        Returns weather to log bot errors or not.
        :return: Bool
        """
        value = self.credentials['log_error']
        return value

    @property
    def log_voice_state_update(self):
        """
        Returns weather to log Voice State Updates or not.
        :return: Bool
        """
        value = self.credentials['log_voice_state_update']
        return value

    @property
    def log_typing(self):
        """
        Returns Weather to log typing or not.
        :return: Bool
        """
        value = self.credentials['log_typing']
        return value

    @property
    def log_socket_raw_receive(self):
        """
        Returns weather to log socket raw recieve data or not.
        :return: Bool
        """
        value = self.credentials['log_socket_raw_receive']
        return value

    @property
    def log_socket_raw_send(self):
        """
        Returns weather to log raw socket send data.
        :return: Bool
        """
        value = self.credentials['log_socket_raw_send']
        return value

    @property
    def log_resumed(self):
        """
        Returns weather to log bot connection resumes or not.
        :return: Bool
        """
        value = self.credentials['log_resumed']
        return value

    @property
    def log_member_join(self):
        """
        Returns weather to log when a person joins a server.
        :return: Bool
        """
        value = self.credentials['log_member_join']
        return value

    @property
    def pm_command_errors(self):
        value = self.credentials['pm_command_errors']
        return value

    @property
    def enable_error_handler(self):
        """
        Returns weather to use the Error Handler or not.
        :return: Bool
        """
        value = None
        if self.pm_command_errors:
            value = False
        else:
            value = True
        return value

    @property
    def bot_prefix(self):
        """
        Returns the Bot Prefix.
        :return:
        """
        value = str(self.credentials['bot_prefix'][0])
        if value == '':
            value = None
        if value is None:
            print('No Prefix specified in Credentials.json. The Bot cannot continue.')
            sys.exit(2)
        return value

    @property
    def discord_user_id(self):
        value = str(self.credentials['ownerid'][0])
        if value == 'None':
            value = None
        return value

    @property
    def discord_user_email(self):
        value = str(self.credentials['email'][0])
        if value == 'None':
            value = None
        return value

    @property
    def discord_user_password(self):
        value = str(self.credentials['password'][0])
        if value == 'None':
            value = None
        return value

    @property
    def bot_token(self):
        value = str(self.credentials['token'][0])
        if value == 'None':
            value = None
        return value

    @property
    def bot_id(self):
        value = str(self.credentials['botid'][0])
        if value == 'None':
            value = None
        return value

    @property
    def disable_voice_commands(self):
        value = self.credentials['disable_voice']
        return value
