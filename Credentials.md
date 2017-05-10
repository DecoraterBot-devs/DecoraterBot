### Setting Credentials.json

After copying ``Credentials_example.json`` to ``Credentials.json`` you can set these values:

|   	| Credentials.json values	|
|:------:	|:-:	|
| ``email``	| Sets the email to use for the bot (This makes the bot log into a normal discord account)(deprecated). Type: ``string``	|
| ``password``	| Sets the password to use for the bot (This makes the bot log into a normal discord account)(deprecated). Type: ``string``	|
| ``language``	| Sets the language to use for the bot. Type: ``string``	|
| ``token``	| Sets the token to use for the bot (This can make the bot also able to login to a normal discord account). Type: ``string``	|
| ``logging``	| (optional) Logs messages to a file. Type: ``bool``	|
| ``logbans``	| (optional) Logs bans to a file. Type: ``bool``	|
| ``logunbans``	| (optional) Logs unbans to a file. Type: ``bool``	|
| ``loggames``	| (optional) Logs games that was changed on the bot to a file. Type: ``bool``	|
| ``logkicks``	| (optional) Logs kicks to a file. Type: ``bool``	|
| ``LogServerAvailable``	| (optional) Logs available servers to a file. Type: ``bool``	|
| ``LogServerUnavailable``	| (optional) Logs unavailable servers to a file. Type: ``bool``	|
| ``discord_py_logger``	| (optional) Logs discord.py related stuff to a file. Type: ``bool``	|
| ``asyncio_logger``	| (optional) Logs asyncio related stuff to a file. Type: ``bool``	|
| ``Is_Official_Bot_Account``	| (Required) Sets if the bot is an normal account or an 'bot' account. Type: ``bool``	|
| ``PM_Commands``	| (Optional) Sets if the bot should PM the commands or send them in the channel the command was sent in in the case of it being the server. Type: ``bool``	|
| ``ownerid``	| (Required) The ID of the bot's owner. Type: ``string``	|
| ``bot_prefix``	| (Required) The prefix to use for the bot. Type: ``string``	|
| ``disable_voice``	| (Optional) Disable Voice Channel commands. Type: ``bool``	|
| ``pm_command_errors``	| (Optional) Sets if you want the bot to PM you command tracebacks or not. Type: ``bool``	|
| ``ytdl_logs``	| (Optional) Logs youtube_dl logs to a file. Type: ``bool``	|
| ``log_channel_create``	| ... Type: ``bool``	|
| ``log_channel_delete``	| ... Type: ``bool``	|
| ``log_channel_update``	| ... Type: ``bool``	|
| ``log_member_update``	| ... Type: ``bool``	|
| ``log_server_join``	| ... Type: ``bool``	|
| ``log_server_remove``	| ... Type: ``bool``	|
| ``log_server_update``	| ... Type: ``bool``	|
| ``log_server_role_create``	| ... Type: ``bool``	|
| ``log_server_role_delete``	| ... Type: ``bool``	|
| ``log_server_role_update``	| ... Type: ``bool``	|
| ``log_group_join``	| ... Type: ``bool``	|
| ``log_group_remove``	| ... Type: ``bool``	|
| ``log_error``	| ... Type: ``bool``	|
| ``log_voice_state_update``	| ... Type: ``bool``	|
| ``log_typing``	| ... Type: ``bool``	|
| ``log_socket_raw_receive``	| ... Type: ``bool``	|
| ``log_socket_raw_send``	| ... Type: ``bool``	|
| ``log_resumed``	| ... Type: ``bool``	|
| ``log_member_join``	| ... Type: ``bool``	|
| ``log_server_emojis_update``	| ... Type: ``bool``	|
| ``log_reaction_add``	| ... Type: ``bool``	|
| ``log_reaction_remove``	| ... Type: ``bool``	|
| ``log_reaction_clear``	| ... Type: ``bool``	|
| ``shards``	| (Optional) The number of shards to use with the bot. Type: ``int``	|
| ``run_on_shard``	| (Optional) The shard id to run the bot on (I am not sure yet if this has to always be shard 0 or 1). Type: ``int``	|
| ``description``	| (Required) The bot's description. Type: ``string``	|
| ``twitch_url``	| (Required) The bot's twitch stream url (This channel/stream to twitch does not have to exist). Type: ``string``	|
| ``youtube_url``	| (Optional) The bot's youtube stream url (This channel/stream to youtube does not have to exist). Type: ``string``	|
| ``redis_url``	| ... Type: ``string``	|
| ``mongo_url``	| ... Type: ``string``	|
| ``dd_agent_url``	| ... Type: ``string``	|
| ``sentry_dsn``	| ... Type: ``string``	|
| ``default_plugins``	| Default plugins the bot loads. Type: ``dict``	|

