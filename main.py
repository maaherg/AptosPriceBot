import json
import asyncio
import discord
import time
from pycoingecko import CoinGeckoAPI

client = discord.Client(intents=discord.Intents.default())

name = None

def get_from_file(file_name):
    f=open(file_name,"r")
    data = f.read()
    f.close()

    return (data)


''' This function gets the token from the token.txt file. 
Used so that the Discord bot's token isn't compromised if this specific file is shared.'''
def get_token():
    token = get_from_file("token.txt")

    return (token)

'''This function stores the name of the cryptocurrency in the name.txt file. 
Used so that it's easier to repurpose this code for another token of your choosing.'''
def get_name():
    global name

    if (not name):
        name = get_from_file("name.txt")

    return (name)

'''Used to determine how long the program should wait before getting an updated price. Currently set to 15 seconds.'''
def get_time_gap():
    time_gap = int(get_from_file("time_gap.txt"))

    return (time_gap)

''' This function gets the price from the CoinGeckoAPI, and specifies what currency it should be displayed as.'''
def get_price():
    cg = CoinGeckoAPI()
    return cg.get_price(ids='aptos', vs_currencies='usd')

previous_time=0

async def update_status():
    global previous_time
    
    await client.wait_until_ready()

    while not client.is_closed(): #checks if the bot is online
        required_time_gap=get_time_gap()     #The time (in seconds) after the status should be updated
                                  
        curr_time=time.time()
        curr_time_gap=curr_time-previous_time
        
        if curr_time_gap>required_time_gap: #checks if the required time has passed
            response = get_price()
            price = response['aptos']['usd']
            name = get_name()

            #Updates the status to "Watching Name: 'Price'"
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{name}: ${price}'))

            #Used for debugging: print("Updated")
            previous_time=curr_time

        await asyncio.sleep(5)

@client.event
async def on_ready():
    client.loop.create_task(update_status())

token=get_token()
client.run(token)

@client.command()
async def rename(ctx, name):
    await client.user.edit(username=name)
        