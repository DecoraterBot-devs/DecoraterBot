# Bot Commands for DecoraterBot

Commands are usually using the `::` prefix.

``::kill <optionally mention someone>`` - Kills someone you mention and randomly generates a kill message. Can onso use the Command and not mention someone as well. (Works in PM and servers)

``::changelog`` - Bot information and command changes. (Works in PM and servers)

``::raid <optionally mention where>`` - Raids a person or place you mention.

``::source`` - Shows GitHub Repositories. (Works in PM and servers)

``::prune <number of messages to remove>`` - Prune a specific number of messages. Max is 100 due to Ratelimits. (Servers only)

``::game <'string here'> | type=<1 for Twitch or 2 for Youtube (Soon™)>`` - Changes game status. (Works in PM and servers)

``::debug`` - Debugs Python Code. (Bot owner only) (Works in PM and servers)

``::eval`` - Evaluates Python Code without Subproccessing the Python Interpreter. (Bot owner only) (Works in PM and servers)

``::color ::pink/::brown <role name here>`` - Changes the Colors of a Role. (Was Originally a Testing Command) (Servers only)

``::meme <picture (required)> | <top text (required)> | <bottom text (required)>`` - Gives a meme with the text you provide. meme picture list can be found here. (BooBot's but it works for this too.) http://pastebin.com/gCL2jMEL. You can also do things like ``::meme [mention someone here] | [top text] | [bottom text]``

``::remgame`` - Removes any game from the bot's status.

``::join <invite url or code>`` - For Joining Servers, However with Official API it does not work so that is why Credentials has a ``True`` and a ``False`` Option for if it is a bot account or not. If it is set to ``True`` it will send you a url to validate it to join the server via oauth.

# TODO: Link to Oauth on the word above.

``::update`` - Command that says that the bot has updated. Probably should remove this due to spamming of it is possible?

``::say <whatever you want here>`` - makes the bot Say whatever you want. Note: You cannot have ``::`` in this nor any Mentions to prevent any abuse of the API.

``::type`` - Makes the bot send a ``typing`` status to the channel the command was sent from.

``::uptime`` Makes the bot Reply withh the uptime of the bot's process. (Not Nessisarrily how long it is online due to possible Websocket closures).

``::reload`` - Allows the bot to Reload it's commands / Logs module(s). (Bot owner only)

``::hlreload`` - Aloows the bot to Do a High level Reload of  the Bot's Code without having to restart it. (Does not work with very big and breaking Changes like Changes to Discord.py itself) (Bot owner only)

``::pyversion`` - Makes the bot Reply with the Version of the Python Interpreter used as well as the bits of it. (32 or 64 bit versions)

``::Libs`` - Makkes the bot Reply with the Libraries used. (Not Currently up to date)

``::userinfo <mention user (optional if you want to see your own info)>`` - Shows your or the person you mentioned user information.

::kick <mention person here>
::ban <mention person here>
::softban <mention person here>
::clear (Clears all messages from bot within a 100 message limit.)
::ignorechannel
::unignorechannel

``::as`` - changes bot's avatar to Asura's image.

``::rs`` - changes bot's avatar to Rune Slayer's image.

``::ai``  - changes bot's avatar to Aisha's base image.

``::tinyurl <URL to shorten here>`` - Makes the bot shorten the URL Provided. (Supports ``<`` and ``>`` between the URL to excape embedding of it with oembed)

# Voice Channel Commands

``::JoinVoiceChannel`` - Allows the bot to Join a Voice Channel. (You must be in a Voice Channel foor it to work)

``::play <youtube url here>`` - URL or Serch Term for a video to Play. Note: Playlist does not support Searching yet. If you have a idea on the Commands extention in Discord.py that can help me with the playlist let me know.

``::pause`` - Pauses any playing Youtube Video/Audio/Music.

``::unpause`` - Resumes any paused Youtube Video/Audio/Music.

``::stop`` - Stops any playing Youtube Video/Audio/Music.

``::move`` - Moves the bot to a Voice Channel that you are in or moved to yourself.

``::LeaveVoiceChannel`` - Makes the bot leave the Voice Channel it is in.

``::Playlist`` - Shows the current Playlist entries. (Has some bugs in it)

``::vol (int value somewhere between 0~200)`` - Sets the Volume of the playing Youtube Video/Audio/Music.

