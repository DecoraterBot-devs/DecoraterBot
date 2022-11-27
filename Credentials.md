### Setting Credentials.json

After copying ``Credentials_example.json`` to ``Credentials.json`` you can set these values:

|   	| Credentials.json values	|
|:------:	|:-:	|
| ``language``	| Sets the language to use for the bot. Type: ``string``	|
| ``token``	| Sets the token to use for the bot. Type: ``string``	|
| ``discord_py_logger``	| (optional) Logs discord.py related stuff to a file. Type: ``bool``	|
| ``asyncio_logger``	| (optional) Logs asyncio related stuff to a file. Type: ``bool``	|
| ``Is_Official_Bot_Account``	| (Required) Sets if the bot is a normal account or an 'bot' account. Type: ``bool``	|
| ``ownerid``	| (Required) The ID of the bot's owner. Type: ``string``	|
| ``bot_prefix``	| (Optional) The prefix to use for the bot. Type: ``string``	|
| ``disable_voice``	| (Optional) Disable Voice Channel commands. Type: ``bool``	|
| ``pm_command_errors``	| (Optional) Sets if you want the bot to PM you command tracebacks or not. Type: ``bool``	|
| ``log_error``	| (Optional) Logs bot errors. Type: ``bool``	|
| ``description``	| (Required) The bot's description. Type: ``string``	|
| ``twitch_url``	| (Required) The bot's twitch stream url (This channel/stream to twitch does not have to exist). Type: ``string``	|
| ``youtube_url``	| (Optional) The bot's YouTube stream url (This channel/stream to YouTube does not have to exist). Type: ``string``	|
| ``default_plugins``	| (Required) Default plugins the bot loads. Type: ``dict``	|

