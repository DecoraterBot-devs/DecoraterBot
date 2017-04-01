Used Discord.py Events in DecoraterBot
======================================

Here is a list of the Discortd.py Events that are used as well as what
they are used for. Note: Events that use Optional Logs are Controlled by
``\\resources\\ConfigData\\Credentials.json``

Documentation on Setting it up is **not** Complete.

+---------------+------------------------------------------------------------+
| Event         | Usage                                                      |
+===============+============================================================+
| ``on_message` | Commands. This is how the Bot Actually Responds to the     |
| `             | commands. Also has Built in Error Handler for this Event.  |
|               | Also has optional logs.                                    |
+---------------+------------------------------------------------------------+
| ``on_message_ | Optional Logs & Built in Error Handler.                    |
| delete``      |                                                            |
+---------------+------------------------------------------------------------+
| ``on_message_ | Optional Logs & Built in Error Handler.                    |
| edit``        |                                                            |
+---------------+------------------------------------------------------------+
| ``on_channel_ | Optional Logs (Not Done yet)                               |
| delete``      |                                                            |
+---------------+------------------------------------------------------------+
| ``on_channel_ | Optional Logs (Not Done yet)                               |
| create``      |                                                            |
+---------------+------------------------------------------------------------+
| ``on_channel_ | Optional Logs (Not Done yet)                               |
| update``      |                                                            |
+---------------+------------------------------------------------------------+
| ``on_member_b | Optional Logs & Cheese.lab verifications (removing users   |
| an``          | from verify cache list)                                    |
+---------------+------------------------------------------------------------+
| ``on_member_u | Optional Logs & Built in Error Handler.                    |
| nban``        |                                                            |
+---------------+------------------------------------------------------------+
| ``on_member_r | Optional Logs & Cheese.lab verifications (removing users   |
| emove``       | from verify cache list)                                    |
+---------------+------------------------------------------------------------+
| ``on_member_u | Optional Logs (Not Done yet)                               |
| pdate``       |                                                            |
+---------------+------------------------------------------------------------+
| ``on_member_j | Optional Logs (Not Done yet) & Cheese.lab verification     |
| oin``         | stuff.                                                     |
+---------------+------------------------------------------------------------+
| ``on_server_a | Optional Logs (Not Done yet)                               |
| vailable``    |                                                            |
+---------------+------------------------------------------------------------+
| ``on_server_u | Optional Logs (Not Done yet)                               |
| navailable``  |                                                            |
+---------------+------------------------------------------------------------+
| ``on_server_j | Optional Logs (Not Done yet)                               |
| oin``         |                                                            |
+---------------+------------------------------------------------------------+
| ``on_server_r | Optional Logs (Not Done yet)                               |
| emove``       |                                                            |
+---------------+------------------------------------------------------------+
| ``on_server_u | Optional Logs (Not Done yet)                               |
| pdate``       |                                                            |
+---------------+------------------------------------------------------------+
| ``on_server_r | Optional Logs (Not Done yet)                               |
| ole_create``  |                                                            |
+---------------+------------------------------------------------------------+
| ``on_server_r | Optional Logs (Not Done yet)                               |
| ole_delete``  |                                                            |
+---------------+------------------------------------------------------------+
| ``on_server_r | Optional Logs (Not Done yet)                               |
| ole_update``  |                                                            |
+---------------+------------------------------------------------------------+
| ``on_group_jo | Optional Logs (Not Done yet)                               |
| in``          |                                                            |
+---------------+------------------------------------------------------------+
| ``on_group_re | Optional Logs (Not Done yet)                               |
| move``        |                                                            |
+---------------+------------------------------------------------------------+
| ``on_error``  | Optional Logs (Not Done yet)                               |
+---------------+------------------------------------------------------------+
| ``on_voice_st | Optional Logs (Not Done yet)                               |
| ate_update``  |                                                            |
+---------------+------------------------------------------------------------+
| ``on_typing`` | Optional Logs (Not Done yet)                               |
+---------------+------------------------------------------------------------+
| ``on_socket_r | Optional Logs (Not Done yet)                               |
| aw_receive``  |                                                            |
+---------------+------------------------------------------------------------+
| ``on_socket_r | Optional Logs (Not Done yet)                               |
| aw_send``     |                                                            |
+---------------+------------------------------------------------------------+
| ``on_ready``  | Bot Status messages on 2 Servers & Initial Streaming       |
|               | Status saying to ``type ::commands for info``.             |
+---------------+------------------------------------------------------------+
| ``on_resumed` | Optional Logs (Not Done yet)                               |
| `             |                                                            |
+---------------+------------------------------------------------------------+
| ``on_server_e | Optional Logs (Not Done yet)                               |
| mojis_update` |                                                            |
| `             |                                                            |
+---------------+------------------------------------------------------------+
| ``on_reaction | Optional Logs (Not Done yet)                               |
| _add``        |                                                            |
+---------------+------------------------------------------------------------+
| ``on_reaction | Optional Logs (Not Done yet)                               |
| _remove``     |                                                            |
+---------------+------------------------------------------------------------+
| ``on_reaction | Optional Logs (Not Done yet)                               |
| _clear``      |                                                            |
+---------------+------------------------------------------------------------+
