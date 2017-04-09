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


__all__ = ['BotCredentialsVars', 'CreditsReader', 'PluginTextReader']


class __BaseCredentialsReader(object):
    """
    Base config Class.
    """
    def __init__(self, file=None):
        self.__credentials = []
        self.filename = file
        self.json_file = None
        self.__load()

    def __load(self):
        """
        Loads the JSON config Data.
        :return: List.
        """
        sepa = os.sep
        path = sys.path[0]
        self.json_file = '{0}{1}resources{1}ConfigData{1}{2}'.format(
            path, sepa, self.filename)
        try:
            with open(self.json_file) as file:
                self.__credentials = json.load(file)
        except(OSError, IOError):
            pass

    def getconfig(self, key):
        """
        Gets a Credentials Config Value basted on the key provided.
        :param key: String key to the entry in Credentials.json
        :return: JSON config Value.
        """
        return self.__credentials[key]


class BaseConfigReader(object):
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
        sepa = os.sep
        path = sys.path[0]
        self.json_file = '{0}{1}resources{1}ConfigData{1}{2}'.format(
            path, sepa, self.filename)
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


class CreditsReader(object):
    """Obtains Data from credits.json"""
    def __init__(self, file=None):
        self.config = []
        self.filename = file
        self.json_file = None
        self.load()

    def load(self):
        """
        Loads the JSON config Data.
        :return: List.
        """
        sepa = os.sep
        path = sys.path[0]
        self.json_file = '{0}{1}resources{1}ConfigData{1}{2}'.format(
            path, sepa, self.filename)
        try:
            with open(self.json_file) as file:
                self.config = json.load(file)
        except(OSError, IOError):
            pass

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
    json_file = '{0}{1}resources{1}ConfigData{1}plugins{1}{2}'.format(
        sys.path[0], os.sep, file)
    try:
        with open(json_file) as fileobj:
            return json.load(fileobj)
    except(OSError, IOError):
        pass
    return None


PluginTextReader = plugintextreader


class BotCredentialsVars(__BaseCredentialsReader):
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
        self.discord_user_email = ''  # string
        self.discord_user_password = ''  # string
        self.bot_token = ''  # string
        self.disable_voice_commands = False  # bool
        self.language = 'en'  # string
        self.description = ''  # string
        self.log_server_emojis_update = False  # bool
        self.log_reaction_add = False  # bool
        self.log_reaction_remove = False  # bool
        self.log_reaction_clear = False  # bool
        self.shards = 0  # int
        self.twitch_url = ''  # string
        self.youtube_url = ''  # string
        self.redis_url = ''  # string
        self.mongo_url = ''  # string
        self.dd_agent_url = ''  # string
        self.sentry_dsn = ''  # string

        # Properties.
        self.logging = self.getconfig(
            'logging')  # bool
        self.logbans = self.getconfig(
            'logbans')  # bool
        self.logunbans = self.getconfig(
            'logunbans')  # bool
        self.logkicks = self.getconfig(
            'logkicks')  # bool
        self.log_games = self.getconfig(
            'loggames')  # bool
        self.discord_logger = self.getconfig(
            'discord_py_logger')  # bool
        self.asyncio_logger = self.getconfig(
            'asyncio_logger')  # bool
        self.log_available = self.getconfig(
            'LogServerAvailable')  # bool
        self.log_unavailable = self.getconfig(
            'LogServerUnavailable')  # bool
        self.log_channel_create = self.getconfig(
            'log_channel_create')  # bool
        self.is_official_bot = self.getconfig(
            'Is_Official_Bot_Account')  # bool
        self.log_ytdl = self.getconfig(
            'ytdl_logs')  # bool
        self.pm_commands_list = self.getconfig(
            'PM_Commands')  # bool
        self.log_channel_delete = self.getconfig(
            'log_channel_delete')  # bool
        self.log_channel_update = self.getconfig(
            'log_channel_update')  # bool
        self.log_member_update = self.getconfig(
            'log_member_update')  # bool
        self.log_server_join = self.getconfig(
            'log_server_join')  # bool
        self.log_server_remove = self.getconfig(
            'log_server_remove')  # bool
        self.log_server_update = self.getconfig(
            'log_server_update')  # bool
        self.log_server_role_create = self.getconfig(
            'log_server_role_create')  # bool
        self.log_server_role_delete = self.getconfig(
            'log_server_role_delete')  # bool
        self.log_server_role_update = self.getconfig(
            'log_server_role_update')  # bool
        self.log_group_join = self.getconfig(
            'log_group_join')  # bool
        self.log_group_remove = self.getconfig(
            'log_group_remove')  # bool
        self.log_error = self.getconfig(
            'log_error')  # bool
        self.log_voice_state_update = self.getconfig(
            'log_voice_state_update')  # bool
        self.log_typing = self.getconfig(
            'log_typing')  # bool
        self.log_socket_raw_receive = self.getconfig(
            'log_socket_raw_receive')  # bool
        self.log_socket_raw_send = self.getconfig(
            'log_socket_raw_send')  # bool
        self.log_resumed = self.getconfig(
            'log_resumed')  # bool
        self.log_member_join = self.getconfig(
            'log_member_join')  # bool
        self.pm_command_errors = self.getconfig(
            'pm_command_errors')  # bool
        self.enable_error_handler = (
            True if not self.pm_command_errors else False)  # bool
        self.bot_prefix = self.getconfig(
            'bot_prefix')  # string
        self.discord_user_id = self.getconfig(
            'ownerid')  # string
        self.discord_user_email = self.getconfig(
            'email')  # string
        self.discord_user_password = self.getconfig(
            'password')  # string
        self.bot_token = self.getconfig(
            'token')  # string
        self.disable_voice_commands = self.getconfig(
            'disable_voice')  # bool
        self.language = self.getconfig(
            'language')  # string
        self.description = self.getconfig(
            'description')  # string
        self.log_server_emojis_update = self.getconfig(
            'log_server_emojis_update')  # bool
        self.log_reaction_add = self.getconfig(
            'log_reaction_add')  # bool
        self.log_reaction_remove = self.getconfig(
            'log_reaction_remove')  # bool
        self.log_reaction_clear = self.getconfig(
            'log_reaction_clear')  # bool
        self.shards = self.getconfig(
            'shards')  # int
        self.twitch_url = self.getconfig(
            'twitch_url')  # string
        self.youtube_url = self.getconfig(
            'youtube_url')  # string
        self.redis_url = self.getconfig(
            'redis_url')  # string
        self.mongo_url = self.getconfig(
            'mongo_url')  # string
        self.dd_agent_url = self.getconfig(
            'dd_agent_url')  # string
        self.sentry_dsn = self.getconfig(
            'sentry_dsn')  # string

        # checks
        if self.discord_user_email == 'None':
            self.discord_user_email = None
        if self.discord_user_password == 'None':
            self.discord_user_password = None
        if self.bot_token == 'None':
            self.bot_token = None
        if self.discord_user_id == 'None':
            self.discord_user_id = None
