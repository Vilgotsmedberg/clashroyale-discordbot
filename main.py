import discord
from discord.ext import commands


import requests
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents=intents)

@bot.event
async def on_connect():
    print(f"Logged in as {bot.user}")



# --- Clash Royale Commands --- #
my_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjViYTQwMzAxLWM4ZTAtNDk1Mi04OGU3LTVlM2Q1NjY3MmUxMiIsImlhdCI6MTY2ODE4MDczNSwic3ViIjoiZGV2ZWxvcGVyLzVjNjY2ZWZkLTRjNTQtOTk4Ni0wNWIyLTFiNTk0MThiNzc1ZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI0NS43OS4yMTguNzkiLCIyMTMuMTAyLjg4Ljk3Il0sInR5cGUiOiJjbGllbnQifV19.feYKVPzobUTECkIp3-B_GPvC5zNYDWQeXrxiUS0t2d9qSmduj_5K4pBKkk4Mnrj-zAkI1UeRB1PQ1l2odPMa1g"

headers = {
    "Authorization": "Bearer %s" % my_key
}

def getPlayerTag(discord_id):
    f = open('linked_accounts.json')
    
    data = json.load(f)
    for i in data:
        if i["discord_id"] == f"{discord_id}":
            tag = i["tag"]
            return tag

#https://proxy.royaleapi.dev/v1/players/%23GP09QGG8C - Example URL Request

def checkUserHasAccount(discord_id):
    f = open('linked_accounts.json')
    
    data = json.load(f)

    discord_ids = []
    for r in data:
        discord_ids.append(r["discord_id"])
    if str(discord_id) in discord_ids:
        hasAccount = True
        return hasAccount
    else:
        hasAccount = False
        return hasAccount

    discord_ids.clear()

@bot.command()
async def stats(ctx):
    url = "https://proxy.royaleapi.dev/v1/players/" + "%23" + getPlayerTag(ctx.message.author.id)
    response = requests.get(f"{url}", headers=headers)
    data  = response.json()
    
    embed = discord.Embed(title = f"Stats för {data['name']} | {data['tag']}!", description =f"{data['name']} är `{data['role']}` i klanen **{data['clan']['name']}**",  color = 0xe67e22)
    embed.add_field(name = "<:green_square:1036621517393502268> Vinster:", value =f"{data['wins']}", inline=True)
    embed.add_field(name = "<:red_square:1036621517393502268> Förluster:", value = f"{data['losses']}", inline=True)
    embed.add_field(name = "<:yellow_square:1036621808683733022> Antal matcher:", value =f"{data['wins'] + data['losses']}", inline=True)

    embed.add_field(name = "<:trophy:1036401203757715506> Troféer:", value = f"{data['trophies']}", inline=True)
    embed.add_field(name = "<:star:1036621249348120597> Bästa säsong:", value = f"{data['leagueStatistics']['bestSeason']['trophies']}", inline=True)
    embed.add_field(name = "<:track_previous:1036620128005140544> Förra säsongen:", value =f"{data['leagueStatistics']['previousSeason']['trophies']}", inline=True)

    embed.add_field(name = "<:black_joker:1036622144408408115> Favoritkort:", value =f"{data['currentFavouriteCard']['name']}")
    
    await ctx.send(embed=embed)


@bot.command()
async def linkaccount(ctx, tag):
    if checkUserHasAccount(ctx.message.author.id) == False:

        dictionary = {
        "discord_id": f'{ctx.message.author.id}',
        "tag": f"{tag}"
        }
        json_object = json.dumps(dictionary, indent=2)
        with open("linked_accounts.json", "r") as infile:
            all_dictionaries = json.load(infile)

            new_dictionary = {"discord_id": f"{ctx.message.author.id}", "tag": f"{tag}"}

            all_dictionaries.append(new_dictionary)

            with open("linked_accounts.json", "w") as outfile:
                json.dump(all_dictionaries, outfile, indent=2)

            embed = discord.Embed(title = "Kontot länkat!", description = f"Ditt konto är nu länkat till taggen `{tag}`", color = 0x2ecc71)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description = f"Du har redan ett konto länkat till taggen `{getPlayerTag(ctx.message.author.id)}`!", color = 0xe74c3c)

        await ctx.send(embed=embed)


@bot.command()
async def claninfo(ctx):
    response = requests.get('https://proxy.royaleapi.dev/v1/clans/%23GLJ00Y2C', headers=headers)
    data = response.json()
    await ctx.send(data["tag"])






@bot.command()
async def gettaginfo(ctx):
    f = open('linked_accounts.json')
    
    data = json.load(f)

    discord_ids = []
    for r in data:
        discord_ids.append(r["discord_id"])
    if str(ctx.message.author.id) in discord_ids:
        await ctx.send("You have an account!")
    else:
        await ctx.send("You don't have an account!")

    discord_ids.clear()
    

    for i in data:
        if i["discord_id"] == f"{ctx.message.author.id}":
            tag = i["tag"]
            await ctx.send(f"Your tag is **{tag}**")

    f.close()

@bot.command()
async def unlink(ctx):
    if checkUserHasAccount(ctx.message.author.id) == True:
        criteria: str = str(ctx.message.author.id)

        with open("linked_accounts.json", "r") as rf:
            list_: dict = json.load(rf)

        for idx, dict_ in enumerate(list_):
            if dict_["discord_id"] == criteria:
                del list_[idx]
                print("Done!")

                with open("linked_accounts.json", "w") as outfile:
                    json.dump(list_, outfile, indent=2)
        embed = discord.Embed(title = "Kontot avlänkat!", description= "Du har nu avlänkat ditt konto. Länka igen genom att skriva `!linkaccount <tag>`", color=0xe74c3c)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description = "Du har inget konto att avlänka!", color = 0xe74c3c)
        await ctx.send(embed=embed)


#

    
@bot.command()
async def ping(ctx):
    await ctx.send("Online!")   

@bot.command()
async def accounts(ctx):
    with open("linked_accounts.json") as accounts:
        data = json.load(accounts)
        num_of_accounts = len(data)

        await ctx.send(num_of_accounts)

@bot.command()
async def serveronline(ctx):
    await ctx.send("Yes...")

bot.run("MTAzMzcyNDI1OTAwNjE3MzIyNA.G2X15P.YYXwUnA43BTz6djC-B4rEHegfPPlTsjCEGKgj0")