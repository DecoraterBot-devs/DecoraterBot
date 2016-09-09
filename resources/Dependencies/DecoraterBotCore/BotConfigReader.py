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
import os
import sys


class BotConfigVars:
    """
    Class for getting the Credentials.json config Values.
    """
    def __init__(self):
        sepa = os.sep
        self.json_file = '{0}{1}resources{1}ConfigData{1}Credentials.json'.format(sys.path[0], sepa)
        self.credentials = None
        self.value = None
        self.load()

        # Properties.
        self.logging = self.credentials['logging']  # bool
        self.logbans = self.credentials['logbans']  # bool
        self.logunbans = self.credentials['logunbans']  # bool
        self.logkicks = self.credentials['logkicks']  # bool
        self.log_games = self.credentials['loggames']  # bool
        self.discord_logger = self.credentials['discord_py_logger']  # bool
        self.asyncio_logger = self.credentials['asyncio_logger']  # bool
        self.log_available = self.credentials['LogServerAvailable']  # bool
        self.log_unavailable = self.credentials['LogServerUnavailable']  # bool
        self.log_channel_create = self.credentials['log_channel_create']  # bool
        self.is_official_bot = self.credentials['Is_Official_Bot_Account']  # bool
        self.log_ytdl = self.credentials['ytdl_logs']  # bool
        self.pm_commands_list = self.credentials['PM_Commands']  # bool
        self.log_channel_delete = self.credentials['log_channel_delete']  # bool
        self.log_channel_update = self.credentials['log_channel_update']  # bool
        self.log_member_update = self.credentials['log_member_update']  # bool
        self.log_server_join = self.credentials['log_server_join']  # bool
        self.log_server_remove = self.credentials['log_server_remove']  # bool
        self.log_server_update = self.credentials['log_server_update']  # bool
        self.log_server_role_create = self.credentials['log_server_role_create']  # bool
        self.log_server_role_delete = self.credentials['log_server_role_delete']  # bool
        self.log_server_role_update = self.credentials['log_server_role_update']  # bool
        self.log_group_join = self.credentials['log_group_join']  # bool
        self.log_group_remove = self.credentials['log_group_remove']  # bool
        self.log_error = self.credentials['log_error']  # bool
        self.log_voice_state_update = self.credentials['log_voice_state_update']  # bool
        self.log_typing = self.credentials['log_typing']  # bool
        self.log_socket_raw_receive = self.credentials['log_socket_raw_receive']  # bool
        self.log_socket_raw_send = self.credentials['log_socket_raw_send']  # bool
        self.log_resumed = self.credentials['log_resumed']  # bool
        self.log_member_join = self.credentials['log_member_join']  # bool
        self.pm_command_errors = self.credentials['pm_command_errors']  # bool
        self.enable_error_handler = self.enable_error_handler_code  # bool
        self.bot_prefix = self.credentials['bot_prefix']  # string
        self.discord_user_id = self.credentials['ownerid']  # string
        self.discord_user_email = self.credentials['email']  # string
        self.discord_user_password = self.credentials['password']  # string
        self.bot_token = self.credentials['token']  # string
        self.disable_voice_commands = self.credentials['disable_voice']  # bool

    def load(self):
        """
        Loads the JSON config Data.
        :return: List.
        """
        try:
            with open(self.json_file) as file:
                self.credentials = json.load(file)
        except(OSError, IOError):
            pass

    @property
    def enable_error_handler_code(self):
        """
        Returns weather to use the Error Handler or not.
        :return: Bool
        """
        if self.pm_command_errors:
            self.value = False
        else:
            self.value = True
        return self.value
