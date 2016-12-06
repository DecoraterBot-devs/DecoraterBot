# coding=utf-8
"""
Logs plugin for DecoraterBot.

This is the default logger for DecoraterBot.
"""
import traceback
import discord


class BotLogger:
    """
    Logging Plugin Class.
    """
    def __init__(self, bot):
        self.bot = bot

    async def on_message_edit(self, before, after):
        """
        Bot Event.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        try:
            if before.channel.is_private is not False:
                if self.bot.logging:
                    self.bot.DBLogs.edit_logs(before, after)
            elif before.channel.server and before.channel.server.id == "81812480254291968":
                if before.author.id == self.bot.user.id:
                    return
                elif before.channel.id == "153055192873566208":
                    return
                elif before.channel.id == "87382611688689664":
                    return
                else:
                    await self.bot.DBLogs.send_edit_logs(self.bot, before, after)
            else:
                if before.channel.is_private is not False:
                    return
                elif before.channel.server.id == '95342850102796288':
                    return
                else:
                    if self.bot.logging:
                        self.bot.DBLogs.edit_logs(before, after)
        except Exception as e:
            funcname = 'on_message_edit'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_channel_delete(self, channel):
        """
        Bot Event.
        :param channel: Channels.
        :return: Nothing.
        """
        if self.bot.log_channel_delete:
            self.bot.DBLogs.onchanneldelete(channel)

    async def on_channel_create(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        if self.bot.log_channel_create:
            self.bot.DBLogs.onchannelcreate(channel)

    async def on_channel_update(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        if self.bot.log_channel_update:
            self.bot.DBLogs.onchannelupdate(before, after)

    async def on_member_ban(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            if self.bot.logbans:
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
            if self.bot.logunbans:
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
                    if self.bot.logkicks:
                        self.bot.DBLogs.onkick(member)
            except (discord.errors.HTTPException, discord.errors.Forbidden):
                if self.bot.logkicks:
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
        if self.bot.log_member_update:
            self.bot.DBLogs.onmemberupdate(before, after)

    async def on_member_join(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            if self.bot.log_member_join:
                self.bot.DBLogs.onmemberjoin(member)
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
        if self.bot.log_available:
            self.bot.DBLogs.onavailable(server)

    async def on_server_unavailable(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        if self.bot.log_unavailable:
            self.bot.DBLogs.onunavailable(server)

    async def on_server_join(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        if self.bot.log_server_join:
            self.bot.DBLogs.onserverjoin(server)

    async def on_server_remove(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        if self.bot.log_server_remove:
            self.bot.DBLogs.onserverremove(server)

    async def on_server_update(self, before, after):
        """
        Bot Event.
        :param before: Server.
        :param after: Server.
        :return: Nothing.
        """
        if self.bot.log_server_update:
            self.bot.DBLogs.onserverupdate(before, after)

    async def on_server_role_create(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        if self.bot.log_server_role_create:
            self.bot.DBLogs.onserverrolecreate(role)

    async def on_server_role_delete(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        if self.bot.log_server_role_delete:
            self.bot.DBLogs.onserverroledelete(role)

    async def on_server_role_update(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        if self.bot.log_server_role_update:
            self.bot.DBLogs.onserverroleupdate(before, after)

    async def on_group_join(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        try:
            if self.bot.log_group_join:
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
            if self.bot.log_group_remove:
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
        if self.bot.log_voice_state_update:
            self.bot.DBLogs.onvoicestateupdate(before, after)

    async def on_typing(self, channel, user, when):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :param when: Time.
        :return: Nothing.
        """
        if self.bot.log_typing:
            self.bot.DBLogs.ontyping(channel, user, when)

    async def on_socket_raw_receive(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        if self.bot.log_socket_raw_receive:
            self.bot.DBLogs.onsocketrawreceive(msg)

    async def on_socket_raw_send(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        if self.bot.log_socket_raw_send:
            self.bot.DBLogs.onsocketrawsend(payload)

    async def on_resumed(self):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.log_resumed:
            self.bot.DBLogs.onresumed()

    # new events (Since Discord.py v0.13.0+).

    async def on_server_emojis_update(self, before, after):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.log_server_emojis_update:
            self.bot.DBLogs.onserveremojisupdate(before, after)

    # added in Discord.py v0.14.3.

    async def on_reaction_add(self, reaction, user):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.log_reaction_add:
            self.bot.DBLogs.onreactionadd(reaction, user)

    async def on_reaction_remove(self, reaction, user):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.log_reaction_remove:
            self.bot.DBLogs.onreactionremove(reaction, user)

    # added in Discord.py v0.15.0.

    async def on_reaction_clear(self, message, reactions):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.log_reaction_clear:
            self.bot.DBLogs.onreactionclear(message, reactions)


def setup(bot):
    """
    Registers the BotLogger class as a extension to the bot.
    """
    bot.add_cog(BotLogger(bot))
