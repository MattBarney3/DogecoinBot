"""
dogeCoinBot.py
Joke Discord bot for a personal discord server. Tracks the % rise/fall of 
dogecoin and sends a message to the server reporting the status of the
cryptocurrency.
Cryptocurrency information provided by https://messari.io/

Matt Barney
January 1st, 2021

TODO:
    - Actually make this a discord bot
"""

import urllib.request
import json
import time

"""
percentTracker() -> void
Continuously gets and updates the percent change of dogecoin from Messari
within the last hour. Keeps track of an older percentage and a newer percentage.
Prints a message dependent on the change in the currency's value, and then
waits to avoid a too many requests error.
This runs an infinite loop.
"""
def precentTracker():
    url = "https://data.messari.io/api/v1/assets/doge/metrics"
    data = json.load(urllib.request.urlopen(url))
    oldPercent= data.get("data").get("market_data").get("percent_change_usd_last_1_hour")
    while True:
        data = json.load(urllib.request.urlopen(url))
        newPercent = data.get("data").get("market_data").get("percent_change_usd_last_1_hour")
        change = newPercent - oldPercent
        if (change > 0): # Value went up
            print("BUY BUY BUY ↑ " + str(change) + "%")
            oldPercent = newPercent
        elif (change < 0): # Value went down
            print("SELL SELL SELL ↓ " + str(change) + "%")
            oldPercent = newPercent
        else: # No change in value
            print("HOLD")

    """
    Messari has a limit of 1000 requests per day so we limit the rate at
    which requests are made by waiting. Added benefit of not spamming the
    server too much.
    """
    time.sleep(60)
