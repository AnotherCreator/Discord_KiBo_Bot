import lightbulb

# ----------    BOT OBJECTS    ---------- #
plugin = lightbulb.Plugin("fun")  # Create plugin


# ----------    BOT COMMANDS    ---------- #
@plugin.command
@lightbulb.command("activity", "get user activity!")
@lightbulb.implements(lightbulb.SlashCommand)
async def act(ctx):
    # bot_presence = ctx.get_guild().get_my_member().get_presence()  # Bot
    user_presence = ctx.member.get_presence()  # User who called command

    # print(bot_presence.activities)  # Bot
    print(user_presence.activities)  # User who called command - will throw error if user is invisible
    user_current_game = user_presence.activities[1].name
    if user_current_game.find("PyCharm") != -1:
        print(f"User is currently playing {user_current_game}")


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)
