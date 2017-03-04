# coding=utf-8
"""
levels plugin for DecoraterBot.
"""
from random import randint
import logging
import asyncio

import discord
from discord.ext import commands

log = logging.getLogger('discord')

DECORATERBOT_COLOR = int('ff4700', 16)
DECORATERBOT_ICON = 'https://cdn.discordapp.com/icons/12181641793' \
                    '7915904/2a8b4b495fbf013675a2db13a91e2a8d.jpg'


def check_add_role_perm(role, bot):
    """..."""
    permissions = bot.server_permissions
    return permissions.manage_roles and bot.top_role > role


class Levels:
    """
    DecoraterBot levels plugin.
    """

    def __init__(self, bot):
        self.bot = bot

    def botcommand(self):
        """Stores all command names in a dictionary."""
        self.bot.commands_list.append('levels')
        self.bot.commands_list.append('rank')

    def __unload(self):
        """
        Clears registered commands.
        """
        self.bot.commands_list.remove('levels')
        self.bot.commands_list.remove('rank')

    @staticmethod
    def _get_level_xp(n):
        return 5 * (n ** 2) + 50 * n + 100

    def _get_level_from_xp(self, exp):
        remaining_xp = int(exp)
        level = 0
        while remaining_xp >= self._get_level_xp(level):
            remaining_xp -= self._get_level_xp(level)
            level += 1
        return level

    @commands.command(name='levels', pass_context=True)
    async def levels(self, ctx):
        """..."""
        url = "<http://DecoraterBot.???/levels/" + ctx.message.server.id + ">"
        response = "Go check **" + ctx.message.server.name +\
                   "**'s leaderboard: "
        response += url + " :wink: "
        await self.bot.send_message(ctx.message.channel, response)

    @commands.command(name='rank', pass_context=True)
    async def rank(self, ctx):
        """..."""
        if ctx.message.mentions:
            player = ctx.message.mentions[0]
        else:
            player = ctx.message.author

        player_info = await self.get_player_info(player)

        if not player_info:
            resp = "{}, It seems like you are not ranked. " \
                   "Start talking in the chat to get ranked :wink:."
            if player != ctx.message.author:
                resp = "{}, It seems like " + player.mention + \
                       " is not ranked :cry:."
            await self.bot.send_message(ctx.message.channel,
                                        resp.format(
                                            ctx.message.author.mention))
            return

        if ctx.message.channel.permissions_for(
                ctx.message.server.me).embed_links:
            embed = discord.Embed(title='', colour=DECORATERBOT_COLOR)
            embed.add_field(name='Rank',
                            value='{}/{}'.format(player_info['rank'],
                                                 player_info['total_players']),
                            inline=True)
            embed.add_field(name='Lvl.', value=player_info['lvl'], inline=True)
            embed.add_field(name='Exp.',
                            value='{}/{} (tot. {})'.format(
                                player_info['remaining_xp'],
                                player_info['level_xp'],
                                player_info['total_xp']),
                            inline=True)
            embed.set_author(name=player.name, icon_url=player.avatar_url)
            embed.set_footer(text='DecoraterBot.???',
                             icon_url=DECORATERBOT_ICON)

            return await self.bot.send_message(ctx.message.channel,
                                               embed=embed)

        if player != ctx.message.author:
            response = '{} : **{}**\'s rank > **LEVEL {}** | **EXP {}/{}** ' \
                       '| **TOTAL EXP {}** | **Rank {}/{}**'.format(
                            ctx.message.author.mention,
                            player.name,
                            player_info['lvl'],
                            player_info['remaining_xp'],
                            player_info['level_xp'],
                            player_info['total_xp'],
                            player_info['rank'],
                            player_info['total_players'])
        else:
            response = '{} : **LEVEL {}** | **EXP {}/{}** | ' \
                       '**TOTAL EXP {}** | **Rank {}/{}**'.format(
                            player.mention,
                            player_info['lvl'],
                            player_info['remaining_xp'],
                            player_info['level_xp'],
                            player_info['total_xp'],
                            player_info['rank'],
                            player_info['total_players'])
        await self.bot.send_message(ctx.message.channel, response)

    async def get_player_info(self, member):
        """..."""
        server = member.server
        storage = await self.bot.get_storage(server)
        players = await storage.smembers('players')
        if member.id not in players:
            return None

        player_total_xp = int(
            await storage.get('player:' + member.id + ':exp'))
        player_lvl = self._get_level_from_xp(player_total_xp)
        x = 0
        for l in range(0, int(player_lvl)):
            x += self._get_level_xp(l)
        remaining_xp = int(player_total_xp - x)
        level_xp = Levels._get_level_xp(player_lvl)
        players = await storage.sort('players',
                                     by='player:*:exp',
                                     offset=0,
                                     count=-1)
        players = list(reversed(players))
        player_rank = players.index(member.id) + 1

        return {"total_xp": player_total_xp,
                "lvl": player_lvl,
                "remaining_xp": remaining_xp,
                "level_xp": level_xp,
                "rank": player_rank,
                "total_players": len(players)}

    async def on_message(self, message):
        """..."""
        if message.author.id == self.bot.user.id or message.author.bot:
            return

        # is_banned = await self.is_ban(message.author)
        # if is_banned:
        #    return

        storage = await self.bot.get_storage(message.server)

        # Updating player's profile
        player = message.author
        server = message.server
        await self.bot.db.redis.set('server:{}:name'.format(server.id),
                                    server.name)
        if server.icon:
            await self.bot.db.redis.set('server:{}:icon'.format(server.id),
                                        server.icon)
        if server.icon:
            await storage.sadd('server:icon', server.icon)
        await storage.sadd('players', player.id)
        await storage.set('player:{}:name'.format(player.id), player.name)
        await storage.set('player:{}:discriminator'.format(player.id),
                          player.discriminator)
        if player.avatar:
            await storage.set('player:{}:avatar'.format(player.id),
                              player.avatar)

        # Is the player good to go ?
        check = await storage.get('player:{}:check'.format(player.id))
        if check:
            return

        # Get the player exp
        exp = await storage.get('player:{}:exp'.format(player.id))
        if exp is None:
            exp = 0
        else:
            exp = int(exp)

        # Get the player lvl
        lvl = self._get_level_from_xp(exp)

        # Give random exp between 50 and 75
        await storage.incrby('player:{}:exp'.format(player.id),
                             randint(50, 75))
        # Block the player for 10 sec
        await storage.set('player:{}:check'.format(player.id), '1', expire=10)
        # Get the new player exp
        player_xp = int(await storage.get('player:{}:exp'.format(player.id)))
        # Comparing the level before and after
        new_level = self._get_level_from_xp(player_xp)
        if new_level != lvl:
            # Check if announcement is good
            announcement_enabled = await storage.get('announcement_enabled')
            whisp = await storage.get('whisp')
            if announcement_enabled:
                dest = message.channel
                mention = player.mention
                if whisp:
                    dest = player
                    mention = player.name
                announcement = await storage.get('announcement')
                await self.bot.send_message(dest, announcement.replace(
                    "{player}",
                    mention,
                ).replace(
                    "{level}",
                    str(new_level)
                ))
            # Updating rewards
            try:
                await self.update_rewards(message.server)
            except Exception as e:
                log.info('Cannot update rewards of server {}'.format(
                    message.server.id
                ))
                log.info(e)

    async def get_rewards(self, server):
        """..."""
        storage = await self.bot.get_storage(server)
        rewards = []
        for role in server.roles:
            lvl = int(await storage.get('reward:{}'.format(role.id)) or 0)
            if lvl == 0:
                continue
            rewards.append({'lvl': lvl,
                            'role': role})
        return rewards

    async def add_role(self, member, role):
        """..."""
        if check_add_role_perm(role, member.server.me):
            return await self.bot.add_roles(member, role)

    async def update_rewards(self, server):
        """..."""
        rewards = await self.get_rewards(server)
        storage = await self.bot.get_storage(server)
        player_ids = await storage.smembers('players')
        for player_id in player_ids:
            player = server.get_member(player_id)
            if player is None:
                continue
            player_xp = int(
                await storage.get('player:' + player.id + ':exp') or
                0)
            player_level = self._get_level_from_xp(player_xp)
            for reward in rewards:
                if reward['lvl'] > player_level:
                    continue
                role = reward['role']
                if role in player.roles:
                    continue
                try:
                    await self.add_role(player, role)
                except Exception as e:
                    log.info('Cannot give {} the {} reward'.format(player.id,
                                                                   role.id))
                    log.info(e)
            await asyncio.sleep(0.1)

    async def update_rewards_job(self):
        """..."""
        for server in list(self.bot.servers):
            plugin_enabled = 'Levels' in await self.bot.db.redis.smembers(
                'plugins:' + server.id
            )
            if not plugin_enabled:
                continue
            try:
                await self.update_rewards(server)
            except Exception as e:
                log.info('Cannot update the rewards for server ' + server.id)
                log.info(e)

            await asyncio.sleep(0.1)


def setup(bot):
    """
    DecoraterBot's Levels Plugin.
    """
    new_cog = Levels(bot)
    new_cog.botcommand()
    bot.add_cog(new_cog)
