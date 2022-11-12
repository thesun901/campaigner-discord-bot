import discord
import discord.ext as discordext
import data_management

##servers under report sequence - asking about wins draws loses
current_servers = {}


async def report(ctx: discordext.commands.Context, name: str):
    name.lower()
    global current_servers
    if name == "":
        await ctx.channel.send("You didn't provide name of campaign! Type 'c!report [campaign name]' to report your progress")
        return

    if not data_management.check_existence(ctx, name):
        await ctx.channel.send(f"Campaign with this name doesn't exist")
        return

    if data_management.check_existence(ctx, name):
        try:
            current_servers[str(ctx.guild.id)][str(ctx.channel)] = {"mode": "start", "name": name, "delete": 6}

        except KeyError:
            current_servers[str(ctx.guild.id)] = {}
            current_servers[str(ctx.guild.id)][str(ctx.channel)] = {}
            current_servers[str(ctx.guild.id)][str(ctx.channel)] = {"mode": "start", "name": name, "delete": 6}
        finally:
            await sequence(ctx, 0)


async def sequence(ctx: discordext.commands.Context, number):
    global current_servers
    server = str(ctx.guild.id)
    channel = str(ctx.channel)
    current = current_servers[server][channel]

    try:
        if current['mode'] == "start":
            current['mode'] = "w"
            await ctx.channel.send(f"Type number of wins: ")
            return

        if current['mode'] == "w":
            current["wins"] = number
            current['mode'] = "l"
            await ctx.channel.send(f"Type number of loses: ")
            return

        if current['mode'] == "l":
            current["loses"] = number
            current['mode'] = "d"
            await ctx.channel.send(f"Type number of draws: ")
            return

        if current['mode'] == "d":
            current["draws"] = number
            await data_management.add_report(ctx, current)
            await ctx.channel.purge(limit=current['delete'])
            await ctx.channel.send(f"Successfully added report to campaign: '{current['name']}'! \n"
                                   f"wins: {current['wins']}    "
                                   f"loses: {current['loses']}    "
                                   f"draws: {current['draws']} \n"
                                   f"Keep on fighting warriors! ⚔")

            current_servers[server].pop(channel)
            if current_servers[server] == "{}":
                current_servers.pop(server)
    except:
        await ctx.channel.send(f"Something went wrong :(")