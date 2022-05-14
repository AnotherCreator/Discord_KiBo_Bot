import lightbulb

plugin = lightbulb.Plugin("help")


# ----------    BOT COMMANDS    ---------- #
# @plugin.command
# @lightbulb.command("market", "response!")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def ping(ctx):
#     await ctx.respond("response!")


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)
