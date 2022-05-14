import json
import lightbulb
import os
import psycopg2 as psycopg2
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

plugin = lightbulb.Plugin("market")  # Create plugin

# ----------    ENV VARS  ---------- #
CMC_API_KEY = os.environ.get("CMC_API_KEY")
DATABASE_PW = os.environ.get("DATABASE_PW")
BOT_AVATAR = os.environ.get("BOT_AVATAR")

# ----------    LOAD API   ---------- #
api_data = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
api_metadata = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CMC_API_KEY,
}

session = Session()
session.headers.update(headers)

# ----------    API PARAMETERS   ---------- #
coin_parameters = {  # Retrieve coins listed 1-100
    'start': '1',
    'limit': '100',
    'convert': 'USD',
    'aux': 'cmc_rank'
}

# ----------    CONNECT TO DB   ---------- #
con = psycopg2.connect(
    host='localhost',
    database='pybo_official',
    user='postgres',
    password=DATABASE_PW
)
cur = con.cursor()


# ----------    DATABASE FUNCTIONS  ---------- #
# Run once to initialize database and cache coins
def cache_coins():
    try:
        id_list = []
        coin_response = session.get(api_data, params=coin_parameters)
        coin_data = json.loads(coin_response.text)
        coins = coin_data['data']

        for x in coins:
            id_list.append(x['id'])
            ids = x['id']
            rank = x['cmc_rank']
            name = x['name']
            symbol = x['symbol']
            price = x['quote']['USD']['price']
            daily_change = x['quote']['USD']['percent_change_24h']

            cur.execute("INSERT INTO coin_info"
                        "(coin_id, coin_name, coin_symbol, coin_price, coin_rank, coin_daily_change)"
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (ids, name, symbol, price, rank, daily_change))
            con.commit()  # Commit transaction

        joined_id = ','.join(map(str, id_list))  # Creates comma-separated string

        metadata_parameters = {  # Retrieves coin_metadata listed 1-100
            'id': joined_id,
            'aux': 'logo'
        }
        metadata_response = session.get(api_metadata, params=metadata_parameters)
        metadata_data = json.loads(metadata_response.text)
        metadata = metadata_data['data']

        for unique_id in id_list:
            logo_url = metadata[str(unique_id)]['logo']

            cur.execute("UPDATE coin_info "  # Uses UPDATE instead of INSERT since first insertion init coin_logo column
                        "SET coin_logo = %s "
                        "WHERE coin_id = %s ",
                        (logo_url, unique_id))
            con.commit()  # Commit transaction
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def update_coins():
    try:
        coin_response = session.get(api_data, params=coin_parameters)
        coin_data = json.loads(coin_response.text)
        coins = coin_data['data']

        for x in coins:
            coin_id = x['id']
            rank = x['cmc_rank']
            price = x['quote']['USD']['price']
            daily_change = x['quote']['USD']['percent_change_24h']

            cur.execute("UPDATE coin_info "
                        "SET coin_price = %s, coin_rank = %s, coin_daily_change = %s "
                        "WHERE coin_id = %s",
                        (price, rank, daily_change, coin_id))
            con.commit()  # Commit transaction
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


# ----------    BOT COMMANDS    ---------- #
@plugin.command
@lightbulb.command("top", "Display cryptocurrency info")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def top_coins(ctx):
    pass


@top_coins.child
@lightbulb.command("rank", "Enter a coin rank")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def top_coins_rank(ctx):
    await ctx.respond("i am an sc")


@top_coins.child
@lightbulb.command("name", "Enter a coin name")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def top_coins_list(ctx):
    await ctx.respond("i am an sc")


@top_coins.child
@lightbulb.command("list", "Enter a coin rank")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def top_coins_list(ctx):
    await ctx.respond("i am an sc")


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)
