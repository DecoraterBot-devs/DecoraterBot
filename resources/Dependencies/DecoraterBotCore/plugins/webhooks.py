# coding=utf-8
"""
levels plugin for DecoraterBot.
"""

from discord.ext import commands


class WebHookRoute:
    BASE = 'https://canary.discordapp.com/api/webhooks'

    def __init__(self, method, path):
        self.path = path
        self.method = method
        url = (self.BASE + self.path)
        self.url = url

    @property
    def bucket(self):
        # the bucket is just method + path w/ major parameters
        return '{0.method}:{0.path}'.format(self)


class WebHooks:
    """
    Webhook Commands Extension.
    """
    def __init__(self, bot):
        self.bot = bot

    def botcommand(self):
        """Stores all command names in a dictionary."""
        self.bot.commands_list.append('webhook')

    def __unload(self):
        """
        Clears registered commands.
        """
        self.bot.commands_list.remove('webhook')

    @commands.command(name='webhook', pass_context=True, no_pm=True)
    async def webhook_command(self, ctx):
        """
        ::webhook request command for DecoraterBot.
        """
        msgdata = ctx.message.content[len(ctx.prefix + "webhook"):].strip()
        await self.request_webhook(
            partialurl='/284510404162355200/F2CFGqlX9UpC_hRpLIbFLzTnXncgqFdaLz09fOI92fihzfQT6lT0VB2ZjW4FtEZPcurS')

    async def request_webhook(partialurl=None):
        """Requests an webhook with the data provided to this function.
        "param partialurl: partial URL to the webhook.
        """
        if partialurl is not None:
            # TODO: Fill the payload in right (payload cannot be empty).
            payload = {}
            await self.bot.http.request(
                    WebHookRoute(
                        'POST',
                        partialurl),
                    json=payload)


def setup(bot):
    """
    DecoraterBot's Moderation Plugin.
    """
    new_cog = WebHooks(bot)
    new_cog.botcommand()
    bot.add_cog(new_cog)
