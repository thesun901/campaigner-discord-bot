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
            current_servers[str(ctx.guild.id)][str(ctx.channel)] = {"mode": "start", "name": name}

        except KeyError:
            current_servers[str(ctx.guild.id)] = {}
            current_servers[str(ctx.guild.id)][str(ctx.channel)] = {}
            current_servers[str(ctx.guild.id)][str(ctx.channel)] = {"mode": "start", "name": name}
        finally:
            await sequence(ctx, 0)


async def sequence(ctx: discordext.commands.Context, number):
    global current_servers

    server = str(ctx.guild.id)
    channel = str(ctx.channel)
    try:
        if current_servers[server][channel]['mode'] == "start":
            current_servers[server][channel]['mode'] = "w"
            await ctx.channel.send(f"Type number of wins: ")
            return

        if current_servers[server][channel]['mode'] == "w":
            current_servers[server][channel]["wins"] = number
            current_servers[server][channel]['mode'] = "l"
            await ctx.channel.send(f"Type number of loses: ")
            return

        if current_servers[server][channel]['mode'] == "l":
            current_servers[server][channel]["loses"] = number
            current_servers[server][channel]['mode'] = "d"
            await ctx.channel.send(f"Type number of draws: ")
            return

        if current_servers[server][channel]['mode'] == "d":
            current_servers[server][channel]["draws"] = number
            await data_management.add_report(ctx, current_servers[server][channel])
            await ctx.channel.send(f"Success!")

            current_servers[server].pop(channel)
            if current_servers[server] == "{}":
                current_servers.pop(server)

    except:
        await ctx.channel.send(f"Something went wrong :(")