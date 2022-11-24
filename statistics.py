from matplotlib import pyplot as plt
import matplotlib.style
import json
import discord.ext as discordext
import discord
import data_management
import asyncio
import time

current_servers = {}

async def stats(ctx: discordext.commands.Context, name: str):
    name.lower()
    global current_servers
    if name == "":
        await ctx.channel.send("You didn't provide name of campaign! Type 'c!stats [campaign name]' ")

        return

    if not data_management.do_exist(ctx, name):
        await ctx.channel.send(f"Campaign with this name doesn't exist")
        return

    try:
        current_servers[str(ctx.guild.id)][str(ctx.channel)] = {"mode": "s", "name": name, "delete": 2,
                                                                "author": ctx.message.author.id}

    except KeyError:
        current_servers[str(ctx.guild.id)] = {}
        current_servers[str(ctx.guild.id)][str(ctx.channel)] = {}
        current_servers[str(ctx.guild.id)][str(ctx.channel)] = {"mode": "s", "name": name, "delete": 2,
                                                                "author": ctx.message.author.id}
    finally:
        await sequence(ctx, 0)

async def check_sequence(ctx):
    global current_servers
    if str(ctx.message.channel) in current_servers[str(ctx.guild.id)].keys():
        if ctx.message.author.id == current_servers[str(ctx.guild.id)][str(ctx.channel)]["author"]:
            if ctx.message.content.isdigit():
                await sequence(ctx, int(ctx.message.content))
            else:
                await ctx.channel.send(f"Wrong input! Type a number!")
                current_servers[str(ctx.guild.id)][str(ctx.channel)]['delete'] += 2
        else:
            current_servers[str(ctx.guild.id)][str(ctx.channel)]['delete'] += 1




async def sequence(ctx: discordext.commands.Context, number):
    global current_servers
    server = str(ctx.guild.id)
    channel = str(ctx.channel)
    current = current_servers[server][channel]

    try:
        if current['mode'] == "s":
            current['mode'] = "number"
            await ctx.channel.send(f"Which statistics do you want to see: ")
            return
        if current['mode'] == "number":
            await ctx.channel.purge(limit=current['delete'])
            await get_stats(number, ctx=ctx)
            current_servers[server].pop(channel)
            if current_servers[server] == "{}":
                current_servers.pop(server)
            return
    except:
        await ctx.channel.send(f"Something went wrong! ")


async def get_stats(number, ctx):
    #time.sleep(0.1)

    match number:
        case 1:
            await w_l_perday(ctx)
        case 2:
            await w_l_summary(ctx)



async def w_l_perday(ctx: discordext.commands.Context):
    global current_servers
    data = data_management.get_data()
    name = current_servers[str(ctx.guild.id)][str(ctx.channel)]['name']
    data = data[str(ctx.guild.id)][name]['data']

    stats = {}
    for record in data:
        #if else statement bc there might be more than one report per day :)
        if record['date'] in stats.keys():
            stats[record['date']] += record['wins'] - record['loses']
        else:
            stats[record['date']] = record['wins'] - record['loses']
    plt.plot(stats.keys(), stats.values())
    plt.title("Wins - Loses: per day")
    plt.savefig("graph.png")
    plt.close()
    image = discord.File("graph.png")
    await ctx.send(file=image)

async def w_l_summary(ctx: discordext.commands.Context):
    global current_servers
    data = data_management.get_data()
    name = current_servers[str(ctx.guild.id)][str(ctx.channel)]['name']
    data = data[str(ctx.guild.id)][name]['data']

    stats = {}
    sum = 0
    for record in data:
        if record['date'] in stats.keys():
            stats[record['date']] += record['wins'] - record['loses']
            sum += record['wins'] - record['loses']
        else:
            stats[record['date']] = sum + (record['wins'] - record['loses'])
            sum += record['wins'] - record['loses']

    plt.plot(stats.keys(), stats.values())
    plt.title("Wins - Loses: overall")
    plt.savefig("graph.png")
    plt.close()
    image = discord.File("graph.png")
    await ctx.send(file=image)


