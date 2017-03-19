# coding=utf-8
"""
Logs plugin for DecoraterBot.

This is the default logger for DecoraterBot.
"""
import traceback
import json
import re

import discord

from .. import BotErrors


class BotLogger:
    """
    Logging Plugin Class.
    """
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, exception, context):
        """..."""
        await self.bot.send_message(
            context.message.channel,
            "exception in command {0}:```py\n{1}```".format(
                context.command, str(exception)))

    async def on_message(self, message):
        """
        Bot Event.
        :param message: Messages.
        :return: Nothing.
        """
        if self.bot.user.mention in message.content:
            await self.bot.bot_mentioned_helper(message)
        # if len(message.mentions) > 5:
        #    await self.bot.mention_ban_helper(message)
        if not message.channel.is_private:
            try:
                if message.channel.server and message.channel.server.id == \
                        "81812480254291968":
                    if message.author.id == self.bot.user.id:
                        return
                    elif message.channel.id == "153055192873566208":
                        pass
                    elif message.channel.id == "87382611688689664":
                        pass
                    else:
                        if self.bot.BotConfig.logging:
                            await self.bot.DBLogs.send_logs(self.bot, message)
                elif message.channel.server and message.channel.server.id == \
                        "71324306319093760":
                    if message.channel.id == '141489876200718336':
                        if self.bot.logging:
                            self.bot.DBLogs.logs(message)
                        await self.bot.cheesy_commands_helper(message)
                    else:
                        # await self.bot.everyone_mention_logger(message)
                        if self.bot.BotConfig.logging:
                            self.bot.DBLogs.logs(message)
                else:
                    if self.bot.BotConfig.logging:
                        self.bot.DBLogs.logs(message)
            except Exception as e:
                if self.bot.BotConfig.pm_command_errors:
                    if self.bot.BotConfig.discord_user_id is not None:
                        owner = self.bot.BotConfig.discord_user_id
                        exception_data2 = str(traceback.format_exc())
                        message_data = '```py\n{0}\n```'.format(
                            exception_data2)
                        try:
                            await self.bot.send_message(discord.User(id=owner),
                                                        content=message_data)
                        except discord.errors.Forbidden:
                            pass
                        except discord.errors.HTTPException:
                            funcname = 'on_message'
                            tbinfo = str(traceback.format_exc())
                            await self.bot.DBLogs.on_bot_error(funcname,
                                                               tbinfo, e)
                    else:
                        return
                else:
                    funcname = 'on_message'
                    tbinfo = str(traceback.format_exc())
                    await self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)
        if message.channel.is_private:
            if self.bot.BotConfig.is_official_bot:
                pattern = '(https?:\/\/)?discord\.gg\/'
                regex = re.compile(pattern)
                searchres = regex.search(message.content)
                if searchres is not None:
                    await self.bot.send_message(message.channel,
                                                content=str(
                                                    self.bot.botmessages[
                                                        'join_command_data'][
                                                        3]))

    async def on_message_edit(self, before, after):
        """
        Bot Event.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        try:
            if before.channel.is_private is not False:
                if self.bot.BotConfig.logging:
                    self.bot.DBLogs.edit_logs(before, after)
            elif before.channel.server and before.channel.server.id == \
                    "81812480254291968":
                if before.author.id == self.bot.user.id:
                    return
                elif before.channel.id == "153055192873566208":
                    return
                elif before.channel.id == "87382611688689664":
                    return
                else:
                    await self.bot.DBLogs.send_edit_logs(before,
                                                         after)
            else:
                if before.channel.is_private is not False:
                    return
                elif before.channel.server.id == '95342850102796288':
                    return
                else:
                    if self.bot.BotConfig.logging:
                        self.bot.DBLogs.edit_logs(before, after)
        except Exception as e:
            funcname = 'on_message_edit'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_message_delete(self, message):
        """
        Bot Event.
        :param message: Message.
        :return: Nothing.
        """
        try:
            if message.channel.is_private is not False:
                if self.bot.BotConfig.logging:
                    self.bot.DBLogs.delete_logs(message)
            elif message.channel.server and message.channel.server.id == \
                    "81812480254291968":
                if message.author.id == self.bot.user.id:
                    return
                elif message.channel.id == "153055192873566208":
                    return
                elif message.channel.id == "87382611688689664":
                    return
                else:
                    await self.bot.DBLogs.send_delete_logs(self.bot, message)
            else:
                if message.channel.is_private is not False:
                    return
                elif message.channel.server.id == '95342850102796288':
                    return
                else:
                    if self.bot.BotConfig.logging:
                        self.bot.DBLogs.delete_logs(message)
        except Exception as e:
            funcname = 'on_message_delete'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_channel_delete(self, channel):
        """
        Bot Event.
        :param channel: Channels.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_channel_delete:
            self.bot.DBLogs.onchanneldelete(channel)

    async def on_channel_create(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_channel_create:
            self.bot.DBLogs.onchannelcreate(channel)

    async def on_channel_update(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_channel_update:
            self.bot.DBLogs.onchannelupdate(before, after)

    async def on_member_ban(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.logbans:
                self.bot.DBLogs.onban(member)
            if member.server.id == "71324306319093760":
                await self.bot.verify_cache_cleanup(member)
        except Exception as e:
            funcname = 'on_member_ban'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_member_unban(self, server, user):
        """
        Bot Event.
        :param server: Server.
        :param user: User.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.logunbans:
                self.bot.DBLogs.onunban(server, user)
        except Exception as e:
            funcname = 'on_member_unban'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_member_remove(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            try:
                banslist = await self.bot.get_bans(member.server)
                if member in banslist:
                    return
                else:
                    if self.bot.BotConfig.logkicks:
                        self.bot.DBLogs.onkick(member)
            except (discord.errors.HTTPException, discord.errors.Forbidden,
                    BotErrors.CommandTimeoutError):
                if self.bot.BotConfig.logkicks:
                    self.bot.DBLogs.onkick(member)
            if member.server and member.server.id == "71324306319093760":
                await self.bot.verify_cache_cleanup_2(member)
        except Exception as e:
            funcname = 'on_member_remove'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_member_update(self, before, after):
        """
        Bot Event.
        :param before: Member.
        :param after: Member.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_member_update:
            self.bot.DBLogs.onmemberupdate(before, after)

    async def on_member_join(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.log_member_join:
                self.bot.DBLogs.onmemberjoin(member)
            if member.server.id == '71324306319093760' and member.bot is not \
                    True:
                file_path_join_1 = '{0}resources{0}ConfigData{0}' \
                                   'serverconfigs{0}'.format(self.bot.sepa)
                filename_join_1 = 'servers.json'
                serveridslistfile = open(
                    self.bot.path + file_path_join_1 + filename_join_1)
                serveridslist = json.load(serveridslistfile)
                serveridslistfile.close()
                serverid = str(serveridslist['config_server_ids'][0])
                file_path_join_2 = '{0}resources{0}ConfigData{0}' \
                                   'serverconfigs{0}{1}{0}verificat' \
                                   'ions{0}'.format(self.bot.sepa, serverid)
                filename_join_2 = 'verifymessages.json'
                filename_join_3 = 'verifycache.json'
                filename_join_4 = 'verifycache.json'
                memberjoinmessagedatafile = open(
                    self.bot.path + file_path_join_2 + filename_join_2)
                memberjoinmessagedata = json.load(memberjoinmessagedatafile)
                memberjoinmessagedatafile.close()
                msg_info = str(memberjoinmessagedata['verify_messages'][0])
                message_data = msg_info.format(member.id, member.server.name)
                des_channel = str(
                    memberjoinmessagedata['verify_messages_channel'][0])
                joinedlistfile = open(
                    self.bot.path + file_path_join_2 + filename_join_3)
                newlyjoinedlist = json.load(joinedlistfile)
                joinedlistfile.close()
                await self.bot.send_message(discord.Object(id=des_channel),
                                            content=message_data)
                if member.id in newlyjoinedlist['users_to_be_verified']:
                    # since this person is already in the list lets
                    #  not readd them.
                    pass
                else:
                    newlyjoinedlist['users_to_be_verified'].append(member.id)
                    json.dump(newlyjoinedlist, open(
                        self.bot.path + file_path_join_2 + filename_join_4,
                        "w"))
        except Exception as e:
            funcname = 'on_member_join'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_server_available(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_available:
            self.bot.DBLogs.onavailable(server)

    async def on_server_unavailable(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_unavailable:
            self.bot.DBLogs.onunavailable(server)

    async def on_server_join(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_join:
            self.bot.DBLogs.onserverjoin(server)

    async def on_server_remove(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_remove:
            self.bot.DBLogs.onserverremove(server)

    async def on_server_update(self, before, after):
        """
        Bot Event.
        :param before: Server.
        :param after: Server.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_update:
            self.bot.DBLogs.onserverupdate(before, after)

    async def on_ready(self):
        """
        Bot Event.
        :return: Nothing.
        """
        await self.bot.on_login()
        """
        try:
            if self.bot.disable_voice_commands is not True:
                await self.bot.DBVoiceCommands.reload_commands_bypass3_new(
                    self.bot)
            else:
                return
        except Exception as e:
            funcname = 'on_ready'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)
        """

    async def on_server_role_create(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_role_create:
            self.bot.DBLogs.onserverrolecreate(role)

    async def on_server_role_delete(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_role_delete:
            self.bot.DBLogs.onserverroledelete(role)

    async def on_error(self, event, *args, **kwargs):
        """
        Bot Event.
        :param event: Event.
        :param args: Args.
        :param kwargs: Other Args.
        :return: Nothing.
        """
        str(args)
        str(kwargs)
        funcname = event
        tbinfo = str(traceback.format_exc())
        self.bot.DBLogs.on_bot_error(funcname, tbinfo, None)

    async def on_server_role_update(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_role_update:
            self.bot.DBLogs.onserverroleupdate(before, after)

    async def on_group_join(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.log_group_join:
                self.bot.DBLogs.ongroupjoin(channel, user)
        except Exception as e:
            funcname = 'on_group_join'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_group_remove(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.log_group_remove:
                self.bot.DBLogs.ongroupremove(channel, user)
        except Exception as e:
            funcname = 'on_group_remove'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_voice_state_update(self, before, after):
        """
        Bot Event.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_voice_state_update:
            self.bot.DBLogs.onvoicestateupdate(before, after)

    async def on_typing(self, channel, user, when):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :param when: Time.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_typing:
            self.bot.DBLogs.ontyping(channel, user, when)

    async def on_socket_raw_receive(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_socket_raw_receive:
            self.bot.DBLogs.onsocketrawreceive(msg)

    async def on_socket_raw_send(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_socket_raw_send:
            self.bot.DBLogs.onsocketrawsend(payload)

    async def on_resumed(self):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_resumed:
            self.bot.DBLogs.onresumed()

    # new events (Since Discord.py v0.13.0+).

    async def on_server_emojis_update(self, before, after):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_emojis_update:
            self.bot.DBLogs.onserveremojisupdate(before, after)

    # added in Discord.py v0.14.3.

    async def on_reaction_add(self, reaction, user):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_reaction_add:
            self.bot.DBLogs.onreactionadd(reaction, user)

    async def on_reaction_remove(self, reaction, user):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_reaction_remove:
            self.bot.DBLogs.onreactionremove(reaction, user)

    # added in Discord.py v0.15.0.

    async def on_reaction_clear(self, message, reactions):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_reaction_clear:
            self.bot.DBLogs.onreactionclear(message, reactions)


def setup(bot):
    """
    Registers the BotLogger class as a extension to the bot.
    """
    bot.add_cog(BotLogger(bot))
