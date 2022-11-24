import discord.ext as discordext
import discord
import json
import datetime


def get_data():
    with open("campaigns.json", "r") as data_file:
        data = dict(json.load(data_file))
    return data


def do_exist(ctx: discordext.commands.Context, name: str):
    name = name.lower()
    data = get_data()

    if str(ctx.guild.id) not in data.keys():
        add_server_to_keys(ctx)
        return False

    elif name not in data[str(ctx.guild.id)].keys():
        return False

    else:
        return True


def check_permissions(ctx: discordext.commands.Context, name: str):
    data = get_data()

    if ctx.message.author.guild_permissions.administrator:
        return "admin"

    if ctx.message.author.id == data[str(ctx.guild.id)][name]['author']:
        return "author"

    if ctx.message.author.id in data[str(ctx.guild.id)][name]['permissions']:
        return "permitted"

    return "none"


def add_server_to_keys(ctx: discordext.commands.Context):
    data = get_data()

    data[ctx.guild.id] = {}
    with open("campaigns.json", "w") as data_file:
        json.dump(data, data_file, indent=4)


async def add_report(ctx: discordext.commands.Context, report: dict):
    name = report['name'].lower()
    date = str(datetime.date.today())

    data = get_data()

    data[str(ctx.guild.id)][name.lower()]['data'].append(
        {"wins": report['wins'],
         "loses": report['loses'],
         "draws": report['draws'],
         "date": date}
    )

    with open("campaigns.json", "w") as data_file:
        json.dump(data, data_file, indent=4)


async def add_campaign(ctx: discordext.commands.Context, name: str):
    name = name.lower()
    if not do_exist(ctx, name):
        with open("campaigns.json", "r") as data_file:
            data = dict(json.load(data_file))

        data[str(ctx.guild.id)][name] = {
            "author": ctx.message.author.id,
            "permissions": [ctx.message.author.id],
            "data": []
        }

        with open("campaigns.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
        await ctx.channel.send(f"Successfully created new camapign {name}!")

    else:
        await ctx.channel.send(f"Campaign with name {name} alredy exist!")
