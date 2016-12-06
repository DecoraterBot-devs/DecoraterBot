# Used Discord.py Events in DecoraterBot

Here is a list of the Discortd.py Events that are used as well as what they are used for.
Note: Events that use Optional Logs are Controlled by ``\\resources\\ConfigData\\Credentials.json``

Documentation on Setting it up is **not** Complete.

| Event	| Usage	|
|:------:	|:-:	|
| ``on_message``	| Commands. This is how the Bot Actually Responds to the commands. Also has Built in Error Handler for this Event. Also has optional logs.	|
| ``on_message_delete``	| Optional Logs & Built in Error Handler.	|
| ``on_message_edit``	| Optional Logs & Built in Error Handler.	|
| ``on_channel_delete``	| Optional Logs (Not Done yet)	|
| ``on_channel_create``	| Optional Logs (Not Done yet)	|
| ``on_channel_update``	| Optional Logs (Not Done yet)	|
| ``on_member_ban``	| Optional Logs & Cheese.lab verifications (removing users from verify cache list)	|
| ``on_member_unban``	| Optional Logs & Built in Error Handler.	|
| ``on_member_remove``	| Optional Logs & Cheese.lab verifications (removing users from verify cache list)	|
| ``on_member_update``	| Optional Logs (Not Done yet)	|
| ``on_member_join``	| Optional Logs (Not Done yet) & Cheese.lab verification stuff.	|
| ``on_server_available``	| Optional Logs (Not Done yet)	|
| ``on_server_unavailable``	| Optional Logs (Not Done yet)	|
| ``on_server_join``	| Optional Logs (Not Done yet)	|
| ``on_server_remove``	| Optional Logs (Not Done yet)	|
| ``on_server_update``	| Optional Logs (Not Done yet)	|
| ``on_server_role_create``	| Optional Logs (Not Done yet)	|
| ``on_server_role_delete``	| Optional Logs (Not Done yet)	|
| ``on_server_role_update``	| Optional Logs (Not Done yet)	|
| ``on_group_join``	| Optional Logs (Not Done yet)	|
| ``on_group_remove``	| Optional Logs (Not Done yet)	|
| ``on_error``	| Optional Logs (Not Done yet)	|
| ``on_voice_state_update``	| Optional Logs (Not Done yet)	|
| ``on_typing``	| Optional Logs (Not Done yet)	|
| ``on_socket_raw_receive``	| Optional Logs (Not Done yet)	|
| ``on_socket_raw_send``	| Optional Logs (Not Done yet)	|
| ``on_ready``	| Bot Status messages on 2 Servers & Initial Streaming Status saying to ``type ::commands for info``.	|
| ``on_resumed``	| Optional Logs (Not Done yet)	|
| ``on_server_emojis_update``	| Optional Logs (Not Done yet)	|
| ``on_reaction_add``	| Optional Logs (Not Done yet)	|
| ``on_reaction_remove``	| Optional Logs (Not Done yet)	|
| ``on_reaction_clear``	| Optional Logs (Not Done yet)	|
