# Bot Commands for DecoraterBot

Commands are usually using the `::` prefix.

|   	| Text Channel Commands	|
|:------:	|:-:	|
| ``::kill <optionally mention someone>``	| Kills someone you mention and randomly generates a kill message. Can onso use the Command and not mention someone as well. (Works in PM and servers)	|
| ``::changelog``	| Bot information and command changes. (Works in PM and servers)	|
| ``::raid <optionally mention where>``	| Raids a person or place you mention.	|
| ``::source``	| Shows GitHub Repositories. (Works in PM and servers)	|
| ``::prune <number of messages to remove>``	| Prune a specific number of messages. Max is 100 due to Ratelimits. (Servers only)	|
| ``::game <'string here'> | type=<1 for Twitch or 2 for Youtube (Soon™)>``	| Changes game status. (Works in PM and servers)	|
| ``::debug``	| Debugs Python Code. (Bot owner only) (Works in PM and servers)	|
| ``::eval``	| Evaluates Python Code without Subproccessing the Python Interpreter. (Bot owner only) (Works in PM and servers)	|
| ``::color ::pink/::brown <role name here>``	| Changes the Colors of a Role. (Was Originally a Testing Command) (Servers only)	|
| ``::meme <picture (required)> | <top text (required)> | <bottom text (required)>``	| Gives a meme with the text you provide. meme picture list can be found [here](http://pastebin.com/gCL2jMEL). (BooBot's but it works for this too) You can also do things like ``::meme [mention someone here] | [top text] | [bottom text]``	|
| ``::remgame``	| Removes any game from the bot's status.	|
| ``::join <invite url or code>``	| For Joining Servers, However with Official API it does not work so that is why Credentials has a ``True`` and a ``False`` Option for if it is a bot account or not. If it is set to ``True`` it will send you a url to validate it to join the server via [OAuth2](http://oauth.net/2/).	|
| ``::update``	| Command that says that the bot has updated. Probably should remove this due to spamming of it is possible?	|
| ``::say <whatever you want here>``	| Makes the bot Say whatever you want. Note: You cannot have ``::`` in this nor any Mentions to prevent any abuse of the API.	|
| ``::type``	| Makes the bot send a ``typing`` status to the channel the command was sent from.	|
| ``::uptime``	| Makes the bot Reply withh the uptime of the bot's process. (Not Nessisarrily how long it is online due to possible Websocket closures).	|
| ``::reload``	| Allows the bot to Reload it's commands / Logs module(s). (Bot owner only)	|
| ``::loadplugin`` | Allows loading of bot plugins. (Bot owner only) |
| ``::unloadplugin`` | Allows unloading of bot plugins. (Bot owner only) |
| ``::reloadplugin`` | Allows reloading of bot plugins. (Bot owner only) |
| ``::pyversion``	| Makes the bot Reply with the Version of the Python Interpreter used as well as the bits of it. (32 or 64 bit versions)	|
| ``::Libs``	| Makes the bot Reply with the Libraries used. (Not Currently up to date)	|
| ``::userinfo <mention user (optional if you want to see your own info)>``	| Shows your or the person you mentioned user information.	|
| ``::kick <mention person here>``	| Kicks the User mentioned. (Bug in it if the bot has no permissions to kick or if the user has a higher rank than the bot that it sends 2 messages)	|
| ``::ban <mention person here>``	| Bans the User mentioned. (Bug in it if the bot has no permissions to ban or if the user has a higher rank than the bot that it sends 2 messages)	|
| ``::softban <mention person here>``	| Bans and then Immediately Unbans the user mentioned. (This Essenctially is a kick that prunes messages)	|
| ``::warn <mention(s)> <reason>`` | Warns a user or user(s) mentioend for a particular reason provided. (Does not work yet) |
| ``::mute <mention>`` | Mutes an user mentioned for a certain amount of time. Requires a role named ``Muted`` to work. (Does not work yet) |
| ``::clear``	| Clears all messages from bot within a 100 message limit.	|
| ``::ignorechannel``	| Ignores the channel that this command was sent from.	|
| ``::unignorechannel``	| Allows the bot to listen to commands from a Ignored Channel and Remvoes it from the ``Ignore`` List.	|
| ``::as``	| Changes bot's avatar to Asura's image.	|
| ``::rs``	| Changes bot's avatar to Rune Slayer's image.	|
| ``::ai``	| Changes bot's avatar to Aisha's base image.	|
| ``::lk``	| Changes bot's avatar to Lord Knight's image.	|
| ``::vp``	| Changes bot's avatar to Void Princess's image.	|
| ``::ws``	| Changes bot's avatar to Wind Sneeker's image.	|
| ``::tinyurl <URL to shorten here>``	| Makes the bot shorten the URL Provided. (Supports ``<`` and ``>`` between the URL to excape embedding of it with [oEmbed](http://oembed.com/))	|

*The commands below are from plugins. They might be moved to an documentation file in another GitHub or BitBucket repository or branch depending on what we decide to place plugins that are not loaded on bot's startup by default. From now on all new bot commands are going to be added via plugins so they should be optional to install. (excluding the commands to be able to install plugins. Those would have to go into the main commands core file that contains the reloading functionality of normal commands and able to load, unload, and reload plugins.)*

|   	| Text Channel Commands (Plugins)	|
|:---------------:	|:--------------------------------------------------------------------------------------------------------------:	|
| ``::givecreds``	| Gives the Bot's Owner Daily Credits even if the Tatsumaki bot is present in the server this command is sent from.	|

View the list of Voice Channel Commands [here](/VoiceCommands.md).
