import os

import lightbulb
from dotenvy import load_env, read_file

# ---------- LOAD ENV VARIABLES ---------- #
load_env(read_file('.env'))
BOT_SECRET = os.environ.get("BOT_SECRET")
DEV_SERVER_ID = os.environ.get("DEV_SERVER_ID")

# ---------- BOT INITIALIZATION ---------- #
bot = lightbulb.BotApp(
    token=BOT_SECRET
)

# ----------  LOAD EXTENSIONS   ---------- #
bot.load_extensions("modules.market")
bot.load_extensions("modules.help")

# ----------    BOT COMMANDS    ---------- #
@bot.command
@lightbulb.command("input", "response!")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("response!")

# ----------     MAIN LINE      ---------- #
if __name__ == '__main__':
    bot.run()
