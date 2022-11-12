from matplotlib import pyplot as plt
import json
import discord.ext as discordext
import discord


async def showstats(ctx: discordext.commands.Context, name):
    with open("campaigns.json", "r") as data_file:
        data = dict(json.load(data_file))
    data = data[str(ctx.guild.id)][name]

    stats = {}
    for record in data:
        if record['date'] in stats.keys():
            stats[record['date']] += record['wins'] - record['loses']
        else:
            stats[record['date']] = record['wins'] - record['loses']
    plt.plot(stats.keys(), stats.values())
    plt.savefig("graph.png")
    plt.close()
    image = discord.File("graph.png")
    await ctx.send(file=image)


