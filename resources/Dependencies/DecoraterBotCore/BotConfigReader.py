# coding=utf-8
"""
DecoraterBotCore
~~~~~~~~~~~~~~~~~~~

Core to DecoraterBot

:copyright: (c) 2015-2017 Decorater
:license: MIT, see LICENSE for more details.

"""
import json
import os
import sys


__all__ = ['BotCredentialsVars', 'CreditsReader', 'PluginTextReader',
           'PluginConfigReader']


class BaseConfigReader:
    """
    Base config Class.
    """
    def __init__(self, file=None):
        self.config = None
        self.filename = file
        self.file = None
        self.json_file = None
        self.load()

    def load(self):
        """
        Loads the JSON config Data.
        :return: List.
        """
        self.json_file = os.path.join(
            sys.path[0], 'resources', 'ConfigData',
            self.filename)
        try:
            with open(self.json_file) as self.file:
                self.config = json.load(self.file)
        except(OSError, IOError):
            pass

    def getconfig(self, key):
        """
        Gets a JSON Config Value basted on the key provided.
        :param key: String key to the entry in the JSON file
        :return: JSON config Value.
        """
        return self.config[key]

    def setconfig(self, key, data):
        """
        Sets a JSON Config Value basted on the key and data provided.
        :param key: String key to the entry in the JSON file
        :param data: Data to replace old value with.
        """
        self.config[key] = data
        with open(self.json_file) as self.file:
            json.dump(self.config, self.file, indent=4, sort_keys=True)


class BaseCredentialsReader(BaseConfigReader):
    """
    Base config Class.
    """
    def __init__(self, file=None):
        super(BaseCredentialsReader, self).__init__(file=file)


class CreditsReader(BaseConfigReader):
    """
    Obtains Data from credits.json
    """
    def __init__(self, file=None):
        super(CreditsReader, self).__init__(file=file)

    def getcredits(self, key, key2):
        """
        Gets a JSON Config Value basted on the key provided.
        :param key: String key to the entry in the JSON file.
        :param key2: String key to the entry in the JSON file.
        :return: JSON config Value.
        """
        return self.config[key][key2]

    def setcredits(self, key, key2, data):
        """
        Sets a JSON Config Value basted on the key and data provided.
        :param key: String key to the entry in the JSON file
        :param key2: String key to the entry in the JSON file.
        :param data: Data to replace old value with.
        """
        try:
            self.config[key][key2] = data
        except (KeyError, TypeError):
            self.config[key] = {}
            self.config[key][key2] = data
        try:
            with open(self.json_file, mode='w') as file:
                file.write(json.dumps(self.config, indent=4, sort_keys=True))
        except(OSError, IOError):
            pass


def plugintextreader(file=None):
    """
    Obtains data from plugin json files
    that contains text for commands.
    """
    json_file = os.path.join(
        sys.path[0], 'resources', 'ConfigData', 'plugins',
        file)
    try:
        with open(json_file) as fileobj:
            return json.load(fileobj)
    except(OSError, IOError):
        pass
    return None


def pluginconfigreader(file=None):
    """
    Obtains data from plugin json files
    that contains config for commands.
    """
    jsonfile = os.path.join(
        sys.path[0], 'resources', 'ConfigData',
        file)
    try:
        with open(jsonfile) as fileobje:
            return json.load(fileobje)
    except(OSError, IOError):
        pass
    return None


PluginConfigReader = pluginconfigreader
PluginTextReader = plugintextreader


class BotCredentialsVars(BaseCredentialsReader):
    """
    Class for getting the Credentials.json config Values.
    """
    def __init__(self):
        super(BotCredentialsVars, self).__init__(file='Credentials.json')

        # defaults.
        self.logging = False  # bool
        self.logbans = False  # bool
        self.logunbans = False  # bool
        self.logkicks = False  # bool
        self.log_games = False  # bool
        self.discord_logger = False  # bool
        self.asyncio_logger = False  # bool
        self.log_available = False  # bool
        self.log_unavailable = False  # bool
        self.log_channel_create = False  # bool
        self.is_official_bot = False  # bool
        self.log_ytdl = False  # bool
        self.pm_commands_list = False  # bool
        self.log_channel_delete = False  # bool
        self.log_channel_update = False  # bool
        self.log_member_update = False  # bool
        self.log_server_join = False  # bool
        self.log_server_remove = False  # bool
        self.log_server_update = False  # bool
        self.log_server_role_create = False  # bool
        self.log_server_role_delete = False  # bool
        self.log_server_role_update = False  # bool
        self.log_group_join = False  # bool
        self.log_group_remove = False  # bool
        self.log_error = False  # bool
        self.log_voice_state_update = False  # bool
        self.log_typing = False  # bool
        self.log_socket_raw_receive = False  # bool
        self.log_socket_raw_send = False  # bool
        self.log_resumed = False  # bool
        self.log_member_join = False  # bool
        self.pm_command_errors = False  # bool
        self.enable_error_handler = False  # bool
        self.bot_prefix = ''  # string
        self.discord_user_id = ''  # string
        self.bot_token = ''  # string
        self.disable_voice_commands = False  # bool
        self.language = 'en'  # string
        self.description = ''  # string
        self.log_server_emojis_update = False  # bool
        self.log_reaction_add = False  # bool
        self.log_reaction_remove = False  # bool
        self.log_reaction_clear = False  # bool
        self.shards = 0  # int
        self.run_on_shard = 0  # int
        self.twitch_url = ''  # string
        self.youtube_url = ''  # string
        self.default_plugins = []  # list
        self.api_token = ''  # string

        # populate the values from Credentials.json.
        self.set_values()

    def set_values(self):
        """
        sets values of the variables.
        """
        try:
            self.logging = self.getconfig(
                'logging')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.logbans = self.getconfig(
                'logbans')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.logunbans = self.getconfig(
                'logunbans')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.logkicks = self.getconfig(
                'logkicks')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_games = self.getconfig(
                'loggames')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.discord_logger = self.getconfig(
                'discord_py_logger')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.asyncio_logger = self.getconfig(
                'asyncio_logger')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_available = self.getconfig(
                'LogServerAvailable')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_unavailable = self.getconfig(
                'LogServerUnavailable')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_channel_create = self.getconfig(
                'log_channel_create')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.is_official_bot = self.getconfig(
                'Is_Official_Bot_Account')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_ytdl = self.getconfig(
                'ytdl_logs')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.pm_commands_list = self.getconfig(
                'PM_Commands')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_channel_delete = self.getconfig(
                'log_channel_delete')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_channel_update = self.getconfig(
                'log_channel_update')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_member_update = self.getconfig(
                'log_member_update')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_server_join = self.getconfig(
                'log_server_join')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_server_remove = self.getconfig(
                'log_server_remove')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_server_update = self.getconfig(
                'log_server_update')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_server_role_create = self.getconfig(
                'log_server_role_create')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_server_role_delete = self.getconfig(
                'log_server_role_delete')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_server_role_update = self.getconfig(
                'log_server_role_update')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_group_join = self.getconfig(
                'log_group_join')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_group_remove = self.getconfig(
                'log_group_remove')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_error = self.getconfig(
                'log_error')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_voice_state_update = self.getconfig(
                'log_voice_state_update')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_typing = self.getconfig(
                'log_typing')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_socket_raw_receive = self.getconfig(
                'log_socket_raw_receive')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_socket_raw_send = self.getconfig(
                'log_socket_raw_send')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_resumed = self.getconfig(
                'log_resumed')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_member_join = self.getconfig(
                'log_member_join')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.pm_command_errors = self.getconfig(
                'pm_command_errors')  # bool
        except (KeyError, TypeError):
            pass
        self.enable_error_handler = (
            True if not self.pm_command_errors else False)  # bool
        try:
            self.bot_prefix = self.getconfig(
                'bot_prefix')  # string
        except (KeyError, TypeError):
            pass
        try:
            self.discord_user_id = self.getconfig(
                'ownerid')  # string
        except (KeyError, TypeError):
            pass
        try:
            self.bot_token = self.getconfig(
                'token')  # string
        except (KeyError, TypeError):
            pass
        try:
            self.disable_voice_commands = self.getconfig(
                'disable_voice')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.language = self.getconfig(
                'language')  # string
        except (KeyError, TypeError):
            pass
        try:
            self.description = self.getconfig(
                'description')  # string
        except (KeyError, TypeError):
            pass
        try:
            self.log_server_emojis_update = self.getconfig(
                'log_server_emojis_update')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_reaction_add = self.getconfig(
                'log_reaction_add')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_reaction_remove = self.getconfig(
                'log_reaction_remove')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.log_reaction_clear = self.getconfig(
                'log_reaction_clear')  # bool
        except (KeyError, TypeError):
            pass
        try:
            self.shards = self.getconfig(
                'shards')  # int
        except (KeyError, TypeError):
            pass
        try:
            self.run_on_shard = self.getconfig(
                'run_on_shard')  # int
        except (KeyError, TypeError):
            pass
        try:
            self.twitch_url = self.getconfig(
                'twitch_url')  # string
        except (KeyError, TypeError):
            pass
        try:
            self.youtube_url = self.getconfig(
                'youtube_url')  # string
        except (KeyError, TypeError):
            pass
        try:
            self.default_plugins = self.getconfig(
                'default_plugins')  # dict
        except (KeyError, TypeError):
            pass
        try:
            self.api_token = self.getconfig(
                'api_token')  # string
        except (KeyError, TypeError):
            pass
