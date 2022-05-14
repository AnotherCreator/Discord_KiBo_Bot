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
    token=BOT_SECRET
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


# ----------     MAIN LINE      ---------- #
if __name__ == '__main__':

    @tasks.task(s=60, auto_start=True)
    async def refresh_coins():
        update_coins()
        print("Coins successfully updated")

    bot.run()
