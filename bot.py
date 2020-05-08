import discord
import asyncio
import urllib3
import json

from discord import Game

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

client = discord.Client()
http = urllib3.PoolManager(10,
headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'})

# The following is an example. Add as many servers as you would like to the array.
servers = [["Deshi Roleplay #1", "178.128.102.180:30120", False],
           ["Asian City Roleplay #2", "139.99.125.107:30148", False],
           ["Halka Gorib #3", "103.125.254.232:30120",False],
           ["Bangladesh Premium Roleplay #1", "103.125.255.38:30120", False]]


def server_online(ip):
    req = http.request('GET', 'https://servers-live.fivem.net/api/servers/single/' + ip)
    code = req.status
    if code == 200:
        return True
    return False


def server_json(ip):
    if server_online(ip):
        req = http.request('GET', 'https://servers-live.fivem.net/api/servers/single/' + ip)
        return json.loads(req.data.decode('utf-8'))


async def server_status_check():
    await client.wait_until_ready()
    channel = discord.Object(id='708061414744653845') # This can be grabbed by right clicking on the channel and using "Copy ID"
    while not client.is_closed:
        for server_id, server in enumerate(servers):
            if not server_online(server[1]) and server[2] is False:
                print(server[0] + " " + server[1] + " OFFLINE")
                await client.send_message(channel, ":x: " + server[0] + "is now Offline! Standby for outage "
                                                                        "information! :x:")
                servers[server_id][2] = True
            if server[2] is True and server_online(server[1]):
                print(server[0] + " " + server[1] + " ONLINE")
                await client.send_message(channel, ":white_check_mark: " + server[0] + "is now Online! "
                                                                                       ":white_check_mark:")
                servers[server_id][2] = False
    await asyncio.sleep(10) # This can be changed. Default: 10 Seconds


async def server_count_status():
    await client.wait_until_ready()
    while not client.is_closed:
        player_count = 0
        for server_id, server in enumerate(servers):
            player_count += server_json(server[1])["Data"]["clients"]
        await client.change_presence(game=Game(name=str(player_count) + " players online."))
    await asyncio.sleep(5)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------ Made by Shafat')


client.loop.create_task(server_count_status())
client.loop.create_task(server_status_check())
client.run('NjkyMDgwMTkzMDg2NTU0MjA2.XrWXJg.kDF_AW7Vy_CzgdZ9-L_rV1ZgTO8') # Place the API Bot User Token here! Get this from https://discordapp.com/developers/applications
