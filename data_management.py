import discord.ext as discordext
import discord
import json
import datetime


def check_existence(ctx: discordext.commands.Context, name: str):
    name = name.lower()

    with open("campaigns.json", "r") as data_file:
        data = dict(json.load(data_file))

    if str(ctx.guild.id) not in data.keys():
        add_server_to_keys(ctx)
        return False

    elif name not in data[str(ctx.guild.id)].keys():
        return False

    else:
        return True


def add_server_to_keys(ctx: discordext.commands.Context):
    with open("campaigns.json", "r") as data_file:
        data = dict(json.load(data_file))

    data[ctx.guild.id] = {}
    with open("campaigns.json", "w") as data_file:
        json.dump(data, data_file, indent=4)


async def add_report(ctx: discordext.commands.Context, report):
    name = report['name'].lower()
    date = str(datetime.date.today())

    with open("campaigns.json", "r") as data_file:
        data = dict(json.load(data_file))

    data[str(ctx.guild.id)][name.lower()].append(
        {"wins": report['wins'],
         "loses": report['loses'],
         "draws": report['draws'],
         "date": date}
    )

    with open("campaigns.json", "w") as data_file:
        json.dump(data, data_file, indent=4)


async def add_campaign(ctx: discordext.commands.Context, name: str):
    name = name.lower()
    if not check_existence(ctx, name):
        with open("campaigns.json", "r") as data_file:
            data = dict(json.load(data_file))

        data[str(ctx.guild.id)][name] = []

        with open("campaigns.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
        await ctx.channel.send(f"Successfully created new camapign {name}!")
    else:
        await ctx.channel.send(f"Campaign with name {name} alredy exist!")

