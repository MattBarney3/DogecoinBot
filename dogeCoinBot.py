"""
dogeCoinBot.py
Joke Discord bot for a personal discord server. Tracks the % rise/fall of
dogecoin and sends a message to the server reporting the status of the
cryptocurrency.
Cryptocurrency information provided by https://messari.io/

Matt Barney
January 1st, 2021
"""

import urllib.request
import json
import asyncio
import os
import discord
from dotenv import load_dotenv

# Get the discord bot token from a .env file to keep it secret
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

"""
percentTracker() -> void
Continuously gets and updates the percent change of dogecoin from Messari
within the last hour. Keeps track of an older percentage and a newer percentage.
Prints a message dependent on the change in the currency's value, and then
waits to avoid a too many requests error.
This runs an infinite loop.

@param channel - The channel we want the bot to post in
"""
async def percentTracker(channel):
    url = "https://data.messari.io/api/v1/assets/doge/metrics"
    data = json.load(urllib.request.urlopen(url))
    oldPercent= data.get("data").get("market_data").get("percent_change_usd_last_1_hour")
    while True:
        data = json.load(urllib.request.urlopen(url))
        newPercent = data.get("data").get("market_data").get("percent_change_usd_last_1_hour")
        change = newPercent - oldPercent
        if (change > 0): # Value went up
            await channel.send("BUY BUY BUY :point_up: " + str(change) + "%")
            oldPercent = newPercent
        elif (change < 0): # Value went down
            # Already reporting the value as down, it being negative is redundant
            await channel.send("SELL SELL SELL :point_down: " + str(-1 * change) + "%")
            oldPercent = newPercent
        else: # No change in value
            await channel.send("HOLD")

        """
        Messari has a limit of 1000 requests per day so we limit the rate at
        which requests are made by waiting. Added benefit of not spamming the
        server too much.
        """
        await asyncio.sleep(60)

@client.event
async def on_ready():
    await percentTracker(client.get_channel(804869597458989094))

client.run(TOKEN)
