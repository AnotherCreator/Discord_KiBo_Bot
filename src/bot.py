import hikari
import lightbulb
import os
from dotenvy import load_env, read_file
from lightbulb.ext import tasks


# ---------- LOAD ENV VARIABLES ---------- #
load_env(read_file('.env'))
BOT_SECRET = os.environ.get("BOT_SECRET")
DEV_SERVER_ID = os.environ.get("DEV_SERVER_ID")


# ---------- BOT INITIALIZATION ---------- #
bot = lightbulb.BotApp(
    token=BOT_SECRET,
    intents=hikari.Intents.ALL
)
tasks.load(bot)


# ----------  LOAD EXTENSIONS   ---------- #
bot.load_extensions("modules.market")
bot.load_extensions("modules.help")

# Extensions must be loaded before importing from those specific modules
from src.modules.market import update_coins


# ----------    BOT COMMANDS    ---------- #
@bot.command
@lightbulb.command("input", "response!")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("response!")


@bot.command
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

# ----------     MAIN LINE      ---------- #
if __name__ == '__main__':

    # ----------    BACKGROUND TASKS    ---------- #
    # Update coin database to reflect 5-min changes
    @tasks.task(s=300)
    async def refresh_coins():
        update_coins()
        print("Coins successfully updated")

    # ----------    RUN BOT & TASKS    ---------- #
    # refresh_coins.start()
    bot.run()
